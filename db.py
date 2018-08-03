#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-26
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Connects DB, executes SQL statements
"""

import pymysql.cursors
from config import DB_CONFIG, DB_MSG_TEMPLATE


class Db():
    """
    Manage DB class

    :Tests:
    >>> expect = ["DB «loff» contains these tables :['category', 'product']",\
"DB «loff» created"]

    >>> class_test = Db()
    >>> class_test.message.splitlines()[0] in expect
    True
    """

    def __init__(self):
        """ Class initialiser """
        self.message = ""
        self.result = list()

        # MYSQL server connexion, without DB selection
        self.start_connexion(False)

        first_summary_run = self.db_summary()
        # No DB, create it
        if first_summary_run is False:
            request_list = self.get_sql_from_file()

            if request_list is not False:

                for sql_request in request_list:
                    self.cursor.execute(sql_request + ';')

                self.message = DB_MSG_TEMPLATE['db_created'].format(
                    DB_CONFIG['db']
                )

                second_summary_run = self.db_summary()

                if second_summary_run is False:
                    print('DB unknown error')

                else:
                    self.message += second_summary_run

        else:
            self.message = first_summary_run

    def db_summary(self):
        """
        Search DB, SHOW TABLES, get DB size and count rows in tables

        :return: False if DB not found, nothing otherwise (but sets messages)

        :Tests:
        >>> expect = ["DB «loff» contains these tables \
:['category', 'product']","DB «loff» created"]

        >>> Db.start_connexion(Db, with_db=False)
        >>> Db.db_summary(Db).splitlines()[0] in expect
        True
        """
        db_not_found = True
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
                summary = DB_MSG_TEMPLATE['database'].format(
                    dashboard[0]['Full database'])

                summary += DB_MSG_TEMPLATE['tables'].format(
                    [val['Tables_in_loff'] for val in tbl_list])

                summary += DB_MSG_TEMPLATE['dashboard'].format(
                    dbsize=dashboard[0]['dbsize'].decode("utf-8"),
                    rowprod=dashboard[1]['dbsize'].decode("utf-8"),
                    rowcat=dashboard[2]['dbsize'].decode("utf-8"))

        if db_not_found:
            return False

        else:
            return summary

    def execute(self, sql_request):
        """
        Executes a request on DB

        :Tests:
        >>> Db.start_connexion(Db, with_db=True)
        >>> Db.execute(Db, 'SHOW TABLES')
        2
        >>> Db.result == [{'Tables_in_loff': 'category'}, \
{'Tables_in_loff': 'product'}]
        True
        """
        # Connect to the database
        self.start_connexion(self)

        response = self.cursor.execute(sql_request)
        self.result = self.cursor.fetchall()
        return response

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

    def start_connexion(self, with_db=True):
        """
        Connect to MySQL Server

        :Tests:
        >>> DB_CONFIG['user'] = 'bob'
        >>> Db.start_connexion(Db, with_db=True)
        OperationalError: «(1045, "Access denied for user 'bob'@'localhost' \
(using password: YES)")»

        >>> DB_CONFIG['user'] = 'loff'
        >>> DB_CONFIG['db'] = 'foobar'
        >>> Db.start_connexion(Db, with_db=True)
        OperationalError: «(1044, "Access denied for user 'loff'@'localhost' \
to database 'foobar'")»

        """
        cnx_conf = {
            'host': DB_CONFIG['host'],
            'user': DB_CONFIG['user'],
            'password': DB_CONFIG['password'],
            'charset': DB_CONFIG['charset'],
            'autocommit': DB_CONFIG['autocommit'],
            'cursorclass': pymysql.cursors.DictCursor
        }

        if with_db:
            cnx_conf['db'] = DB_CONFIG['db']

        try:
            self.cnx = pymysql.connect(**cnx_conf)
            self.cursor = self.cnx.cursor()

        # For "Access denied" errors
        except pymysql.err.OperationalError as except_detail:
            print("OperationalError: «{}»".format(except_detail))

    def __del__(self):
        """ Object destruction"""
        self.cursor.close()
        self.cnx.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
