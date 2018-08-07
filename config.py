#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-27
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

This file is part of [ocp5](https://github.com/freezed/ocp5) project
"""

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

# CLI
DB_REQUEST = {
    'list_cat': "SELECT c.name, COUNT(*) AS 'option', c.id AS 'id' FROM category AS c JOIN product AS p ON p.category_id = c.id GROUP BY c.name ORDER BY COUNT(*) DESC;",
    'list_prod': "SELECT p.name, p.nutrition_grades AS 'option', p.id AS 'id' FROM product AS p LEFT JOIN category AS c ON p.category_id = c.id WHERE c.id = '{}' AND p.nutrition_grades IS NOT NULL;",
    'list_substitute': "SELECT p.name, p.nutrition_grades AS 'option', p.id AS 'id' FROM product AS p LEFT JOIN category AS c ON p.category_id = c.id WHERE c.id = '{}' AND p.nutrition_grades < '{}'",
    'select_substitute': "SELECT p.*, c.name FROM product AS p LEFT JOIN category AS c ON p.category_id = c.id WHERE p.id = '{}'",
    'save_substitute': "UPDATE product SET substitute_id={} WHERE id={}",
}

CLI_MSG_DISCLAIMER = "# # # Bienvenu sur le terminal # # #\n\n"
CLI_MSG_CAT = "Catégories disponibles :\n"
CLI_MSG_PROD = "Produits disponibles :\n"
CLI_MSG_SUBST = "Substituts disponibles :\n"
CLI_MSG_ASK_IDX = "Index choisi [0-{}] («Q»uitter) :"
CLI_MSG_ASK_BAK = "Voulez vous sauvegarder «{}» en substitut du produit «{}»?"\
    " [O/N]\n(«Q» pour quitter): "

CLI_MSG_CHOOSEN_CAT = "# # Categorie : [ {} ]\n"
CLI_MSG_CHOOSEN_PROD = "# Produits : [ {} ]\n"
CLI_MSG_CHOOSEN_SUBST = "Fiche complète du substitut : [ {} ]\n"
CLI_MSG_DETAILLED_SUB = "Nutriscore [ {nutri} ]\tCode [ {code} ]"\
    "\nURL:{url}"

CLI_MSG_NO_SUBST = "Pas de substitut trouvé pour le produit «{}» (nutriscore : «{}»)"
CLI_MSG_ASK_ERR = "\nSaisie incorrecte : «{}»"
CLI_MSG_QUIT = "\nAu revoir!"
#CLI_ITEM_MAX_LEN = 15

# DATABASE
DB_CONFIG = {
    'host': 'localhost',
    'user': 'loff',
    'password': 'loff',
    'db': 'loff',
    'charset': 'utf8',
    'autocommit': True,
    'file': 'create-db-loff.sql'
}

DB_MSG_TEMPLATE = {
    "database": "DB «{}» contains these tables :",
    "db_created": "DB «{}» created\n\n",
    "tables": "{}\n",
    "dashboard": "DB size : {dbsize}\nTable 'product' has «{rowprod}» "
                 "row(s)\nTable 'category' has «{rowcat}» row(s)"
}

# POPULATE
POP_MSG_TEMPLATE = {
    'work': '\n# # # # # #\tC A T E G O R Y --[ {} ]--',
    'fetch': '\tFetching data over API…',
    'insert': '\tInserting data into DB…',
    'missing': '\t/!\\ [ {} ] do not exists /!\\',
    # '': '',
}

CATEGORY_LIST = [
    'ail',
    'bio',
    'blés',
    'roti',
    'edam',
    'kits',
    'farces',
    'bars',
    'insectes'
]
