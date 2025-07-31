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

<pre lang="python"><code>
import zmq

# Create socket and connect to local host port 5555
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

# Given the file sqlite_database.db exists in the local directory, store the binary in db_bytes
with open("sqlite_database.db", "rb") as f:
    db_bytes = f.read()

# Send binary data to the microservice
socket.send(db_bytes)
</code></pre>

The example call above assumes that a SQLite database file exists in the current directory of the calling program. An example of the `sqlite_database.db` is the SQLite database file created by inserting data into the table created by the following SQL query

<pre lang="sql"><code>
'''CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL
        )'''
</code></pre>


## How to programmatically RECEIVE data from the microservice
The microservice will process the data and sends back a string that communicates if the CSV file creation was successful or not.

To receive data from the microservice, use the following steps:
1. Use `socket.recv_string()` to get the message string that the microservice returns and store it in a variable.
2. The returned string will be 1 of the 3 following possibilities depending on if the export was successful or not:
  1. `Export Successful. {file_name} available in Downloads folder.`
  2. `Export Failure. Incorrect data format requested.`
  3. `Export Failure. Could not located Downloads folder.`
3. If the returned message string states the export was successful, then the generated csv file will be in the local Downloads directory.

An example of a way to receive data from the microservice in Python, is to add the following lines to the request example above:

<pre lang="python"><code>
# Wait for reply from microservice
reply = socket.recv_string()
print(reply)
</code></pre>

If successful, the output of the above print statement will be:

<pre><code>
Example Output:
    
    Export Successful. db_export_2025-07-31_15-32-45.csv available in Downloads folder.
    
</code></pre>

## UML sequence diagram 
