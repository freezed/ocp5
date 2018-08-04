#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-04
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

    Command line interface to interact with local DB

Choose a product in the list of aivaiable categories, the system gives you an
alternative with a better 'nutriscore'.
You can save this product to get it later.

 """
from os import system
from db import Db
from config import DB_REQUEST, CLI_MSG_DISCLAIMER, CLI_MSG_ASK_CAT

# Starts a DB connection
local_db = Db()
# print(local_db.message)

# Gets category list
local_db.execute(DB_REQUEST['list_cat'])

# Hacky result split for rendering in 2 columns
results_1 = [(idx, val['name'], val['COUNT(*)']) for idx, val in enumerate(local_db.result) if idx%2 != 0]
results_2 = [(idx, val['name'], val['COUNT(*)']) for idx, val in enumerate(local_db.result) if idx%2 == 0]

cli_msg = str()
for num, row in enumerate(results_1):
    cli_msg += "{} : {} \t\t {} : {}\n".format(
        results_2[num][0],
        results_2[num][1],
        row[0],
        row[1]
    )


# Prompts it with an index
system('clear')
print(CLI_MSG_DISCLAIMER)
print(cli_msg)

# Asks the user to enter the index of the selected category
input(CLI_MSG_ASK_CAT)


    # If index is not valid, re-ask

# Lists all products

# Asks the user to enter the index of the selected product

    # If index is not valid, re-ask

# Shows the 1st product in the same category with the lowest nutriscore

# Saves if user choose it
