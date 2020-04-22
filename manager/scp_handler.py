import paramiko, traceback
from scp import SCPClient

class SCP_handler:
    """
    this class will be handle all the scp request.
    """
    def __init__(self, host, port, user="root", password="password"):
        """Here will be established the connection with the given sidecar server.
        @:parameter
        client: the object which represent the connection to the FTP server"""
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port, user, password)
            
    def upload_file(self, local_filename):
        """this method will upload the given file (filename) in the default location."""
        try:
            scp = SCPClient(self.client.get_transport())
            scp.put(local_filename, recursive=True, remote_path='/home/')
            return True
        except Exception:
            tb = traceback.format_exc()
            print(tb)
            return False
        

