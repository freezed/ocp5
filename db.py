#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-26
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Connect to DB
 """

import pymysql.cursors

CONFIG = {
    'host': 'localhost',
    'user': 'loff',
    'pass': 'loff',
    'db': 'loff',
    'char': 'utf8'
}


# Connect to the database
connection = pymysql.connect(host=CONFIG['host'],
                             user=CONFIG['user'],
                             password=CONFIG['pass'],
                             database=CONFIG['db'],
                             charset=CONFIG['char'],
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Show DB
        cursor.execute("SHOW DATABASES")
        db_list  = cursor.fetchall()

        for line in range(len(db_list)):

            if CONFIG['db'] in db_list[line].values():
                # DB found
                cursor.execute("USE {}".format(CONFIG['db']))

            # else:
                # Create DB
                # cursor.execute(create_db)

except pymysql.err.OperationalError as except_detail:
    print("DB error: «{}»".format(except_detail))

finally:
    connection.close()

def function():
    """
    Function documentation

    :Tests:
    >>> a = 10
    >>> a + 5
    15
    """


if __name__ == "__main__":
    """ Running doctests """
    import doctest
    doctest.testmod()
