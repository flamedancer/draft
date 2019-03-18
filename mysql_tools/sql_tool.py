import MySQLdb
import logging
from MySQLdb.connections import Connection


class FindResult:
    def __init__(self, rows, columns=None):
        self.rows = rows
        self.columns = columns
        self.length = len(rows)

    def assoc(self):
        assoc_attr = '_assoc'
        if hasattr(self, assoc_attr):
            return self._assoc
        if not self.columns or (self.rows and len(self.columns) != len(self.rows[0])):
            raise ValueError('no columns or the len of columns and row not same')
        assoc_result = []
        for row in self.rows:
            assoc_result.append(dict(zip(self.columns, row)))
        setattr(self, assoc_attr, assoc_result)
        return assoc_result

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.rows[key]
        if key == 'rows':
            return self.rows
        if key == 'columns':
            return self.columns

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        self.index += 1
        if self.index > self.length:
            raise StopIteration
        return self.rows[self.index - 1]


class DB:
    @classmethod
    def init_db(cls, db_config):
        if not db_config:
            return None
        db = MySQLdb.connect(**db_config)
        return {
            'db': db,
        }

    def __init__(self, db_config_read, db_config_write=None):
        self.db_read = self.init_db(db_config_read)
        if not db_config_write or db_config_write == db_config_read:
            self.db_write = self.db_read
        else:
            self.db_write = self.init_db(db_config_read)

    def close(self):
        if self.db_read['db']:
            self.db_read['db'].close()
        if self.db_write != self.db_read:
            self.db_write['db'].close()

    def _exec_sql(self, db: Connection, sql: str, args=None):
        db.ping(True)

        with db.cursor() as rs:
            logging.debug(sql)
            if args is None:
                rs.execute(sql)
            else:
                rs.execute(sql, args)
            db.commit()

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
            return FindResult(
                rs.fetchall(),
                [i[0] for i in rs.description] if rs.description else []
            )

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

    def select(self, table_name, query_list, filter_info=None, limit=None, order_by=None, ):
        query_columns_s = ', '.join(query_list)
        sql = """SELECT {query_columns_s} FROM {table_name} """.format(
            table_name=table_name,
            query_columns_s=query_columns_s,
        )
        if filter_info:
            where_sentence = "WHERE " + ' AND '.join(["{}='{}'".format(k, v) for k, v in filter_info.items()])
            sql += where_sentence
        if order_by:
            if isinstance(order_by, str):
                sql += " order by {}".format(order_by)
            else:
                sql += " order by {}".format(','.join(order_by))
        if limit:
            sql += " limit {}".format(limit)
        return self._find_sql(self.db_read['db'], sql)

    def select_one_assoc(self, table_name, query_list, filter_info=None):
        rst = self.select(table_name, query_list, filter_info, limit=1)
        if not rst:
            return {}
        return rst.assoc()[0]

    def select_raw_sql(self, sql, args=None):
        return self._find_sql(self.db_read['db'], sql, args)

    def update_raw_sql(self, sql, args=None):
        self._exec_sql(self.db_write['db'], sql, args)
