from getpass import getpass
from mysql.connector import connect, Error, MySQLConnection
from configparser import ConfigParser


def connect_to_mysql():
    """" Connect to MySQL database """
    try:
        connection = connect(
                host="localhost",
                user=input("Имя пользователя: "),
                password=input("Пароль: "),
                database="cinema"
        )
        return connection
    except Error as e:
        print(e)


def connect_to_mysql_config():
    """ Connect to MySQL database """

    db_config = read_db_config()

    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')
        return conn
    except Error as error:
        print(error)


def read_db_config(filename='config.ini', section='mysql'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def read_query_config(section, filename='config.ini'):
    if section is None:
        raise Exception("Select none section");

    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        items = parser.items(section)
        return items[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))



def query_mysql(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM hall")

        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()
    except Error as e:
        print(e)
    finally:
        cursor.close()


def insert_movie(connection, name, time):
    query = "INSERT INTO movie(movie_name, movie_time) VALUES(%s,%s)"
    args = (name, time)
    try:
        cursor = connection.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        connection.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()


def update_movie(connection, book_id, time):
    query = """ UPDATE movie
                SET movie_time = %s
                WHERE id = %s """

    data = (time, book_id)

    try:
        cursor = connection.cursor()
        cursor.execute(query, data)

        # accept the changes
        connection.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()

def delete_movie(coonection, movie_id):
    query = "DELETE FROM movie WHERE id = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (movie_id,))

        # accept the change
        connection.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()

if __name__ == '__main__':
    connection = connect_to_mysql_config()
    if connection.is_connected():
        print("Connected to MySQL database")
        print("Select hall")
        query_mysql(connection)
        read_query_config(section="insert_movie")
        connection.close();
