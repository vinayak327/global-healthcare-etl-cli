import mysql.connector
import logging
from configparser import ConfigParser

class MySQLHandler:
    def __init__(self, config_file='config.ini'):
        config = ConfigParser()
        config.read(config_file)
        self.conn = mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            database=config['mysql']['database']
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        with open("sql/create_tables.sql", "r") as f:
            sql_commands = f.read()
        for stmt in sql_commands.strip().split(";"):
            if stmt.strip():
                self.cursor.execute(stmt)
        self.conn.commit()
        logging.info("Tables created.")

    def insert_data(self, table_name, data_list):
        if not data_list:
            logging.info("No data to insert.")
            return

        sample_record = data_list[0]
        keys = sample_record.keys()
        columns = ", ".join(keys)
        placeholders = ", ".join(["%s"] * len(keys))
        insert_sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"

        values = [tuple(d.values()) for d in data_list]

        try:
            self.cursor.executemany(insert_sql, values)
            self.conn.commit()
            logging.info(f"Inserted {len(values)} new records into {table_name}.")
        except mysql.connector.Error as err:
            logging.error(f"MySQL insert error: {err}")
            self.conn.rollback()

    def query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def list_tables(self):
        self.cursor.execute("SHOW TABLES")
        return self.cursor.fetchall()

    def drop_tables(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        for (table_name,) in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
        logging.info("All tables dropped.")

    def close(self):
        self.cursor.close()
        self.conn.close()
