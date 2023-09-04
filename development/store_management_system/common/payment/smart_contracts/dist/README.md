To compile run from src/ following cmd:


docker container run -v $(pwd):/app ethereum/solc:stable --bin --abi app/OrderPayment.sol --output-dir app/ 

<!-- THIS ONE -->
docker container run -v $(pwd):/app ethereum/solc:0.8.18 --bin --abi app/OrderPayment.sol --output-dir app/ 


docker run -v ${PWD}/solidity:/sources ethereum/solc:0.8.18 -o /sources/output --abi --bin /sources/OrderPayment.sol

