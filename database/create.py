# Run:
# curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/97198408-7052-49b3-8c56-e6819a6d8314/cert
# And then:
# export DATABASE_URL="postgresql://hrl:YlSQpoc7KwnWe1BcdP-TdA@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dgame-ai-sms-2687"

import logging
import os
import psycopg
from psycopg.errors import ProgrammingError

if __name__ == "__main__":
    # Connect to CockroachDB
    connection = psycopg.connect(os.environ["DATABASE_URL"], application_name="$game-ai-sms")

    # create_query = '''DROP TABLE Users'''
    
    create_query = '''CREATE TABLE Users (phone_number varchar(12) PRIMARY KEY NOT NULL, 
                                            board varchar(255) DEFAULT '', 
                                            difficulty_level INT DEFAULT 1,
                                            win INT DEFAULT 0,
                                            loss INT DEFAULT 0,
                                            draw INT DEFAULT 0,
                                            CONSTRAINT already_exist UNIQUE (phone_number))'''

    with connection.cursor() as cur:
        cur.execute(create_query)
        connection.commit()

    # Close communication with the database
    connection.close()