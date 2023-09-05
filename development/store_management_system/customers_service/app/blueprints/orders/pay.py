import json
import web3
from flask import (
    request as flask_request,
    current_app,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from std_authentication.decorators import roles_required_login
from project_common.utils.request import (
    flask_request_get_typechecked as req_get_typechecked
)
from . import ORDERS_BP
from ...models import Order



@ORDERS_BP.route('/pay', methods=['POST'])
@roles_required_login(
    [ 'customer' ],
    roles_response_func=lambda _: (jsonify({ 'msg': 'Missing Authorization Header' }), 401)
)
def pay_order():
    db: SQLAlchemy = current_app.container.services.db_store_management()
    logger = current_app.logger
    w3: web3.Web3 = current_app.container.gateways.w3()


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

        if not isinstance(id, int):
            raise ParsingError(f'Invalid order id.')

        if id <= 0:
            raise ValidationError(f'Invalid order id.')

        return id

    def get_order(id: int):
        order = Order.query.filter_by(id=id).first()

        if order is None:  # order does not exist
            raise ValidationError(f'Invalid order id.')

        return order

    def get_customer_payment_info():
        # customer address and their private key, json object
        secret_customer_data = flask_request.json.get('keys', '')
        if len(secret_customer_data) == 0:
            raise FieldMissingError('Missing keys.')

        # passphrase used to decrypt the secret_customer_data
        passphrase = req_get_typechecked('json', str, 'passphrase', None)
        if passphrase is None or len(passphrase) == 0:
            raise FieldMissingError('Missing passphrase.')

        # logger.info(f'JSON: {secret_customer_data}')
        # logger.info(f'passphrase: {passphrase}')

        try:
            secret_customer_data = json.loads(secret_customer_data.replace("'", '"'))
            customer_address = w3.to_checksum_address(
                secret_customer_data['address']
            )
            private_key = web3.Account.decrypt(
                secret_customer_data,
                passphrase
            ).hex()

        except Exception as e:
            logger.exception(f'HEY I GOT : {e}')
            raise ValidationError('Invalid credentials.')

        return customer_address, private_key

    def transact_and_close_contract(
        customer_address,
        private_key,
        contract_address,
        price: int,  # in wei
    ):
        payment = current_app.container.services.smart_contracts_factory()('OrderPayment')

        try:

            transaction = (
                payment.functions.pay()
                    .build_transaction({
                        'from': customer_address,
                        'gasPrice': w3.eth.gas_price,
                        'nonce': w3.eth.get_transaction_count(customer_address),
                        'value': price,
                        'to': contract_address
                    })
            )
            transaction = w3.eth.account.sign_transaction(transaction, private_key)
            transaction_hash = w3.eth.send_raw_transaction(transaction.rawTransaction)
            receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

        except ValueError as e:
            if 'insufficient funds' in str(e):
                raise SmartContractError('Insufficient funds.')

            raise e

        except web3.exceptions.ContractLogicError as e:
            err_msg = str(e)

            if 'Restricted to all but customer.' in err_msg:  # unexpected
                raise SmartContractError('Invalid customer account.')

            if 'Only 1 transaction allowed, strictly equal to price.' in err_msg:
                raise SmartContractError('Transfer already complete.')

            raise e

    try:
        id = get_id()
        order = get_order(id)
        customer_address, private_key = get_customer_payment_info()
        transact_and_close_contract(
            customer_address,
            private_key,
            order.contract_address,
            round(order.total_price)
        )

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
