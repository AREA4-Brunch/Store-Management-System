import web3
from .. import Payment
from ..utils import CompiledSolidityContractFactory



class OrderPayment(Payment):
    _WEB3_CONTRACT_FACTORY = CompiledSolidityContractFactory(
        'order_payment/OrderPayment-0.1.0.abi',
        'order_payment/OrderPayment-0.1.0.bin',
    )

    # attributes:
    # state: dict

    def __init__(
        self,
        owner_adress: str,
        customer_address: str,
        order_total_price: int  # in wei, uint
    ) -> None:
        super().__init__()

        payment_contract = OrderPayment._WEB3_CONTRACT_FACTORY \
                                       .create_contract()
        payment_contract.constructor(
            customer_address,
            order_total_price,
        )

        self._state = {
            'state': 'CREATED',
            'owner_address': owner_adress,
            'web3_contract': payment_contract,
        }

    def deploy_contract(self):
        """ Costs the owner_adress gas to call this. """

        contract_hash = self.state['web3_contract'].transact({
            'from': self._state['owner_address']
        })

        self._state = {
            'state': 'DEPLOYED_1',
            'contract_hash': contract_hash,
        }

    def wait_for_receiept(self):
        self._state['state'] = 'WAITING_RECEIEPT'
        receiept = web3.eth.wait_for_transaction_receiept(
            self._state['contract_hash']
        )
        self._state['state'] = 'DEPLOYED_2'
        self._state['receiept'] = receiept
