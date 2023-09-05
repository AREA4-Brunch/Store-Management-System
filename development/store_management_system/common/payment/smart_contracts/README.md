To compile run from src/ following cmd:


docker container run -v $(pwd):/app ethereum/solc:stable --bin --abi app/OrderPayment.sol --output-dir app/ 

<!-- THIS ONE -->
docker container run -v $(pwd):/app ethereum/solc:0.8.18 --bin --abi app/OrderPayment.sol --output-dir app/ 
