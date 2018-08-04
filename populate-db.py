#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-02
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Populates local DB with data comming from OpenFF API

:Tests:
>>> CATEGORY_LIST.append('falsecategory')

"""
from random import choice
from os import system
import pymysql
from db import Db
from function import get_category, sql_generator
from config import DB_CONFIG, POP_MSG_TEMPLATE, CATEGORY_LIST

system('clear')
local_db = Db()
print(local_db.message)

for category in CATEGORY_LIST:

    print(POP_MSG_TEMPLATE['work'].format(category))
    print(POP_MSG_TEMPLATE['fetch'])

    # get data (one page each, TODO multipage)
    staging_data = get_category(category)

    # generate SQL
    sql_list = sql_generator(staging_data)

    # execute SQL
    print(POP_MSG_TEMPLATE['insert'].format(category))

    if sql_list is False:
        print(POP_MSG_TEMPLATE['missing'].format(category))

    else:
        for idx, sql in enumerate(sql_list):

            try:
                response = local_db.cursor.execute(sql)

            # For warnings, do not catch "Data truncated…" as expected
            except pymysql.err.Warning as except_detail:
                response = "Warning: «{}»".format(except_detail)

            # Duplicate entry
            except pymysql.err.IntegrityError as except_detail:
                response = "0, {}".format(except_detail)

            except pymysql.err.ProgrammingError as except_detail:
                response = "ProgrammingError: «{}»".format(except_detail)

            except pymysql.err.MySQLError as except_detail:
                response = "MySQLError: «{}»".format(except_detail)

            print("\t{}. [{}…] | Affected rows : «{}»".format(idx, sql[87:100], response))
