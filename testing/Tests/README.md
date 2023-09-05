Start the deployment/docker-compose.yaml and once the containers up
(aside from migration containers which should have status exited with error code 0)
then in the logs of ethreum-simulator container copy paste 0-th and any other
private key and paste in ./run.ps1 as owner and couriers private keys respectively.
Then run ./run.ps1, tests on LEVEL 3 take around 8 minutes.
