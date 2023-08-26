import gc
from typing import Any
from flask import (
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from std_authentication.services import AuthenticationService
from ...models import Product, Order, OrderItem
from . import ORDERS_BP



@ORDERS_BP.route('/order', methods=['POST'])
@roles_required_login(
    ['customer'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def order_products():
    db: SQLAlchemy = current_app.container.services.db_store_management()
    logged_in_user_identifier: str \
        = AuthenticationService.get_user_identifier_from_jwt_header()
    logger = current_app.logger

    class FieldMissingError(Exception):
        pass

    class ParsingError(Exception):
        pass

    class ValidationError(Exception):
        pass

    def fetch_fields():
        form_fields = dict({
            'requests': flask_request.json.get('requests', None),
        })

        # check if all required fields have been filled out
        def check_missing_fields():
            for field_name, field_val in form_fields.items():
                if field_val is None:
                    raise FieldMissingError(f'Field {field_name} is missing.')

        check_missing_fields()
        return form_fields

    def create_order(requested_products_raw: list):
        class IPrioritizedError(Exception):
            PRIORITY = float('inf')

        class IdMissing(ParsingError, IPrioritizedError):
            PRIORITY = 0
            msg = 'Product id is missing for request number {}.'

            def __init__(self, request_idx: int) -> None:
                super().__init__(IdMissing.msg.format(request_idx))

        class QuantityMissing(ParsingError, IPrioritizedError):
            PRIORITY = 1
            msg = 'Product quantity is missing for request number {}.'

            def __init__(self, request_idx: int) -> None:
                super().__init__(QuantityMissing.msg.format(request_idx))

        class InvalidId(ValidationError, IPrioritizedError):
            PRIORITY = 2
            msg = 'Invalid product id for request number {}.'

            def __init__(self, request_idx: int) -> None:
                super().__init__(InvalidId.msg.format(request_idx))

        class InvalidQuantity(ValidationError, IPrioritizedError):
            PRIORITY = 3
            msg = 'Invalid product quantity for request number {}.'

            def __init__(self, request_idx: int) -> None:
                super().__init__(InvalidQuantity.msg.format(request_idx))

        class ProductDoesNotExist(ValidationError, IPrioritizedError):
            PRIORITY = 4
            msg = 'Invalid product for request number {}.'

            def __init__(self, request_idx: int) -> None:
                super().__init__(ProductDoesNotExist.msg.format(request_idx))

        def get_more_prioritized_err(
            err_metric: tuple[IPrioritizedError, Any],
            new_err: IPrioritizedError,
            new_err_priority: Any
        ):
            if err_metric is None or err_metric[0] > new_err_priority:
                err_metric = (new_err_priority, new_err)
            return err_metric

        def parse_request(request, request_idx: int):
            id = request.get('id', None)
            if id is None:
                raise IdMissing(request_idx)

            quantity = request.get('quantity', None)
            if quantity is None:
                raise QuantityMissing(request_idx)

            return id, quantity

        def validate_id(id: str, request_idx: int):
            try:
                id = int(id)
            except Exception:
                raise InvalidId(request_idx)

            if id <= 0:
                raise InvalidId(request_idx)

        def validate_quantity(quantity: str, request_idx: int):
            try:
                quantity = int(quantity)
            except Exception:
                raise InvalidQuantity(request_idx)

            if quantity <= 0:
                raise InvalidQuantity(request_idx)

        # Parse raw data, validate and store parsed data,
        # in case of errors keep looking for the lowest priority one and
        # do not execute any code that does not raise relevant errors
        
        # if empty list of products to add to the order was
        # passed raise IdMissing error:
        if len(requested_products_raw) == 0:
            raise IdMissing(0)

        order = Order(
            total_price=0.,
            status='CREATED',
            customer=logged_in_user_identifier,
        )

        # handle the same product id being passed
        # product_order_item[product_id] = order_item
        product_order_item = dict()
        err = None  # (err_priority, exception)
        for idx, request in enumerate(requested_products_raw):
            def add_order_item(id: int, quantity: int):
                if id in product_order_item:  # product already in order
                    product_order_item[id].quantity += quantity
                    order.total_price += quantity * product_order_item[id].price
                    return

                # lock the product and fetch its price as tuple
                price = Product.query.filter_by(
                    id=id
                ).with_for_update().with_entities(
                    Product.price
                ).first()

                if price is None: raise ProductDoesNotExist(idx)
                price = price[0]  # tuple[float] -> float

                order_item = OrderItem(
                    id_product=id,
                    id_order=order.id,
                    quantity=quantity,
                    price=price
                )
                order.items.append(order_item)

                order.total_price += quantity * price
                # associate the item to product to check if there
                # already was such product in the order
                product_order_item[id] = order_item


            if idx % 1000 == 0: gc.collect();

            try:
                id, quantity = parse_request(request, idx)
                validate_id(id, idx)
                validate_quantity(quantity, idx)
                # err != None => executed code above just to
                # search for lower priority err, no need to execute
                # code to search for the highest priority err (ProductDoesNotExist)
                if err is not None: continue;

                add_order_item(id, quantity)
                del request  # free memory as raw data gets replaced by parsed

            except IPrioritizedError as e:
                del product_order_item
                err = get_more_prioritized_err(err, e, e.__class__.PRIORITY)
                # stop early in case of lowest error priority which is 0
                if err[0] == 0: break;

            except Exception as e:  # unexpected error
                del product_order_item
                err = get_more_prioritized_err(
                    err,
                    Exception(f'Unknown error while parsing line #{idx}.\n{e}'),
                    float('inf')
                )

        if err is not None:
            raise err[1]

        return order

    try:
        form_fields = fetch_fields()
        order: Order = create_order(form_fields['requests'])

        try:
            db.session.add(order)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

        return jsonify({
            'id': order.id
        }), 200  # successfully ordered products

    except (FieldMissingError, ParsingError, ValidationError) as e:
        return jsonify({
            "message": f'{e}'
        }), 400

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to order products')
        return f'Internal error: {e}', 500
