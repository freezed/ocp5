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

def get_product(code):
    """
    Call OpenFF API to get data of a single product

    :Tests:
    >>> product = get_product('3017760000109')
    >>> print(product['id'])
    3017760000109

    >>> print(product['product_name'])
    Le Véritable Petit Beurre

    >>> print(product['stores'])
    Super U

    >>> print(product['nutrition_grades'])
    e

    >>> print(product['categories_tags'])
    ['en:sugary-snacks', 'en:biscuits-and-cakes', 'en:biscuits', 'fr:petits-beurres']
    """

if __name__ == "__main__":
    """ Starting doctests """

    import doctest
    doctest.testmod()
