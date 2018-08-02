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
# import pprint
from config import FIELD_KEPT


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
    File load error : sample-product-1664.json

    >>> prod_string = get_product('string', True)
    File load error : sample-product-string.json

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
    filename = 'sample-product-{}.json'.format(str(code))

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

    # >>> prod_bisc = get_category('biscuits')

    :Tests OFFLINE:
    >>> prod_bisc = get_category('biscuits', True)
    >>> prod_bisc['category'] == 'biscuits'
    True

    >>> 'count' in prod_bisc
    True

    >>> 'product_name' in prod_bisc['products'][0]
    True

    >>> 'nutrition_grades' in prod_bisc['products'][0]
    True

    >>> 'categories_tags' in prod_bisc['products'][0]
    True

    >>> get_category('wrong_file', True)
    File load error : sample-category-wrong_file.json
    False

    # >>> pprint.pprint(prod_bisc)
    """

    if from_file:
        from os import path

        filename = 'sample-category-{}.json'.format(str(name))
        # File did not exists
        if path.isfile(filename) is False:
            print("File load error : {}".format(filename))
            status = 404
            category_json = {'count': 0}

        else:
            with open(filename, "r") as json_file:
                category_json = json.loads(json_file.read())
                status = 200
    else:
        response = requests.get(
            "https://fr.openfoodfacts.org/category/{}.json".format(str(name))
        )
        category_json = json.loads(response.text)
        status = response.status_code

    if category_json['count'] is not 0 and status == 200:
        category_kept = {
            'count': category_json['count'],
            'category': str(name),
            'products': []
            }

        for idx, product_fields in enumerate(category_json['products']):
            category_kept['products'].append(dict())

            for field in FIELD_KEPT['category']:

                if field in product_fields:
                    category_kept['products'][idx][field] = product_fields[field]

                else:
                    category_kept['products'][idx][field] = False

        return category_kept

    else:
        return False


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
    >>> bisc = {'count': 4377,'category':'biscuits','products':[\
{'_id':'8480000141323','categories_tags':['en:sugary-snacks','en:biscuits-and-cakes','en:biscuits'],'nutrition_grades':'d','product_name':'Galletas María Dorada Hacendado','url':'https://fr-en.openfoodfacts.org/product/8480000141323/galletas-maria-dorada-hacendado'},\
{'_id':'3593551174971','categories_tags':['en:sugary-snacks','en:biscuits-and-cakes','en:biscuits'],'nutrition_grades':'e','product_name':'Les Broyés du Poitou','url':'https://fr-en.openfoodfacts.org/product/3593551174971/les-broyes-du-poitou-les-mousquetaires'}]}

    >>> sql_list_bisc = sql_generator(bisc)
    >>> sql_list_bisc[0]
    "INSERT INTO category (`name`) VALUES ('biscuits')"

    >>> sql_list_bisc[1]
    "INSERT INTO product (`code`, `url`, `name`, `nutrition_grades`, `category_id`) \
SELECT '8480000141323', 'https://fr-en.openfoodfacts.org/product/8480000141323/galletas-maria-dorada-hacendado', 'Galletas María Dorada Hacendado', 'd', id AS category_id \
FROM category WHERE name = 'biscuits';"

    >>> sql_list_bisc[2]
    "INSERT INTO product (`code`, `url`, `name`, `nutrition_grades`, `category_id`) SELECT '3593551174971', 'https://fr-en.openfoodfacts.org/product/3593551174971/les-broyes-du-poitou-les-mousquetaires', 'Les Broyés du Poitou', 'e', id AS category_id FROM category WHERE name = 'biscuits';"

    >>> oreo = {'categories_tags':['en:sugary-snacks','en:biscuits-and-cakes','en:biscuits','en:chocolate-biscuits','es:sandwich-cookies'],'code':'8410000810004','nutrition_grades':'e','product_name':'Biscuit Oreo', 'url':'https://fr.openfoodfacts.org/product/8410000810004/'}
    >>> sql_list_oreo = sql_generator(oreo)
    >>> sql_list_oreo[0]
    "INSERT INTO category (`name`) VALUES ('biscuits')"

    >>> sql_list_oreo[1]
    "INSERT INTO product (`code`, `url`, `name`, `nutrition_grades`, `category_id`) SELECT '8410000810004', 'https://fr.openfoodfacts.org/product/8410000810004/', 'Biscuit Oreo', 'e', id AS category_id FROM category WHERE name = 'biscuits';"
    """

    sql_list = []
    insert_cat = "INSERT INTO category (`name`) VALUES ('{}')"
    insert_prod = """INSERT INTO product (`code`, `url`, `name`, `nutrition_grades`, `category_id`) \
SELECT '{code}', '{url}', '{name}', '{nutri}', id AS category_id \
FROM category \
WHERE name = '{cat}';"""

    if 'category' in staging_data.keys():
        used_category = staging_data['category']

        # insert category
        sql_list.append(insert_cat.format(used_category))

        # insert products
        for idx, val in enumerate(staging_data['products']):
            sql_list.append(
                insert_prod.format(
                    code=staging_data['products'][idx]['_id'],
                    url=staging_data['products'][idx]['url'],
                    name=staging_data['products'][idx]['product_name'],
                    nutri=staging_data['products'][idx]['nutrition_grades'],
                    cat=used_category
                )
            )

    elif 'product_name' in staging_data.keys():
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

    return sql_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()
