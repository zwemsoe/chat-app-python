import psycopg2


class DB:
    def __init__(self, config):
        self.host = config["DB_HOST"]
        self.username = config["DB_USERNAME"]
        self.password = config["DB_PASSWORD"]
        self.database = config["DB_DATABASE"]
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    database=self.database,
                )
            except psycopg2.DatabaseError as e:
                print(e)
            except Exception as e:
                print(e)
            else:
                print("Connection successful")
