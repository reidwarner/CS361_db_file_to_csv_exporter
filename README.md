# DB To CSV Exporter Microservice - Communication Contract

This communication contract explain how to request data from the microservice, receive data from the microservice and a UML diagram showing how requesting and receiving data works.

The microservice uses a Request/Resonse communication pattern with ZeroMQ as the protocol. This allows processes to communicate with the microservice over TCP. The microservice uses a socket connection that sends and receives on local host port 5555.

## How to programmatically REQUEST data from the microservice
The microservice receives request from the calling program in the form of binary SQLite database files by listening on the endpoint `tcp://127.0.0.1:5555`.

To request data from the microservice, use the following steps:
1. Make sure the mircroservice is running
2. Create a zeroMQ REQ socket and connect to `tcp://127.0.0.1:5555`
3. Given a SQLite database file exists, read the database file and store the file as binary in a variable
4. Use `socket.send(binary_data)` to send the data to the microservice

An example call using Python can be seen below:
`import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
with open("sqlite_database.db", "rb") as f:
    db_bytes = f.read()
socket.send(db_bytes)`

<pre lang="python"><code>```python def hello(): print("Hello, world!") ```</code></pre>


## How to programmatically RECEIVE data from the microservice
The microservice will process the data and sends back a string that communicates if the CSV file creation was successful or not.

To receive data from the microservice, use the following steps:
1. Use `socket.recv_string()` to get the message string that the microservice returns and store it in a variable.
2. The returned string will be 1 of the 3 following possibilities depending on if the export was successful or not:
  1. `Export Successful. {file_name} available in Downloads folder.`
  2. `Export Failure. Incorrect data format requested.`
  3. `Export Failure. Could not located Downloads folder.`
3. If the returned message string states the export was successful, then the generated csv file will be in the local Downloads directory.

## UML sequence diagram 
