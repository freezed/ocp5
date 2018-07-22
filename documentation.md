Documentation
=============

## Installation

1. get the code : `git clone git@github.com:freezed/ocp5.git`
2. create a dedicated virtualenv
3. ~adds dependencies : `cd ocp5; pip3 install -r requirement.txt`~
4. dowload the [HUDGE CSV file][3] ([more info about data here][4])
5. set up the data on a MariaDB/MySQL server with [`create-db.sql`][5]
5. ~run it : `./main.py`~

## Usage

### 1. Find an alternative product

1. Type the number corresponding to the product's category
2. Type the number corresponding to the choosen alternative product
3. The system shows you the product sheet :
     - description
     - a shop where you can buy it (if available)
     - the product link to [OpenFoodFacts][1] website
4. Decide if you want to save the alternative product in DB

### 2. Retrieve saved alternatives products

1. Type the number corresponding to the choosen alternative product
2. The system shows you the product sheet :
     - description
     - a shop where you can buy it (if available)
     - the product link to [OpenFoodFacts][1] website

## Data kept

1. Tagged `'countries':'france'`
2. [OpenFoodFacts data uses more than 170 fields][2]. Here are those we keep in this project :

```
1	code
2	url
4	created_t
6	last_modified_t
8	product_name
10	quantity
11	packaging_tags
13	brands_tags
17	categories_fr
18	origins_tags
20	manufacturing_places_tags
24	labels_fr
30	purchase_places
31	stores
35	ingredients_text
41	serving_size
42	serving_quantity
47	additives_fr
55	nutrition_grade_fr
60	states_fr
62	main_category_fr
69	energy_100g
71	fat_100g
108	sugars_100g
122	salt_100g
123	sodium_100g
124	alcohol_100g
165	nutrition-score-fr_100g
```


[1]: https://world.openfoodfacts.org/ "OpenFoodFacts project"
[2]: https://world.openfoodfacts.org/data/data-fields.txt "OpenFoodFacts field list"
[3]: https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv "CSV Data Export"
[4]: https://world.openfoodfacts.org/data "OpenFoodFacts data page"
[5]: https://github.com/freezed/ocp5/blob/master/create-db.sql
