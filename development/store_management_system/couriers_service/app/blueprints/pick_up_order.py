import web3  # module w3
from flask import (
    request as flask_request,
    current_app,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from project_common.utils.request import (
    flask_request_get_typechecked as req_get_typechecked
)
from . import ORDERS_BP
from ..models import Order



@ORDERS_BP.route('/pick_up_order', methods=['POST'])
@roles_required_login(
    ['courier'],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def pick_up_order():
    db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger
    w3: web3.Web3 = current_app.container.gateways.w3()
    # pretend the first account is always the owners
    owner_address = w3.eth.accounts[0]

    class FieldMissingError(Exception):
        pass

    class ParsingError(Exception):
        pass

    class ValidationError(Exception):
        pass

    class SmartContractError(Exception):
        pass

    def get_id():
        id = flask_request.json.get('id', None)
        if id is None:
            raise FieldMissingError(f'Missing order id.')

        try:  # convert to int
            id = int(id)
        except Exception:
            raise ParsingError(f'Invalid order id.')

        if id <= 0:
            raise ValidationError(f'Invalid order id.')

        return id

    def get_order(id: int):
        order = Order.query.filter_by(id=id).first()

        if order is None:  # order does not exist
            raise ValidationError(f'Invalid order id.')

        # check if the order has not been picked or deliverd
        # up by any courier yet
        if order.status != 'CREATED':
            raise ValidationError(f'Invalid order id.')

        return order

    def get_courier_address():
        courier_address = req_get_typechecked('json', str, 'address', None)
        if courier_address is None or len(courier_address) == 0:
            raise FieldMissingError('Missing address.')
        return courier_address

    def validate_courier_address(courier_address):
        if not w3.is_address(courier_address):
            raise ValidationError('Invalid address.')

    def assign_courier(contract_address):
        payment = current_app.container.services.smart_contracts_factory()(
            'OrderPayment',
            contract_address
        )

        try:
            payment.functions.assignCourier(
                courier_address
            ).transact({
                'from': owner_address,
            })

        except web3.exceptions.ContractLogicError as e:
            err_msg = str(e)

            # if 'Restricted to all but owner.' in err_msg:  # unexpected
            #     raise e

            # if 'Requires courier not to have been assigned.' in err_msg:  # unexpected
            #     raise e

            if 'Not full price was paid.' in err_msg:
                raise SmartContractError('Transfer not complete.')

            raise e

        except Exception as e:
            raise ValidationError('Invalid customer account.')

    try:
        id = get_id()
        order = get_order(id)
        courier_address = get_courier_address()
        validate_courier_address(courier_address)
        assign_courier(order.contract_address)

        try:
            order.status = 'PENDING'
            db.session.add(order)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

        return '', 200

    except (
        FieldMissingError,
        ParsingError,
        ValidationError,
        SmartContractError
    ) as e:
        return jsonify({
            'message': f'{e}'
        }), 400

    except Exception as e:  # unexpected error
        logger.exception(f'Failed to set the order\'s status `COMPLETE`.')
        return f'Internal error: {e}', 500
