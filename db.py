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
    DB size : 0.1 MB
    Table 'product' has «0» row(s)
    Table 'category' has «0» row(s)
    """

    def __init__(self):
        """
        Class initialiser
        """
        self.DB_NOT_FOUND = True
        self.MSG = {
            "request": "-- REQUEST #{} : --{}",
            "database": "DB «{}» contains these tables :",
            "tables": "{}\n",
            "dashboard": "DB size : {dbsize}\nTable 'product' has «{rowprod}» "
                         "row(s)\nTable 'category' has «{rowcat}» row(s)"
        }
        self.message = ""

        # Connect to the database
        self.connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['pass'],
            charset=DB_CONFIG['char'],
            cursorclass=pymysql.cursors.DictCursor)

        try:
            with self.connection.cursor() as cursor:
                # Show DB
                cursor.execute("SHOW DATABASES")
                db_list = cursor.fetchall()

                for idx, unused in enumerate(db_list):

                    if DB_CONFIG['db'] in db_list[idx].values():
                        self.DB_NOT_FOUND = False

                        cursor.execute("USE {}".format(DB_CONFIG['db']))

                        cursor.execute("SHOW TABLES")
                        tbl_list = cursor.fetchall()

                        # Get size information on DB
                        # TODO : extract DB & tables names from code
                        cursor.execute("""
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
                        dashboard = cursor.fetchall()

                        # Constructs DB information message
                        self.message = self.MSG['database'].format(
                            dashboard[0]['Full database'])

                        self.message += self.MSG['tables'].format(
                            [val['Tables_in_loff'] for val in tbl_list])

                        self.message += self.MSG['dashboard'].format(
                            dbsize=dashboard[0]['dbsize'].decode("utf-8"),
                            rowprod=dashboard[1]['dbsize'].decode("utf-8"),
                            rowcat=dashboard[2]['dbsize'].decode("utf-8"))

                # No DB, create it
                if self.DB_NOT_FOUND:
                    request_list = self.get_sql_from_file()

                    if request_list is not False:

                        for idx, sql_request in enumerate(request_list):
                            self.message = self.MSG['request'].format(
                                idx, sql_request)
                            cursor.execute(sql_request + ';')

        except pymysql.err.OperationalError as except_detail:
            print("DB error: «{}»".format(except_detail))

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
        self.connection.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
