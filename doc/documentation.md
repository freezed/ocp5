Documentation
=============

## Created with

- `python 3.6.4 `
- `Requests`
- ~`PyMySQL` or `openfoodfacts-python`~ [`TODO #4`][4]

## Installation

1. get the code : `git clone git@github.com:freezed/ocp5.git`
2. create a dedicated virtualenv : `python3 -m venv .venv; source .venv/bin/activate`
3. adds dependencies : `cd ocp5; pip install -r requirements.txt`

## Collects data

1. [OpenFoodFacts data uses more than 170 fields][92]. Here are those we keep localy :
```
code
product_name
categories_fr
nutrition-score-fr_100g
```
2. Request will only ask for tagged products with `'countries':'france'`
3. Physical Data Model

![-Physical Data Model-][96]

4. ~Creates local MariaDB/MySQL : `./create-db.py`~ [`TODO #2`][2]

## Use de CLI to get alternate product

1. ~run it : `./main.py`~ [`TODO #5`][5]
2. ~follow instructions :~ [`TODO #5`][5]

    1. Find an alternative product

        1. Type the number corresponding to the product's category
        2. Type the number corresponding to the choosen alternative product
        3. The system shows you the product sheet :
             - description
             - a shop where you can buy it (if available)
             - the product link to [OpenFoodFacts][91] website
        4. Decide if you want to save the alternative product in DB

    2. Retrieve saved alternatives products

        1. Type the number corresponding to the choosen alternative product
        2. The system shows you the product sheet :
             - description
             - a shop where you can buy it (if available)
             - the product link to [OpenFoodFacts][91] website


[91]: https://world.openfoodfacts.org/ "OpenFoodFacts project"
[92]: https://world.openfoodfacts.org/data/data-fields.txt "OpenFoodFacts field list"
[93]: https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv "CSV Data Export"
[94]: https://world.openfoodfacts.org/data "OpenFoodFacts data page"
[95]: https://github.com/freezed/ocp5/blob/master/create-db.sql
[96]: https://raw.githubusercontent.com/freezed/ocp5/master/doc/pdm.png "Image of the physical data model"
[2]: https://github.com/freezed/ocp5/issues/2 "Issue #2"
[4]: https://github.com/freezed/ocp5/issues/4 "Issue #4"
[5]: https://github.com/freezed/ocp5/issues/5 "Issue #5"