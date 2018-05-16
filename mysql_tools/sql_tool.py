import datetime
import time
import MySQLdb
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

session = None
cursor = None
db = None



def init(db_config):
    db_uri = "mysql+mysqldb://{user}:{passwd}@{host}:{port}/{db}?charset={charset}".format(**db_config)
    sql_engine = create_engine(db_uri)
    global session, cursor, db
    session = sessionmaker(bind=sql_engine)()
    db = MySQLdb.connect(**db_config)
    cursor = db.cursor()



def update(table_name, row_info, filter_key):
    update_sentence = ', '.join(["{}='{}'".format(k, row_info[k]) for k in row_info if k not in filter_key])
    where_sentence = ' AND '.join(["{}='{}'".format(k, row_info[k]) for k in filter_key])
    sql = """update {table_name} set {update_sentence} where {where_sentence}""".format(
            table_name=table_name,
            update_sentence=update_sentence,
            where_sentence=where_sentence,
        )
    logging.debug(sql)
    logging.debug(cursor.execute(sql))
    db.commit()


def insert(table_name, row_info, unique_key=None):
    if unique_key:
        filter_info = {key: row_info[key] for key in unique_key}
        if select(table_name, unique_key, filter_info, limit=1):
            logging.debug('DUMPLICA insert table %s vale %s', table_name, row_info)
            update(table_name, row_info, unique_key)
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
    logging.debug(cursor.execute(sql, values))
    db.commit()


def select(table_name, query_list, filter_info=None, limit=None):
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
    cursor.execute(sql)
    return cursor.fetchall()
