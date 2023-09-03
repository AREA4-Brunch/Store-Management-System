import web3
import pkg_resources



class CompiledSolidityContractFactory:
    def __init__(
        self,
        web3: web3.Web3,
        path_solidity_order_payment_abi,
        path_solidity_order_payment_bytecode,
    ) -> None:
        """ Given paths should be relative to pypayment module. """
        super().__init__()
        self._web3 = web3
        self._set_abi(path_solidity_order_payment_abi)
        self._set_bytecode(path_solidity_order_payment_bytecode)

    def create_contract(self) -> web3.eth.Contract:
        payment = self._web3.eth.contract(
            abi=self._abi,
            bytecode=self._bytecode
        )
        return payment

    def _set_abi(self, path_abi):
        self._abi = pkg_resources.resource_stream(
            'pypayment',
            path_abi  # relative to pypayment
        )

    def _set_bytecode(self, path_bytecode):
        self._bytecode = pkg_resources.resource_stream(
            'pypayment',
            path_bytecode
        )
