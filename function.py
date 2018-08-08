#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: freezed <freezed@users.noreply.github.com> 2018-07-24
Version: 0.1
Licence: `GNU GPL v3` GNU GPL v3: http://www.gnu.org/licenses/

Call OpenFF API to populate a local MariaDB/MySQL database with product data
This DB will serve an CLI client which gives alternative products with better
nurition grade.
"""
import json
import requests
from config import FIELD_KEPT, API_URL_CAT


def get_product(code, from_file=False):
    """
    Call OpenFF API to get data of a single product

    :Tests ONLINE:
    # >>> prod_beurre = get_product('3017760000109')
    # >>> prod_oreo = get_product('8410000810004')

    # >>> prod_false is False
    # True

    # >>> prod_string is False
    # True

    :Tests OFFLINE:
    >>> prod_beurre = get_product('3017760000109', True)
    >>> prod_oreo = get_product('8410000810004', True)
    >>> prod_false = get_product('1664', True)
    File load error : sample/product-1664.json

    >>> prod_string = get_product('string', True)
    File load error : sample/product-string.json

    >>> print(prod_beurre['product_name'])
    Le Véritable Petit Beurre

    >>> print(prod_beurre['nutrition_grades'])
    e

    >>> print(prod_beurre['categories_tags'])
    ['en:sugary-snacks', 'en:biscuits-and-cakes', \
'en:biscuits', 'fr:petits-beurres']

    >>> print(prod_oreo['code'])
    8410000810004

    >>> print(prod_oreo['url'])
    https://fr.openfoodfacts.org/product/8410000810004/

    >>> print(prod_oreo['product_name'])
    Biscuit Oreo

    >>> print(prod_oreo['nutrition_grades'])
    e

    >>> print(prod_oreo['categories_tags'])
    ['en:sugary-snacks', 'en:biscuits-and-cakes', 'en:biscuits', \
'en:chocolate-biscuits', 'es:sandwich-cookies']
    """

    ERR_FILE = "File load error : {}"
    filename = 'sample/product-{}.json'.format(str(code))

    try:
        int(code)

    except ValueError:  # as except_detail:
        # print("Exception: «{}»".format(except_detail))
        print(ERR_FILE.format(filename))

    else:

        if from_file:
            from os import path

            # File did not exists
            if path.isfile(filename) is False:
                print(ERR_FILE.format(filename))
                status = 404
                product_json = {'status': 0}

            else:
                with open(filename, "r") as json_file:
                    product_json = json.loads(json_file.read())
                    status = 200

        else:

            response = requests.get(
                "https://fr.openfoodfacts.org/api/v0/product/{}.json".format(code)
            )
            product_json = json.loads(response.text)
            status = response.status_code

        if product_json['status'] and status == 200:
            product_kept = {
                'code': code,
                'url': "https://fr.openfoodfacts.org/product/{}/".format(code)
            }

            for field in FIELD_KEPT['product']:
                product_kept[field] = product_json['product'][field]

            return product_kept

        else:
            return False


def get_category(name, from_file=False):
    """
    Call OpenFF API to get data of products in a single category

    :return: Dict filled with products & kept fields

    First try, TODO :
    - work offline with local JSON
    - need to get all the products of a category

    :Tests ONLINE:
    >>> prod_false = get_category('1664')
    >>> prod_false
    False

    >>> prod_bles = get_category('blés')

    :Tests OFFLINE:
    # >>> prod_bles = get_category('biscuits', True)
    >>> prod_bles['category'] == 'biscuits'
    True

    >>> 'count' in prod_bles
    True

    >>> 'product_name' in prod_bles['products'][0]
    True

    >>> 'nutrition_grades' in prod_bles['products'][0]
    True

    >>> 'categories_tags' in prod_bles['products'][0]
    True

    >>> get_category('wrong_file', True)
    File load error : sample/category-wrong_file.json
    False

    # >>> pprint.pprint(prod_bles)
    """

    if from_file:
        from os import path

        filename = 'sample/category-{}.json'.format(str(name))
        # File did not exists
        if path.isfile(filename) is False:
            print("File load error : {}".format(filename))
            status = 404
            cat_json = {'count': 0}

        else:
            with open(filename, "r") as json_file:
                cat_json = json.loads(json_file.read())
                status = 200

    # Requests over API
    else:
        page = 1
        response = requests.get(API_URL_CAT.format(str(name), page))
        cat_json = json.loads(response.text)
        status = response.status_code

    # Gets data
    if cat_json['count'] > 0:
        # Defines dict it will be returned
        staging_data = {
            # 'count': cat_json['count'],
            'category': str(name),
            'products': []
        }

        # Counts pages of this category
        total_pages = int(cat_json['count'] // cat_json['page_size'])

        if int(cat_json['count'] % cat_json['page_size']) > 0:
            total_pages += 1

        # Loops on data from 1st page
        for idx, product_fields in enumerate(cat_json['products']):
            staging_data['products'].append(dict())

            for field in FIELD_KEPT['category']:

                if field in product_fields:
                    staging_data['products'][idx][field] = product_fields[field]

                else:
                    staging_data['products'][idx][field] = False

        # Gets data for all other pages
        while page < total_pages:
            # Requests next page over API
            page += 1
            response = requests.get(API_URL_CAT.format(str(name), page))
            cat_json = json.loads(response.text)
            idx = len(staging_data['products'])

            for product_fields in cat_json['products']:
                staging_data['products'].append(dict())

                for field in FIELD_KEPT['category']:
                    # import pdb; pdb.set_trace()
                    if field in product_fields:
                        staging_data['products'][idx][field] = product_fields[field]

                    else:
                        staging_data['products'][idx][field] = False

                idx += 1

            print("\t\t[…finish page {}/{} - {} ids]".format(page, total_pages, idx))

        return staging_data

    else:
        return False


def false_to_null(sql_list):
    """ Replacing nutrition_score="False" by nutrition_score=NULL """
    for idx, request in enumerate(sql_list):
        if "False" in request:
            sql_list[idx] = "{}NULL{}".format(
                request[:request.find('False')-1],
                request[request.find('False')+6:]
            )
    return sql_list


def pick_category(cat_list):
    """
    Picks only one category to associate the product in the local DB

    One of the shortest tag (without langage prefix) is taken.
    For improvement it is a good place to adds more work here, like selecting
    by langage prefix.

    :Tests:
    >>> pick_category(['en:sugary-snacks', 'en:biscuits-and-cakes', \
'en:biscuits'])
    'biscuits'
    """
    if len(cat_list) > 1:
        # get idx of the shortest tag
        flip_list = [(len(cat), idx) for idx, cat in enumerate(cat_list)]
        flip_list.sort()

        shortest_tag_idx = flip_list[0][1]

        return cat_list[shortest_tag_idx].split(":")[1]

    elif len(cat_list) == 1:
        return cat_list[0].split(":")[1]

    else:
        return False


def sql_generator(staging_data):
    """
    Uses `staging_data` to generate SQL INSERT requests.

    :staging_data: dict() created with `get_product()` or `get_category()`
    :return: list() of SQL requests

    :Tests:
    >>> sql_generator(False) is False
    True

    >>> bisc = {'count': 4377,'category':'biscuits','products':[{'_id':'8480000141323','categories_tags':['en:sugary-snacks','en:biscuits-and-cakes','en:biscuits'],'nutrition_grades':'e','product_name':'Galletas María Dorada Hacendado','url':'https://fr-en.openfoodfacts.org/product/8480000141323/galletas-maria-dorada-hacendado'},{'_id':'3593551174971','categories_tags':['en:sugary-snacks','en:biscuits-and-cakes','en:biscuits'],'nutrition_grades':'False','product_name':'Les Broyés du Poitou','url':'https://fr-en.openfoodfacts.org/product/3593551174971/les-broyes-du-poitou-les-mousquetaires'}]}

    >>> sql_list_bisc = sql_generator(bisc)
    >>> sql_list_bisc[0]
    "INSERT INTO category (`name`) VALUES ('biscuits');"

    >>> sql_list_bisc[1]
    'INSERT INTO product (`name`, `code`, `url`, `nutrition_grades`, `category_id`) SELECT "Galletas María Dorada Hacendado", "8480000141323", "https://fr-en.openfoodfacts.org/product/8480000141323/galletas-maria-dorada-hacendado", "e", id AS category_id FROM category WHERE name = "biscuits";'

    >>> sql_list_bisc[2]
    'INSERT INTO product (`name`, `code`, `url`, `nutrition_grades`, `category_id`) SELECT "Les Broyés du Poitou", "3593551174971", "https://fr-en.openfoodfacts.org/product/3593551174971/les-broyes-du-poitou-les-mousquetaires", NULL, id AS category_id FROM category WHERE name = "biscuits";'

    >>> oreo = {'categories_tags':['en:sugary-snacks','en:biscuits-and-cakes','en:biscuits','en:chocolate-biscuits','es:sandwich-cookies'],'code':'8410000810004','nutrition_grades':'e','product_name':'Biscuit Oreo', 'url':'https://fr.openfoodfacts.org/product/8410000810004/'}
    >>> sql_list_oreo = sql_generator(oreo)
    >>> sql_list_oreo[0]
    "INSERT INTO category (`name`) VALUES ('biscuits');"

    >>> sql_list_oreo[1]
    'INSERT INTO product (`name`, `code`, `url`, `nutrition_grades`, `category_id`) SELECT "Biscuit Oreo", "8410000810004", "https://fr.openfoodfacts.org/product/8410000810004/", "e", id AS category_id FROM category WHERE name = "biscuits";'

    >>> oreo_nutri_null = {'categories_tags':['en:sugary-snacks','en:biscuits-and-cakes','en:biscuits','en:chocolate-biscuits','es:sandwich-cookies'],'code':'8410000810004','nutrition_grades':'False','product_name':'Biscuit Oreo', 'url':'https://fr.openfoodfacts.org/product/8410000810004/'}
    >>> sql_list_oreo_nutri_null = sql_generator(oreo_nutri_null)

    >>> sql_list_oreo_nutri_null[1]
    'INSERT INTO product (`name`, `code`, `url`, `nutrition_grades`, `category_id`) SELECT "Biscuit Oreo", "8410000810004", "https://fr.openfoodfacts.org/product/8410000810004/", NULL, id AS category_id FROM category WHERE name = "biscuits";'
    """

    sql_list = []
    insert_cat = "INSERT INTO category (`name`) VALUES ('{}');"
    insert_prod = """INSERT INTO product (`name`, `code`, `url`, `nutrition_grades`, `category_id`) \
SELECT "{name}", "{code}", "{url}", "{nutri}", id AS category_id \
FROM category \
WHERE name = "{cat}";"""

    if staging_data is not False and 'category' in staging_data.keys():
        used_category = staging_data['category']

        # insert category
        sql_list.append(insert_cat.format(used_category))

        # insert products
        for idx, val in enumerate(staging_data['products']):
            sql_list.append(
                insert_prod.format(
                    code=val['_id'],
                    url=val['url'],
                    name=val['product_name'],
                    nutri=val['nutrition_grades'],
                    cat=used_category
                )
            )

    elif staging_data is not False and 'product_name' in staging_data.keys():
        used_category = pick_category(staging_data['categories_tags'])

        # insert category
        sql_list.append(insert_cat.format(used_category))

        sql_list.append(
            insert_prod.format(
                code=staging_data['code'],
                url=staging_data['url'],
                name=staging_data['product_name'],
                nutri=staging_data['nutrition_grades'],
                cat=used_category
            )
        )

    else:
        sql_list = False

    if sql_list is not False:
        sql_list = false_to_null(sql_list)

    return sql_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()
