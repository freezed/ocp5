#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-26
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Connects DB, executes SQL statements
"""

import pymysql.cursors
from config import DB_CONFIG


class Db():
    """
    Class doc

    :Test:
    >>> test = Db()
    >>> print(test.message)
    DB «loff» contains these tables :['category', 'product']
    DB size : n.n MB
    Table 'product' has «n» row(s)
    Table 'category' has «n» row(s)
    """

    def __init__(self):
        """
        Class initialiser
        """
        MSG_TEMPLATE = {
            "request": "-- REQUEST #{} : --{}",
            "database": "DB «{}» contains these tables :",
            "tables": "{}\n",
            "dashboard": "DB size : {dbsize}\nTable 'product' has «{rowprod}» "
                         "row(s)\nTable 'category' has «{rowcat}» row(s)"
        }
        db_not_found = True
        self.message = ""
        self.result = list()

        # MYSQL server connexion, without DB selection
        self.cnx()

        self.cursor.execute("SHOW DATABASES")
        db_list = self.cursor.fetchall()

        for idx, unused in enumerate(db_list):

            if DB_CONFIG['db'] in db_list[idx].values():
                db_not_found = False

                self.cursor.execute("USE {}".format(DB_CONFIG['db']))

                self.cursor.execute("SHOW TABLES")
                tbl_list = self.cursor.fetchall()

                # Get size information on DB
                self.cursor.execute("""
                SELECT table_schema "Full database",
                    CONCAT(
                        ROUND(
                            SUM(data_length + index_length)
                        / 1024 / 1024, 1),
                    " MB") "dbsize"
                FROM information_schema.tables
                WHERE table_schema = "loff"
                GROUP BY table_schema

                UNION

                SELECT "Rows in 'product' table", COUNT(*)
                FROM product

                UNION

                SELECT "Rows in 'category' table", COUNT(*)
                FROM category;
                """)
                dashboard = self.cursor.fetchall()

                # Constructs DB information message
                self.message = MSG_TEMPLATE['database'].format(
                    dashboard[0]['Full database'])

                self.message += MSG_TEMPLATE['tables'].format(
                    [val['Tables_in_loff'] for val in tbl_list])

                self.message += MSG_TEMPLATE['dashboard'].format(
                    dbsize=dashboard[0]['dbsize'].decode("utf-8"),
                    rowprod=dashboard[1]['dbsize'].decode("utf-8"),
                    rowcat=dashboard[2]['dbsize'].decode("utf-8"))

        # No DB, create it
        if db_not_found:
            request_list = self.get_sql_from_file()

            if request_list is not False:

                for idx, sql_request in enumerate(request_list):
                    self.message = MSG_TEMPLATE['request'].format(
                        idx, sql_request)
                    self.cursor.execute(sql_request + ';')

    def cnx(self, with_db=False):
        """ Connect to DB """
        conf = {
            'host': DB_CONFIG['host'],
            'user': DB_CONFIG['user'],
            'password': DB_CONFIG['password'],
            'charset': DB_CONFIG['charset'],
            'cursorclass': pymysql.cursors.DictCursor
        }

        if with_db:
            conf['db'] = DB_CONFIG['db']

        self.cursor = pymysql.connect(**conf).cursor()

    def get_sql_from_file(self, filename=DB_CONFIG['file']):
        """
        Get the SQL instruction from a file

        :return: a list of each SQL query whithout the trailing ";"

        :Tests:
        >>> Db.get_sql_from_file(Db, 'wronq_file.sql')
        False
        >>> Db.message
        'File load error : wronq_file.sql'
        """
        from os import path

        # File did not exists
        if path.isfile(filename) is False:
            self.message = "File load error : {}".format(filename)
            return False

        else:
            with open(filename, "r") as sql_file:
                # Split file in list
                ret = sql_file.read().split(';')
                # drop last empty entry
                ret.pop()
                return ret

    def __del__(self):
        """ Object destruction"""
        self.cursor.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
