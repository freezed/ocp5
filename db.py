#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-26
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Connect to DB
 """

import pymysql.cursors

# CONFIG
CONFIG = {
    'host': 'localhost',
    'user': 'loff',
    'pass': 'loff',
    'db': 'loff',
    'char': 'utf8',
    'file': 'create-db-loff.sql'
}
DB_NOT_FOUND = True


# FUNCTION
def sql_create_db(filename=CONFIG['file']):
    """
    Get the SQL instruction to create the DB for file

    :return: a list of each SQL query whithout the trailing ";"

    :Tests:
    >>> sql_create_db('wronq_file.sql')
    File load error : wronq_file.sql
    False
    """
    from os import path

    # Loading file
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


# WORK
# Connect to the database
CONNECTION = pymysql.connect(host=CONFIG['host'],
                             user=CONFIG['user'],
                             password=CONFIG['pass'],
                             charset=CONFIG['char'],
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with CONNECTION.cursor() as cursor:
        # Show DB
        cursor.execute("SHOW DATABASES")
        db_list = cursor.fetchall()

        for idx, val in enumerate(db_list):

            if CONFIG['db'] in db_list[idx].values():
                DB_NOT_FOUND = False
                cursor.execute("USE {}".format(CONFIG['db']))
                print('DB exist : ready to use it.')

        # No DB, create it
        if DB_NOT_FOUND:
            request_list = sql_create_db()

            if request_list is not False:

                for idx, sql_request in enumerate(request_list):
                    # print(sql_request + ';')
                    print("-- REQUEST #{} : --{}".format(idx, sql_request))
                    cursor.execute(sql_request + ';')

except pymysql.err.OperationalError as except_detail:
    print("DB error: «{}»".format(except_detail))

finally:
    CONNECTION.close()


if __name__ == "__main__":
    """ Running doctests """
    import doctest
    doctest.testmod()
