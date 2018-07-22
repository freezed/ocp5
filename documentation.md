# Documentation

## Installation

1. get the code : `git clone git@github.com:freezed/ocp5.git`
2. if you want, create a dedicated virtualenv
3. adds dependencies : `cd ocp5; pip3 install -r requirement.txt`
4. run it : `./main.py`

## Usage

### A - Find an alternative product

1. Type the number corresponding to the product's category
2. Type the number corresponding to the choosen alternative product
3. The system shows you the product sheet :
     - description
     - a shop where you can buy it (if available)
     - the product link to [OpenFoodFacts][1] website
4. Decide if you want to save the alternative product in DB

### B - Retrieve my alternative products

1. Type the number corresponding to the choosen alternative product
2. The system shows you the product sheet :
     - description
     - a shop where you can buy it (if available)
     - the product link to [OpenFoodFacts][1] website

## Data used

With the field 'countries':'france'

Data provided by [OpenFoodFacts][1] is saved in more than 170 fields. Here are those we will need in this projects:

1	code
2	url
4	created_t
6	last_modified_t
8	product_name
10	quantity
11	packaging
13	brands
17	categories_fr
18	origins
20	manufacturing_places
24	labels_fr
25	emb_codes
30	purchase_places
31	stores
35	ingredients_text
41	serving_size
42	serving_quantity
47	additives_fr
48	ingredients_from_palm_oil_n
51	ingredients_that_may_be_from_palm_oil_n
53	ingredients_that_may_be_from_palm_oil_tags
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



[1]: https://fr.openfoodfacts.org/ "OpenFoodFacts project"
