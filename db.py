#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-26
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Connect to DB
 """

import pymysql.cursors
from config import DB_CONFIG


class Db():
    """
    Class doc

    :Test:
    >>> test = Db()
    >>> print(test.message)
    DB «localhost» exist, using it
    """

    def __init__(self):
        """
        Class initialiser
        """
        self.DB_NOT_FOUND = True
        self.MSG = {
            "request": "-- REQUEST #{} : --{}",
            "database": "DB «{}» exist, using it"}
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
                        DB_NOT_FOUND = False
                        cursor.execute("USE {}".format(DB_CONFIG['db']))
                        self.message = self.MSG['database'].format(
                            DB_CONFIG['host'])

                # No DB, create it
                if DB_NOT_FOUND:
                    request_list = self.get_sql_from_file()

                    if request_list is not False:

                        for idx, sql_request in enumerate(request_list):
                            self.message = self.MSG['request'].format(
                                idx, sql_request)
                            cursor.execute(sql_request + ';')

        except pymysql.err.OperationalError as except_detail:
            print("DB error: «{}»".format(except_detail))

    @staticmethod
    def get_sql_from_file(filename=DB_CONFIG['file']):
        """
        Get the SQL instruction from a file

        :return: a list of each SQL query whithout the trailing ";"

        :Tests:
        >>> Db.get_sql_from_file('wronq_file.sql')
        File load error : wronq_file.sql
        False
        """
        from os import path

        # File did not exists
        if path.isfile(filename) is False:
            print("File load error : {}".format(filename))
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
    """ Running doctests """
    import doctest
    doctest.testmod()
