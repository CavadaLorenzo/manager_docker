import paramiko, traceback
from scp import SCPClient

class SCP_handler:
    """
    this class will be handle all the scp request. It will create an ssh 
    connection and will perform the transfer
    """
    def __init__(self, host, port, user, password="password"):
        """Here will be established the connection with the given sidecar server.
        @:parameter
        host: represent the IP of the sidecar
        port: represent the port where the sidecar is listening
        password: represent the super user password of the sidecar
        """
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port, user, password)
            
    def upload_file(self, local_filename):
        """this method will upload the given file (local_filename) in the /home/
        direcotory on the sidecar. It will return True if the porcess end without
        errors or False if any exception will be throw."""
        try:
            scp = SCPClient(self.client.get_transport())
            scp.put(local_filename, recursive=True, remote_path='/home/')
            return True
        except Exception:
            tb = traceback.format_exc()
            print(tb)
            return False
        

