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


def get_data_list(db_obj, sql):
    """
    Gets data from DB & return them formated as a text list displayable on CLI

    :db_obj: a database object [PyMySQL]
    :sql: a SQL query

    :Return: a dict containing details on requested data:
        - max_id: maximum ID
        - results_list: stored in a list of tuple (id, name, count)
        - results_txt: in a string, text-formated
    """

    db_obj.execute(sql)
    max_id = int(db_obj.cursor.rowcount - 1)
    results_list = [(idx, val['name'], val['COUNT(*)'])
                    for idx, val in enumerate(db_obj.result)]

    # Hacky results-split for rendering in 2 columns
    res_even = [(idx, val['name'], val['COUNT(*)'])
                for idx, val in enumerate(db_obj.result) if idx % 2 == 0]
    res_uneven = [(idx, val['name'], val['COUNT(*)'])
                  for idx, val in enumerate(db_obj.result) if idx % 2 != 0]
    # category list
    results_txt = ""
    for num, unused in enumerate(res_uneven):
        results_txt += "{} : {} \t\t {} : {}\n".format(
            res_even[num][0],
            res_even[num][1],
            res_uneven[num][0],
            res_uneven[num][1]
        )

    if len(res_uneven) < len(res_even):
        num += 1
        results_txt += "{} : {}\n".format(
            res_even[num][0],
            res_even[num][1]
        )

    return {
        'max_id': max_id,
        'results_list': results_list,
        'results_txt': results_txt
    }


# Starts a DB connection
LOCAL_DB = Db()

# category list
categories = get_data_list(LOCAL_DB, DB_REQUEST['list_cat'])
CAT_MAX_ID = categories['max_id']
CATEGORIES = categories['results_list']
CAT_TXT_LIST = categories['results_txt']

# Prompts it with an index
# Asks the user to enter the index of the selected category
while valid_category is False:
    system('clear')
    print(LOCAL_DB.message)
    print(CLI_MSG_DISCLAIMER)
    print(CAT_TXT_LIST)
    print(cli_msg)

    RESPONSE = input(CLI_MSG_ASK_CAT.format(CAT_MAX_ID))

    if RESPONSE.lower() == "q":
        valid_category = True
        cli_msg = CLI_MSG_QUIT

    else:
        try:
            RESPONSE = int(RESPONSE)

        # Response not int(), re-ask
        except ValueError:
            cli_msg += CLI_MSG_ASK_ERR.format(RESPONSE)
            # pass

        else:
            # Response is valid
            if RESPONSE <= CAT_MAX_ID:
                valid_category = True
                category = CATEGORIES[RESPONSE]
                cli_msg = CLI_MSG_CHOOSEN_CAT.format(category[1])

            # Response not in range, re-ask
            else:
                cli_msg += CLI_MSG_ASK_ERR.format(RESPONSE)

# Lists all products

# Asks the user to enter the index of the selected product

    # If index is not valid, re-ask

# Shows the 1st product in the same category with the lowest nutriscore

# Saves if user choose it

print(cli_msg)
