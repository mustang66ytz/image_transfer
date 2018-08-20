# image transfer package:
## There are both cpp and python versions of the image transfer nodes
run the server first, and then the client to request image from the server.
you may provide images to be sent and specify the path in the server node, and also specify the path and the name the received image you want to save.

## Some commands to execute the image transfer services:
You can find a random unused port by running '. ./random_unused_port.sh' and 'echo $RANDOM_PORT'
Execute the cpp nodes by running './server' and './client'
Execute the python nodes by runnning 'python imgtest_server.py' and 'python imgtest_client.py' 
