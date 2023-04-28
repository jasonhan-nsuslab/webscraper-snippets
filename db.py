import mysql.connector
import configparser

# Import database configs
vars = configparser.ConfigParser()
vars.read("vars.cfg")

class Database:
    def __init__(self, cur, conn):
        self.cur = cur
        self.conn = conn

# Local connection
def local_db():
    conn = mysql.connector.connect(
        host=vars["DB_LOCAL"]["sql_hostname"],
        port=vars["DB_LOCAL"]["sql_port"],
        user=vars["DB_LOCAL"]["sql_uname"],
        passwd=vars["DB_LOCAL"]["sql_passwd"],
        database=vars["DB_LOCAL"]["sql_db"]
    )
    return Database(conn.cursor(), conn)