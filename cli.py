#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-04
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

    Command line interface to interact with local DB

Choose a product in a list of aivaiable CATEGORIES, the system gives you an
alternative with a better 'nutriscore'.
You can save this product to get it later.

 """
from os import system
from db import Db
from config import DB_REQUEST, CLI_MSG_DISCLAIMER, CLI_MSG_ASK_CAT, \
    CLI_MSG_ASK_ERR, CLI_MSG_QUIT, CLI_MSG_CHOOSEN_CAT

valid_category = False
cli_msg = str()

# Starts a DB connection
LOCAL_DB = Db()
# print(LOCAL_DB.message)

# Gets category list
LOCAL_DB.execute(DB_REQUEST['list_cat'])
IDX_MAX = int(LOCAL_DB.cursor.rowcount - 1)
CATEGORIES = [(idx, val['name'], val['COUNT(*)'])
              for idx, val in enumerate(LOCAL_DB.result)]

# Hacky results-split for rendering in 2 columns
RES_EVEN = [(idx, val['name'], val['COUNT(*)'])
            for idx, val in enumerate(LOCAL_DB.result) if idx % 2 == 0]
RES_UNEVEN = [(idx, val['name'], val['COUNT(*)'])
              for idx, val in enumerate(LOCAL_DB.result) if idx % 2 != 0]

# category list
CLI_MSG_LIST = ""
for num, row in enumerate(RES_UNEVEN):
    CLI_MSG_LIST += "{} : {} \t\t {} : {}\n".format(
        RES_EVEN[num][0],
        RES_EVEN[num][1],
        RES_UNEVEN[num][0],
        RES_UNEVEN[num][1]
    )

if len(RES_UNEVEN) < len(RES_EVEN):
    num += 1
    CLI_MSG_LIST += "{} : {}\n".format(
        RES_EVEN[num][0],
        RES_EVEN[num][1]
    )

# Prompts it with an index
# Asks the user to enter the index of the selected category
while valid_category is False:
    system('clear')
    print(CLI_MSG_DISCLAIMER)
    print(CLI_MSG_LIST)
    print(cli_msg)

    response = input(CLI_MSG_ASK_CAT.format(IDX_MAX))

    if response.lower() == "q":
        valid_category = True
        cli_msg = CLI_MSG_QUIT

    else:
        try:
            response = int(response)

        # Response not int(), re-ask
        except ValueError:
            cli_msg += CLI_MSG_ASK_ERR.format(response)
            # pass

        else:
            # Response is valid
            if response <= IDX_MAX:
                valid_category = True
                category = CATEGORIES[response]
                cli_msg = CLI_MSG_CHOOSEN_CAT.format(category[1])

            # Response not in range, re-ask
            else:
                cli_msg += CLI_MSG_ASK_ERR.format(response)

# Lists all products

# Asks the user to enter the index of the selected product

    # If index is not valid, re-ask

# Shows the 1st product in the same category with the lowest nutriscore

# Saves if user choose it

print(cli_msg)
