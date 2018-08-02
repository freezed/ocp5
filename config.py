#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-27
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of [ocp5](https://github.com/freezed/ocp5) project
"""

# DATABASE
DB_CONFIG = {
    'host': 'localhost',
    'user': 'loff',
    'password': 'loff',
    'db': 'loff',
    'charset': 'utf8',
    'file': 'create-db-loff.sql'
}

DB_MSG_TEMPLATE = {
    "database": "DB «{}» contains these tables :",
    "db_created": "DB «{}» created\n\n",
    "tables": "{}\n",
    "dashboard": "DB size : {dbsize}\nTable 'product' has «{rowprod}» "
                 "row(s)\nTable 'category' has «{rowcat}» row(s)"
}

# API
FIELD_KEPT = {
    'product': [
        'product_name',
        'nutrition_grades',
        'categories_tags'
    ],
    'category': [
        '_id',
        'url',
        'product_name',
        'nutrition_grades',
        'categories_tags'
    ]
}
