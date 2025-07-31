import zmq
from data_processing import process_sqlite_bin_helper

# Setup Socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")

# Loop while listening for requests
while True:
    db_bytes = socket.recv()
    if db_bytes:
        file_name, db_error, csv_error = process_sqlite_bin_helper(db_bytes)

        # Process any errors and send confirmation string to calling program
        if not db_error and not csv_error:
            msg = f"Export Successful. {file_name} available in Downloads folder."
        elif db_error:
            msg = f"Export Failure. Incorrect data format requested."
        else:
            msg = f"Export Failure. Could not located Downloads folder."

        socket.send_string(msg)
