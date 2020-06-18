##
# @file
# The main class. The script will copy a specific file to a specif server using ssh.
# Everything starts when a get request will arrive to the port 7025. This get 
# request needs to provide a server IP + PORT where a file must 
# to be copy and, of course, the filename.
# This script is designed to run in docker so will take as enviroment variable
# the defualt password used for all the ssh conenction.
#

from flask import Flask
from flask import jsonify
from flask import request
from scp_handler import SCP_handler
import os, traceback
from postgres_DB import PostgresDB


app = Flask(__name__)

try:    DEFAULT_PSW = os.environ.get('DEFAULT_PSW')
except:     DEFAULT_PSW = "password"

@app.route("/")
def manager():
    """
    In this method will be created an instance of SCP_handler and it will be used
    to perform the copy. A json with the result of the operation will be returned.
    """
    try:
        db = PostgresDB()
        server_ip = request.args.get('server_ip')
        server_port = request.args.get('server_port')
        filename = request.args.get('filename')
        print(f"FILENAME: {filename}")

        scp = SCP_handler(server_ip, server_port, "root", DEFAULT_PSW)
        print("\nConnection established with server: " + server_ip + ":" + server_port)
        print("Searching file: " + filename)
        local_filename = "/file_storage/" + filename

        server = db.search_server(server_ip, server_port)
        if not db.check_file_existence(server[0], filename):            
            check = scp.upload_file(local_filename)
            db.add_new_file(filename, server[0])
            print("File: " + filename + " moved to server: " + server_ip + ":" + server_port + "\n")
        else:
            check = False
            print("File already on the FTP server")
        return jsonify({'result': True})
    except Exception as ex:
        print(ex.__class__, ex.__class__.__name__, flush=True)
        tb = traceback.format_exc()
        print(tb, flush=True)
        return jsonify({'result': False})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7025)
