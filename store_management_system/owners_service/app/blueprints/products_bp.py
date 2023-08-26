import csv
import gc  # for releasing memory when parsing file
from flask import (
    Blueprint,
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login, \
                                          login_required, roles_present
from ..models import Product, ProductCategory, IsInCategory



PRODUCTS_BP = Blueprint( 'products', __name__ )


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

    def add_products_from_file(file):
        class InvalidPrice(Exception):
            PRIORITY = 1

        class ProductAlreadyExists(Exception):
            PRIORITY = 2

        def update_err_priority(err_metric, new_err, new_err_proiority):
            if err_metric is None or err_metric[0] > new_err_proiority:
                err_metric = (new_err_proiority, new_err)
            return err_metric

        def get_categories_names(line) -> set[str]:
            return set(line[0].split('|'))

        def get_name(line: str):
            return line[1]

        def get_price(line: str):
            try:
                price = float(line[2])
                if price <= 0: raise Exception('Negative price provided')
                return price

            # in case of any exception raise exc of type InvalidPrice
            except Exception as e:
                raise InvalidPrice(f'{e}')

        def create_product_if_not_exists(name, price):
            product = Product.query.filter_by(name=name).first()
            if product is not None:
                raise ProductAlreadyExists()
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

        # Add products row by row from given file:

        def parse_file():
            reader = csv.reader(
                file.stream.read().decode('utf-8').split('\n'),
                delimiter=','
            )

            parsed_data = []
            err = None
            for idx, line in enumerate(reader):
                if len(line) != 3:  # PRIORITY 0
                    raise ParsingError(f'Incorrect number of values on line {idx}.')

                if idx % 100 == 0:  # free up freed lines
                    gc.collect()

                try:
                    # if err has occurred then look only for
                    # strictly lower lvl error => no need to raise
                    # highest lvl error (ProductAlreadyExists) and
                    # no reason to keep going after lowest one (len(line) != 3)
                    if err is not None:
                        price: float = get_price(line)
                        continue

                    categories: set[str] = get_categories_names(line)
                    name: str = get_name(line)
                    price: float = get_price(line)
                    parsed_data.append((categories, name, price))
                    del line  # free memory as raw data gets replaced by parsed

                except InvalidPrice as e:  # PRIORITY 1
                    del parsed_data
                    err = update_err_priority(
                        err,
                        ValidationError(f'Incorrect price on line {idx}.'),
                        InvalidPrice.PRIORITY
                    )

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

        # create the actual product and catgory objects in db
        for (categories, name, price) in parse_file():
            try:
                # create the product if it does not exist, else stop everything
                product = create_product_if_not_exists(name, price)

            except ProductAlreadyExists as e:  # PRIORITY 2
                raise ValidationError(f'Product {name} already exists.')

            # create its categories if they are new
            categories = create_categories_if_not_exists(categories)

            db.session.flush()  # make new product and new categories visible
            add_categories_to_product(product.id, categories)

    try:
        form_fields = fetch_fields()
        
        try:
            add_products_from_file(form_fields['file'])
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

        return '', 200  # successfully added products

    except FieldMissingError as e:
        return jsonify({
            "message": f'{e}'
        }), 400

    except ParsingError as e:
        return jsonify({
            "message": f'{e}'
        }), 400

    except ValidationError as e:
        return jsonify({
            "message": f'{e}'
        }), 400

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to add products batch')
        return f'Internal error: {e}', 500
