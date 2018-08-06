import MySQLdb
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB:
    @classmethod
    def init_db(cls, db_config):
        if not db_config:
            return None
        db_uri = "mysql+mysqldb://{user}:{passwd}@{host}:{port}/{db}?charset={charset}".format(**db_config)
        sql_engine = create_engine(db_uri)
        session = sessionmaker(bind=sql_engine)()
        db = MySQLdb.connect(**db_config)
        cursor = db.cursor()
        return {
            'db_uri': db_uri,
            'sql_engine': sql_engine,
            'session': session,
            'db': db,
            'cursor': cursor,
        }

    def __init__(self, db_config_read, db_config_write=None):
        if db_config_write is None:
            db_config_write = db_config_read
        self.db_read = self.init_db(db_config_read)
        self.db_write = self.init_db(db_config_read)

    def update(self, table_name, row_info, filter_key):
        update_sentence = ', '.join(["{}='{}'".format(k, row_info[k]) for k in row_info if k not in filter_key])
        where_sentence = ' AND '.join(["{}='{}'".format(k, row_info[k]) for k in filter_key])
        sql = """update {table_name} set {update_sentence} where {where_sentence}""".format(
                table_name=table_name,
                update_sentence=update_sentence,
                where_sentence=where_sentence,
            )
        logging.debug(sql)
        logging.debug(self.db_write['cursor'].execute(sql))
        self.db_write['cursor'].commit()

    def insert(self, table_name, row_info, unique_key=None):
        if unique_key:
            filter_info = {key: row_info[key] for key in unique_key}
            if self.select(table_name, unique_key, filter_info, limit=1):
                logging.debug('DUMPLICA insert table %s vale %s', table_name, row_info)
                self.update(table_name, row_info, unique_key)
                return
        row_columns = list(row_info.keys())
        row_columns_s = ', '.join(row_columns)
        value_s = ', '.join(['%s'] * len(row_columns))
        values = [row_info[key] for key in row_columns]

        sql = """insert ignore into {table_name} ({row_columns_s}) values ({value_s})""".format(
            table_name=table_name,
            row_columns_s=row_columns_s,
            value_s=value_s,
        )
        logging.debug(sql)
        logging.debug(self.db_write['cursor'].execute(sql, values))
        self.db_write['cursor'].commit()

    def select(self, table_name, query_list, filter_info=None, limit=None):
        query_columns_s = ', '.join(query_list)
        sql = """SELECT {query_columns_s} FROM {table_name} """.format(
            table_name=table_name,
            query_columns_s=query_columns_s,
        )
        if filter_info:
            where_sentence = "WHERE " + ' AND '.join(["{}='{}'".format(k, v) for k, v in filter_info.items()])
            sql += where_sentence
        if limit:
            sql += " limit {}".format(limit)
        logging.debug(sql)
        self.db_read['cursor'].execute(sql)
        return self.db_read['cursor'].fetchall()

    def select_raw_sql(self, sql, args=None):
        if args is None:
            self.db_read['cursor'].execute(sql)
        else:
            self.db_read['cursor'].execute(sql, args)
        return self.db_read['cursor'].fetchall()

    def update_raw_sql(self, sql, args=None):
        if args is None:
            self.db_write['cursor'].execute(sql)
        else:
            self.db_write['cursor'].execute(sql, args)
        self.db_write['cursor'].commit()

    def get_columns(self):
        return [i[0] for i in self.db_read['cursor'].description]


if __name__ == '__main__':
    db_config_read = {
        'host': '127.0.0.1',
        'db': 's2c',  # www
        'user': 'guochen',
        'passwd': '1111',
        'charset': 'utf8mb4',
        'port': 3306,
    }
    db_config_write = db_config_read
    db = DB(db_config_read, db_config_write)
    result = db.select_raw_sql("show databases;")
    print(result)
    
