import logging
import os
import psycopg
from psycopg.errors import ProgrammingError

def commit(query):
    # just for debug
    print(query)

    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"], application_name="$ docs_quickstart_python")

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    # Close communication with the database
    connection.close()

def get(query):
    # just for debug
    print(query)

    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"], application_name="$ docs_quickstart_python")

    result = None

    with connection.cursor() as cur:
        cur.execute(query)
        result = cur.fetchone()
        connection.commit()

    # Close communication with the database
    connection.close()

    # return the result
    return result

def create_user(phone : str):
    query = "INSERT INTO Users (phone_number) VALUES ({number})".format(number = phone)
    commit(query)

def check_user_exist(phone: str) -> bool:
    query = "SELECT COUNT(*) FROM Users WHERE phone_number = \'{number}\'".format(number = phone)  # either 1 or 0
    result = get(query)
    print(result)
    return result[0] == 1


def select(attribute : str, phone : str):
    query = "SELECT {at} FROM Users WHERE phone_number = \'{number}\'".format(at = attribute, number = phone)
    return get(query)[0]

def update(attribute : str, phone : str, content):
    query = "Update Users SET {at} = \'{c}\' WHERE Users.phone_number = \'{number}\'".format(at = attribute, c = content, number = phone)
    commit(query)

def update_board(phone : str, board : str):
    update("board", phone, board)

def get_board_for(phone : str):
    query = "SELECT board FROM Users WHERE phone_number = \'{number}\'".format(number = phone)
    return get(query)[0]

def get_difficulty_level_for(phone : str):
    return select("difficulty_level", phone)

def update_difficulty_level(phone : str, difficulty_level : int):
    update("difficulty_level", phone, difficulty_level)

def get_win(phone : str):
    return select("win", phone)

def update_win(phone : str):
    pass

def get_loss(phone : str):
    return select("loss", phone)

def update_loss(phone : str):
    pass

def get_draw(phone : str):
    return select("draw", phone)

def update_draw(phone: str):
    pass

def get_everything():
    query = '''SELECT * FROM Users'''
    return get(query)