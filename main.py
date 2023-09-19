"""
This script allows us to make backup copies on a mysql server by 
providing the server connection data and a list of databases. Additionally, 
if you provide it with a database that does not exist instead 
of creating an empty file, it will skip it.

Finally, it allows you to send slack messages to a 
specific group with the final result of your backups.
"""
# pylint: disable=W1203
import subprocess
from pathlib import Path
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
from utils.variables import BACKUP_FOLDER, DB_HOST, DB_PASS, DB_PORT, DB_USER, DATABASES, SLACK_FILENAME, SLACK_WEBHOOK_URL
from utils.logger import Logger
from utils.slack import SlackNofifier

DATE = datetime.now().strftime("%Y-%m-%d")

backup_folder = Path(BACKUP_FOLDER)
if not backup_folder.exists():
    backup_folder.mkdir(parents=True, exist_ok=True)

def mysql_databases():
    """
    This function is responsible for creating the connection to the database and
        obtaining all the databases
    Return:
        database_list (list): List of all databases on the server
    """
    try:
        log.info("Creating the connection to the database...")
        cnx = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            log.error("User/password error")
        elif err.errno == errorcode.CR_SERVER_GONE_ERROR:
            log.error("Server down error")
        else:
            log.exception(f"Something went wrong: {err}")
    else:
        log.info("The connection to the database has been created successfully.")
        cursor = cnx.cursor()

    cursor.execute("SHOW DATABASES")
    database_list = [database for _tuple in cursor for database in _tuple]
    return database_list

def check_databases(database_list: list, ddbb: str):
    """
    This function is responsible for creating a definitive list, 
        discarding databases that are not on the server.
    Params:
        database_list (list): List of all databases on the server
        ddbb (str): User Provided Database
    Return:
        final_list_databases: Returns the final list of databases that will be backed up
    """
    final_list_databases = []
    ddbb = ddbb.lstrip()
    if not ddbb in database_list:
        log.error(f"The {ddbb} database does not exist on the server, it is ignored.")
        message =  f"❌ The {ddbb} database does not exist on the server, it is ignored."
        slack_message.write_message(message)
    else:
        final_list_databases.append(ddbb)
    return final_list_databases

def get_dump(dblist: list):
    """
    This function is responsible for creating the backup.
    Params:
            dblist (str): list of databases that will be backed up.
    """
    for ddbb in dblist:
        result = subprocess.run([f"""mysqldump -u {DB_USER} -p{DB_PASS} -h {DB_HOST} -P {DB_PORT} {ddbb} > {BACKUP_FOLDER}/{ddbb}-{DATE}.sql"""],
                   check=True, shell=True, capture_output=True)
        if result.returncode == 0:
            message = f"✅ The {ddbb} database backup was successful."
        else:
            message = f"❌ The {ddbb} database backup has failed."

        slack_message.write_message(message)

def main():
    """
    Main function that is responsible for defining the workflow of the script.
    """
    log.info("Started")
    all_databases = mysql_databases()
    for database in list(DATABASES):
        final_databases = check_databases(all_databases, database)
        get_dump(final_databases)
    log.info("Finished")
    slack_message.send_message()

if __name__ == "__main__":
    log = Logger(__name__).setup()
    slack_message = SlackNofifier(SLACK_WEBHOOK_URL, SLACK_FILENAME)
    main()
