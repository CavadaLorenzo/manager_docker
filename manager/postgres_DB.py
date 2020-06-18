import psycopg2, os, uuid, datetime


# default value is used when KeyError exception is raised
try:    POSTGRES_IP =  os.environ['POSTGRES_IP'] 
except:    POSTGRES_IP = '192.168.1.190'
try:    POSTGRES_PORT = os.environ['POSTGRES_PORT'] 
except:    POSTGRES_PORT = '54320'
try:    POSTGRES_USER = os.environ['POSTGRES_USER'] 
except:    POSTGRES_USER = 'admin'
try:    POSTGRES_DB_NAME = os.environ['POSTGRES_DB_NAME'] 
except:    POSTGRES_DB_NAME = 'servers'
try:    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD'] 
except:    POSTGRES_PASSWORD = 'admin'

class PostgresDB:
    def __init__(self):
        """
        Create an object PostgreDB which connect to the given database. 

        :param host: is the database IP
        :param database: is the name of the database
        :param user: is the user used to connect to the database
        :param password: is the password used to connect to the database
        :param port: is the port used to connecto to the database
        """
        self.conn = psycopg2.connect(host = POSTGRES_IP, 
                                    database = POSTGRES_DB_NAME, 
                                    user = POSTGRES_USER, 
                                    password = POSTGRES_PASSWORD,
                                    port = POSTGRES_PORT) 

    def search_server(self, ip, port):
        """
        This method will return a specif server searching it from its
        ssh port and IP address.

        :param ip: the ip of the FTP server
        :param port: the port of the FTP server
        """
        search_server_query = f"SELECT * FROM \"Servers\" WHERE server_ssh_port = \'{port}\' AND server_ip = \'{ip}\'"
        cursor = self.conn.cursor()
        cursor.execute(search_server_query)
        self.conn.commit() 
        return cursor.fetchall()
        

    def add_new_file(self, new_file, server):
        current_date = datetime.datetime.now()
        current_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
        query  = f'INSERT INTO \"File_list\"(id, server_id, filename, upload_date) VALUES (\'{uuid.uuid1()}\', \'{server[1]}\', \'{new_file}\', \'{current_date}\')'
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def check_file_existence(self, server, filename):
        select_all_query = f"SELECT * FROM \"File_list\" WHERE server_id = \'{server[1]}\' AND filename = \'{filename}\'"
        cursor = self.conn.cursor()
        cursor.execute(select_all_query)
        self.conn.commit() 
        return len(cursor.fetchall()) > 0