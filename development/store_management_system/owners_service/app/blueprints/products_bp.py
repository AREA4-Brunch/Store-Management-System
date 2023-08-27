import csv
import gc  # for releasing memory when parsing file
from flask import (
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from . import PRODUCTS_BP
from ..models import Product, ProductCategory, IsInCategory



@PRODUCTS_BP.route('/update', methods=['POST'])
@roles_required_login(
    ['owner'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def add_products_batch():
    db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger

    class FieldMissingError(Exception):
        pass

    class ParsingError(Exception):
        pass

    class ValidationError(Exception):
        pass

    def fetch_fields():
        form_fields = dict({
            'file': flask_request.files.get('file', None),
        })

        # check if all required fields have been filled out
        def check_missing_fields():
            for field_name, field_val in form_fields.items():
                if field_val is None:
                    raise FieldMissingError(f'Field {field_name} is missing.')

        check_missing_fields()
        return form_fields

    def get_products_to_add_data(file):
        class InvalidPrice(ValidationError):
            PRIORITY = 1
            msg = 'Incorrect price on line {}.'

            def __init__(self, line_idx: int) -> None:
                super().__init__(InvalidPrice.msg.format(line_idx))

        def update_err_priority(err_metric, new_err, new_err_priority):
            if err_metric is None or err_metric[0] > new_err_priority:
                err_metric = (new_err_priority, new_err)
            return err_metric

        def get_categories_names(line) -> set[str]:
            return set(line[0].split('|'))

        def get_name(line: str):
            return line[1]

        def get_price(line: str, line_idx: int):
            try:
                price = float(line[2])
            except Exception:
                raise InvalidPrice(line_idx)

            if price <= 0:
                raise InvalidPrice(line_idx)

            return price

        # Add products row by row from given file:

        reader = csv.reader(
            file.stream.read().decode('utf-8').split('\n'),
            delimiter=','
        )

        # parse raw data, validate and store parsed data,
        # in case of errors keep looking for the lowest priority one and
        # do not execute any code that does not raise relevant errors
        parsed_data = []
        err = None
        for idx, line in enumerate(reader):
            if len(line) != 3:  # PRIORITY 0
                raise ParsingError(f'Incorrect number of values on line {idx}.')

            # err != None => executed code above just to
            # search for lower priority err
            if err is not None:
                continue

            # free up freed lines
            if idx % 100 == 0: gc.collect();

            try:
                categories: set[str] = get_categories_names(line)
                name: str = get_name(line)
                price: float = get_price(line, idx)
                parsed_data.append((categories, name, price))
                del line  # free memory as raw data gets replaced by parsed

            except (InvalidPrice) as e:  # not lowest lvl PRIORITY
                del parsed_data
                err = update_err_priority(err, e, e.__class__.PRIORITY)

            except Exception as e:
                del parsed_data
                err = update_err_priority(
                    err,
                    Exception(f'Unknown error while parsing line #{idx}.\n{e}'),
                    float('inf')
                )

        if err is not None:  # raise lowest priority error
            raise err[1]
        
        return parsed_data

    def add_products(products_to_add):
        class ProductAlreadyExists(ValidationError):
            # PRIORITY = 2
            msg = 'Product {} already exists.'

            def __init__(self, name: str) -> None:
                super().__init__(ProductAlreadyExists.msg.format(name))

        def create_product_if_not_exists(name, price):
            product = Product.query.filter_by(name=name).first()
            if product is not None:
                raise ProductAlreadyExists(name)
            product = Product(name=name, price=price)
            db.session.add(product)
            return product
        
        def create_categories_if_not_exists(categories_names: set[str]):
            categories = []
            for name in categories_names:
                category = ProductCategory.query.filter_by(name=name).first()
                if category is None:
                    category = ProductCategory(name=name)
                    db.session.add(category)
                categories.append(category)
            return categories

        def add_categories_to_product(product_id, categories: list[ProductCategory]):
            """ Assumes product is currently in no given categories. """
            for category in categories:
                is_in_category = IsInCategory(
                    id_product=product_id,
                    id_product_category=category.id
                )
                db.session.add(is_in_category)

        # create the actual product and catgory objects in db
        for (categories, name, price) in products_to_add:
            # create the product if it does not exist, else stop everything
            product = create_product_if_not_exists(name, price)
            # create its categories if they are new
            categories = create_categories_if_not_exists(categories)
            db.session.flush()  # make new product and new categories visible
            add_categories_to_product(product.id, categories)

    try:
        form_fields = fetch_fields()
        products_to_add = get_products_to_add_data(form_fields['file'])

        try:
            add_products(products_to_add)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

        return '', 200  # successfully added products

    except (FieldMissingError, ParsingError, ValidationError) as e:
        return jsonify({
            "message": f'{e}'
        }), 400

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to add products batch')
        return f'Internal error: {e}', 500
