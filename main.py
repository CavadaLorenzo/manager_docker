from flask import Flask
from flask import jsonify
from flask import request
from scp_handler import SCP_handler
import os, traceback
import subprocess


app = Flask(__name__)
DEFAULT_PSW = os.environ['DEFAULT_PSW']

@app.route("/")
def manager():
    try:
        server_ip = request.args.get('server_ip')
        server_port = request.args.get('server_port')
        filename = request.args.get('filename')
        
        print(request.args.get('server_ip'))
        print(request.args.get('server_port'))
        print(request.args.get('filename'))

        scp = SCP_handler(server_ip, server_port, "root", DEFAULT_PSW)
        print("\nConnection established with server: " + server_ip + ":" + server_port)
        check = True
        print("Searching file: " + filename)
        local_filename = "/file_storage/" + filename
        check = scp.upload_file(local_filename)
        print("File: " + filename + " moved to server: " + server_ip + ":" + server_port + "\n")
        return jsonify({'result': True})
    except Exception as ex:
        print(ex.__class__, ex.__class__.__name__, flush=True)
        tb = traceback.format_exc()
        print(tb, flush=True)
        return jsonify({'result': False})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7025)
