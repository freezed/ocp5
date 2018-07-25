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

# CONFIG
FIELD_KEPT = [
    'product_name',
    'stores',
    'nutrition_grades',
    'categories_tags',
    'id'
]


def get_product(code):
    """
    Call OpenFF API to get data of a single product

    :Tests:
    >>> prod_beurre = get_product('3017760000109')
    >>> print(prod_beurre['product_name'])
    Le Véritable Petit Beurre

    >>> print(prod_beurre['stores'])
    Super U

    >>> print(prod_beurre['nutrition_grades'])
    e

    >>> print(prod_beurre['categories_tags'])
    ['en:sugary-snacks', 'en:biscuits-and-cakes', 'en:biscuits', 'fr:petits-beurres']

    >>> prod_oreo = get_product('8410000810004')
    >>> print(prod_oreo['product_name'])
    Biscuit Oreo

    >>> print(prod_oreo['stores'])
    Cora,Irma.dk,Leader Price

    >>> print(prod_oreo['nutrition_grades'])
    e

    >>> print(prod_oreo['categories_tags'])
    ['en:sugary-snacks', 'en:biscuits-and-cakes', 'en:biscuits', 'en:chocolate-biscuits', 'es:sandwich-cookies']

    >>> prod_false = get_product('1664')
    >>> prod_false is False
    True

    >>> prod_string = get_product('string')
    >>> prod_string is False
    True
    """


    response = requests.get(
        "https://fr.openfoodfacts.org/api/v0/product/{}.json".format(code)
    )
    product_data = json.loads(response.text)

    product = {}

    for field in FIELD_KEPT:
        product[field] = product_data['product'][field]

    return product


if __name__ == "__main__":
    """ Starting doctests """

    import doctest
    doctest.testmod()
