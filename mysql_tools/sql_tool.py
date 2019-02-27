import MySQLdb
import logging
from MySQLdb.connections import Connection


class DB:
    @classmethod
    def init_db(cls, db_config):
        if not db_config:
            return None
        db = MySQLdb.connect(**db_config)

        db.autocommit(True)
        return {
            'db': db,
        }

    def __init__(self, db_config_read, db_config_write=None):
        self.db_read = self.init_db(db_config_read)
        if not db_config_write or db_config_write == db_config_read:
            self.db_write = self.db_read
        else:
            self.db_write = self.init_db(db_config_read)

    def _exec_sql(self, db: Connection, sql: str, args=None):
        db.ping(True)

        with db.cursor() as rs:
            logging.debug(sql)
            if args is None:
                rs.execute(sql)
            else:
                rs.execute(sql, args)
            rs.commit()

    def _find_sql(self, db: Connection, sql: str, args=None):
        db.ping(True)
        # try:
        #     db.ping()
        # except MySQLdb.OperationalError:
        #     db.reconnect()
        with db.cursor() as rs:
            logging.debug(sql)
            if args is None:
                rs.execute(sql)
            else:
                rs.execute(sql, args)
            return {
                'rows': rs.fetchall(),
                'columns': [i[0] for i in rs.description] if rs.description else [],
            }

    def update(self, table_name, row_info, filter_key):
        update_sentence = ', '.join(["{}='{}'".format(k, row_info[k]) for k in row_info if k not in filter_key])
        where_sentence = ' AND '.join(["{}='{}'".format(k, row_info[k]) for k in filter_key])
        sql = """update {table_name} set {update_sentence} where {where_sentence}""".format(
                table_name=table_name,
                update_sentence=update_sentence,
                where_sentence=where_sentence,
            )
        self._exec_sql(self.db_write['db'], sql)

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
            value_s=value_s
        )
        self._exec_sql(self.db_write['db'], sql)

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
        return self._find_sql(self.db_read['db'], sql)['rows']

    def select_raw_sql(self, sql, args=None):
        return self._find_sql(self.db_read['db'], sql, args)

    def update_raw_sql(self, sql, args=None):
        self._exec_sql(self.db_write['db'], sql, args)
