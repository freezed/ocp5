#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-08-04
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

    Command line interface to interact with local DB

Choose a product in a list of aivaiable categories['results_list'],
the system gives you an alternative with a better 'nutriscore'.
You can save this product to get it later.

 """
from os import system
from db import Db
from config import DB_REQUEST, CLI_MSG_DISCLAIMER, CLI_MSG_ASK_IDX, \
    CLI_MSG_ASK_ERR, CLI_MSG_QUIT, CLI_MSG_CHOOSEN_CAT, CLI_MSG_PROD, \
    CLI_MSG_PROD, CLI_MSG_SUBST, CLI_MSG_NO_SUBST
cli_msg = str()

product_asked = {'valid_item': False}


def ask_user(head_msg, foot_msg, item_list, db_obj=None):
    """
    Ask user to choose an item in the provided list, using numeric index

    :head_msg:  Text displayed in header
    :foot_msg:  Text displayed in footer
    :item_list: Dict() containing all data about item (see `get_data_list()`)
    :db_obj:        Database object (optionnal)

    :result:
        - item:
        - cli_msg:
        - valid_item:
    """
    valid_input = False

    if db_obj is not None:
        db_msg = db_obj.message
    else:
        db_msg = ""

    while valid_input is False:
        system('clear')
        print(db_msg)
        print(head_msg)
        print(item_list['results_txt'])
        print(foot_msg)

        user_input = input(CLI_MSG_ASK_IDX.format(item_list['max_id']))

        if user_input.lower() == "q":
            valid_input = True
            valid_item = False
            item = ""

        else:
            try:
                user_input = int(user_input)

            # Response not int(), re-ask
            except ValueError:
                foot_msg += CLI_MSG_ASK_ERR.format(user_input)

            else:
                # Response is valid
                if user_input <= item_list['max_id']:
                    valid_input = True
                    valid_item = True
                    item = item_list['results_list'][user_input]
                    foot_msg = CLI_MSG_CHOOSEN_CAT.format(item[1])

                # Response not in range, re-ask
                else:
                    foot_msg += CLI_MSG_ASK_ERR.format(user_input)
    return {
        'item': item,
        'cli_msg': foot_msg,
        'valid_item': valid_item
    }


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
    results_list = [(idx, val['name'], val['option'])
                    for idx, val in enumerate(db_obj.result)]

    # Hacky results-split for rendering in 2 columns
    res_even = [(idx, val['name'], val['option'])
                for idx, val in enumerate(db_obj.result) if idx % 2 == 0]
    res_uneven = [(idx, val['name'], val['option'])
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

####################
# LISTS CATEGORIES #
####################
category_list = get_data_list(
    LOCAL_DB,
    DB_REQUEST['list_cat']
)

# Asks the user to select a category
category_asked = ask_user(
    CLI_MSG_DISCLAIMER,
    "WTF0",     # cli_msg
    category_list,
    LOCAL_DB
)

##################
# LISTS PRODUCTS #
##################
if category_asked['valid_item']:
    product_list = get_data_list(
        LOCAL_DB, DB_REQUEST['list_prod'].format(category_asked['item'][1])
    )
    CLI_MSG_PROD = CLI_MSG_CHOOSEN_CAT.format(category_asked['item'][1]) \
        + CLI_MSG_PROD

    # Asks the user to select a product
    product_asked = ask_user(
        CLI_MSG_PROD,
        "WTF1",    # cli_msg
        product_list
    )

####################
# LISTS SUBTITUTES #
####################
if product_asked['valid_item']:
    substitute_list = get_data_list(
        LOCAL_DB,
        DB_REQUEST['list_substitute'].format(
            category_asked['item'][1],
            product_asked['item'][2]
        )
    )

    # No substitute found
    if substitute_list['max_id'] == -1:
        cli_msg = CLI_MSG_NO_SUBST.format(
            product_asked['item'][1],
            product_asked['item'][2]
        )

    # Shows product in the same category with a lowest nutriscore
    elif substitute_list['max_id'] > 0:
        substitute_asked = ask_user(
            CLI_MSG_SUBST,
            "WTF2",
            substitute_list
        )

        if substitute_asked['valid_item']:
            cli_msg = "cli_msg : «{}»\n\n".format(cli_msg)
            cli_msg += "category : «{}»\n\n".format(category_asked['item'][1])
            cli_msg += "product : «{}»\n\n".format(product_asked['item'][1])
            cli_msg += "substitut : «{}»".format(substitute_asked['item'][1])

            # Asks the user to select a substitute

            # Saves if user choose it

else:
    cli_msg = CLI_MSG_QUIT

print(cli_msg)
