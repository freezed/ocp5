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
    CLI_MSG_SUBST, CLI_MSG_NO_SUBST, CLI_MSG_CAT, CLI_MSG_CHOOSEN_PROD, \
    CLI_MSG_DETAILLED_SUB, CLI_MAX_LEN, \
    CLI_ITEM_LIST, CLI_MSG_ASK_BAK, CLI_MSG_BAK_DONE, CLI_MSG_INIT_MENU,\
    CLI_MSG_SUBST_HEAD, CLI_MSG_SUBST_TITLE, CLI_MSG_SUBST_LIST

product_asked = {'valid_item': False}
cli_end_msg = CLI_MSG_QUIT


def ask_user(head_msg, item_list):
    """
    Ask user to choose an item in the provided list, using numeric index

    :head_msg:  Text displayed in header
    :item_list: Dict() containing all data about item (see `get_data_list()`)

    :result:
        - item:
        - cli_end_msg:
        - valid_item:
    """
    valid_input = False
    foot_msg = ""

    while valid_input is False:
        system('clear')
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

                # Response not in range, re-ask
                else:
                    foot_msg += CLI_MSG_ASK_ERR.format(user_input)
    return {
        'item': item,
        'cli_end_msg': foot_msg,
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
    results_list = [(idx, val['name'], val['option'], val['id'])
                    for idx, val in enumerate(db_obj.result)]

    # Hacky results-split for rendering in 2 columns
    res_even = [(
        idx,
        val['name'][:CLI_MAX_LEN].ljust(CLI_MAX_LEN),
        val['option'], val['id']
    ) for idx, val in enumerate(db_obj.result) if idx % 2 == 0]

    res_uneven = [(
        idx,
        val['name'][:CLI_MAX_LEN],
        val['option'],
        val['id']
    ) for idx, val in enumerate(db_obj.result) if idx % 2 != 0]

    # category list
    results_txt = ""

    if len(res_uneven) == 0 and len(res_even) > 0:
        results_txt += "{} : {}\n".format(
            res_even[0][0],
            res_even[0][1]
        )

    else:
        for num, unused in enumerate(res_uneven):
            results_txt += CLI_ITEM_LIST.format(
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


def start_init_menu():
    """ Ask for saved substitution or searching new one """
    LOCAL_DB.execute(DB_REQUEST['list_substituated_prod'])

    if LOCAL_DB.cursor.rowcount > 0:
        menu_list = {
            'results_txt': CLI_MSG_INIT_MENU,
            'results_list': [False, True],
            'max_id': 1
        }

        # Ask for saved list or search new one
        menu_asked = ask_user(
            CLI_MSG_DISCLAIMER,
            menu_list
        )

        # Shows saved list
        if menu_asked['valid_item'] and menu_asked['item']:
            cli_msg_subst_recap = CLI_MSG_SUBST_TITLE + CLI_MSG_SUBST_HEAD

            for row in LOCAL_DB.result:
                cli_msg_subst_recap += CLI_MSG_SUBST_LIST.format(
                    pname=row['pname'][:CLI_MAX_LEN].center(CLI_MAX_LEN),
                    sname=row['sname'][:CLI_MAX_LEN].center(CLI_MAX_LEN),
                )
            return (True, cli_msg_subst_recap)

        return (False, "")

    return (False, "Pas de substitutions enregistée")


# Starts a DB connection
LOCAL_DB = Db()

################
# INITIAL MENU #
################
init_menu = start_init_menu()

#############################
# LISTS SAVED SUBSTITUTIONS #
#############################
if init_menu[0]:
    cli_end_msg = init_menu[1]

####################
# LISTS CATEGORIES #
####################
else:
    category_list = get_data_list(
        LOCAL_DB,
        DB_REQUEST['list_cat']
    )

    head_msg = CLI_MSG_DISCLAIMER
    head_msg += init_menu[1]
    head_msg += CLI_MSG_CAT

    # Asks the user to select a category
    category_asked = ask_user(
        head_msg,
        category_list
    )

    ##################
    # LISTS PRODUCTS #
    ##################
    if category_asked['valid_item']:
        product_list = get_data_list(
            LOCAL_DB,
            DB_REQUEST['list_prod'].format(category_asked['item'][3])
        )

        head_msg = CLI_MSG_DISCLAIMER
        head_msg += CLI_MSG_CHOOSEN_CAT.format(category_asked['item'][1])
        head_msg += CLI_MSG_PROD

        # Asks the user to select a product
        product_asked = ask_user(
            head_msg,
            product_list
        )

    ####################
    # LISTS SUBTITUTES #
    ####################
    if product_asked['valid_item']:
        substitute_list = get_data_list(
            LOCAL_DB,
            DB_REQUEST['list_substitute'].format(
                category_asked['item'][3],
                product_asked['item'][2]
            )
        )

        head_msg = CLI_MSG_DISCLAIMER
        head_msg += CLI_MSG_CHOOSEN_CAT.format(category_asked['item'][1])
        head_msg += CLI_MSG_CHOOSEN_PROD.format(product_asked['item'][1])
        head_msg += CLI_MSG_SUBST

        # No substitute found
        if substitute_list['max_id'] == -1:
            cli_end_msg = CLI_MSG_NO_SUBST.format(
                product_asked['item'][1],
                product_asked['item'][2]
            )

        # Asks the user to select a substitute
        elif substitute_list['max_id'] >= 0:
            substit_asked = ask_user(
                head_msg,
                substitute_list
            )

            ##########################
            # SHOW SUBTITUTE DETAILS #
            ##########################
            if substit_asked['valid_item']:
                LOCAL_DB.execute(DB_REQUEST['select_substitute'].format(
                    substit_asked['item'][3]
                ))

                head_msg = CLI_MSG_DISCLAIMER +\
                    CLI_MSG_CHOOSEN_CAT.format(substit_asked['item'][1])

                backup_list = {
                    'results_txt': CLI_MSG_DETAILLED_SUB.format(
                        code=LOCAL_DB.result[0]['code'],
                        nutri=LOCAL_DB.result[0]['nutrition_grades'],
                        url=LOCAL_DB.result[0]['url']
                    ) + CLI_MSG_ASK_BAK.format(
                        substit_asked['item'][1],
                        product_asked['item'][1]
                    ),
                    'results_list': [False, True],
                    'max_id': 1
                }

                # Saves if user choose it
                backup_asked = ask_user(
                    head_msg,
                    backup_list
                )

                if backup_asked['valid_item'] and backup_asked['item']:
                    LOCAL_DB.execute(DB_REQUEST['save_substitute'].format(
                        substit_asked['item'][3],
                        product_asked['item'][3]
                    ))

                    if LOCAL_DB.cursor.rowcount == 1:
                        cli_end_msg = CLI_MSG_BAK_DONE

print(cli_end_msg)
