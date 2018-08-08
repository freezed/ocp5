Documentation
=============

## Created with

- `python 3.6.4 `
- `Requests`
- `PyMySQL`

## Installation

1. get the code : `git clone git@github.com:freezed/ocp5.git`
2. create a dedicated virtualenv : `python3 -m venv .venv; source .venv/bin/activate`
3. adds dependencies : `cd ocp5; pip install -r requirements.txt`

## Collects data

1. [OpenFoodFacts data uses more than 170 fields][92]. Here are those we keep localy :
```
code / _id
url
product_name
categories_tags
nutrition_grades
```
2. Physical Data Model

![-Physical Data Model-][96]

3. Edit [config.py](https://github.com/freezed/ocp5/blob/master/config.py)
4. Creates local MariaDB/MySQL : `python ./populate-.py`

## Use de CLI to get alternate product

1. run it : `python ./cli.py`
2. follow instructions :

    1. Find a substitute product

        1. Type the number corresponding to the product's category
        2. Type the number corresponding to the choosen substitute product
        3. The system shows you the product sheet :
             - description
             - the product link to [OpenFoodFacts][91] website
        4. Decide if you want to save the substitute product in DB

    2. Retrieve saved substitutes

[91]: https://world.openfoodfacts.org/ "OpenFoodFacts project"
[92]: https://world.openfoodfacts.org/data/data-fields.txt "OpenFoodFacts field list"
[93]: https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv "CSV Data Export"
[94]: https://world.openfoodfacts.org/data "OpenFoodFacts data page"
[95]: https://github.com/freezed/ocp5/blob/master/create-db.sql
[96]: https://raw.githubusercontent.com/freezed/ocp5/master/doc/pdm.png "Image of the physical data model"
