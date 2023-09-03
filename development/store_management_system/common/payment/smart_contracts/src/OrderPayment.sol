// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;


contract OrderPayment {
    address payable public owner;
    address payable public courier;
    address public customer;  // not payable <=> cannot get money
    uint private price;  // in wei
    // served its purpose, now is read only
    bool private is_closed;

    constructor(address _customer, uint _price) {
        owner = payable(msg.sender);
        customer = _customer;
        price = _price;
    }

    modifier notClosed() {
        require(is_closed == false, "Closed.");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Restricted to all but owner.");
        _;  // run all code the modifier is decorating
    }

    modifier onlyCustomer() {
        require(msg.sender == customer, "Restricted to all but customer.");
        _;  // run all code the modifier is decorating
    }

    modifier courierAssigned(bool require_yes) {
        require(
            require_yes ? courier != address(0)
                        : courier == address(0),
            require_yes ? "Requires courier to have been assigned."
                        : "Requires courier not to have been assigned."
        );
        _;
    }

    /// accepts given money within contract's balance
    /// only if the total provided amount does not exceed the price
    function receieve() payable external
        notClosed onlyCustomer
    {
        require(
            address(this).balance + msg.value <= price,
            "Total amount provided must strictly equal to price."
        );
    }

    function assignCourier(address payable _courier) public
        notClosed onlyOwner courierAssigned(false)
    {
        require(
            address(this).balance == price,
            "Courier is to be assigned only after total price was recieved."
        );
        courier = _courier;
    }

    function confirmDelivery() payable external
        notClosed onlyCustomer courierAssigned(true)
    {
        uint owner_profit = price * 80 / 100;  // 80% price
        uint courier_profit = price - owner_profit;  // 20% price
        owner.transfer(owner_profit);
        courier.transfer(courier_profit);
        is_closed = true;
    }

}
