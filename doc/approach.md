-[_Courses Open Classrooms_][2]-

# [PyDev] Project 5 : Use public data of [Open Food Facts][1] project

_Last version of this document is available on [github][4]._

## Approach

### Introduction

Search substitute for food product in the [Open Food Facts][1] DB and displays products informations

The user can:

 - interact with the system in the terminal
 - save products for later retrieval

This project was created for studying purpose, to train these tools :

- manipulating [Open Food Facts `REST API`][9] with [`Requests`][6]
- connecting a `MySQL` DB with [`PyMySQL`][7]
- using a [`MariaDB`][8] server with a `MySQL` CLI (`mycli`)
- creating an interactive script


[](https://world.openfoodfacts.org/) t purpose. It can evolve beyond for training with [PyMySQL](), [Requests]() and [OpenFF API](https://en.wiki.openfoodfacts.org/API).

The whole exercise description is available on [OpenClassrooms site][2].

The project is hosted on [github][5].

### Workflow

 - plan the work : features, scripts, files, functions tool needed…
 - create `features`, grouped in autonomous packages
 - organize `features` in a _kanban_ type table
 - write documentation, as text & [`doctest`][3]
 - write code


### Code construction

To build the script, I followed this approach :

1. take in hand the necessary tools
2. get started with some the basic features/tools
3. finally add more specific detailed functionalities

Concretely :

- familiarize myself with the data stored in the DB (playing with the CSV file)
- use the API in a basic way (see `get_product()` function)
- imagine the main SQL queries
- use `PyMySQL` in a basic way
- create an interface object with the DB
- create the script interfacing the API and the DB
- create the DB CLI used by the user


### Code organization

- `config.py`          : configuration
- `cli.py`             : user interface script
- `db.py`              : DB class used by all scripts
- `function.py`        : files with functions used by all scripts
- `populate-db.py`     : back-office script used to populate DB using API
- `create-db-loff.sql` : back-office script used to creates local (empty) DB
- `doc`                : documentation folder
- `legacy-sql`         : first SQL manipulations (just for memories)
- `sample`             : _Open Food Facts_ category & product JSON files (to work offline and lower API usage)


### Difficulties encountered

#### How to interact between the API and the DB

Before exchanging with my mentor I think about using the CSV file as a resource for creating the local DB and then the API will allow to keep it up to date afterwards. This version would have required a large amount of time without bringing a gain of interest.

#### Creating class Db():

Tests are not required in this project but, using [`doctest`][3] is a precious help when I code. It was an opportunity for me to use them in a class, dealing with trouble like «where the test are useful»?

#### Stay in the scope

Not easy to frame initial specifications that have a part of interpretation. Similarly for the levels of details, it is easy to slip into a design where they are places for evolution and/or new features.


[1]: https://fr.openfoodfacts.org/ "Open Food Facts répertorie les produits alimentaires du monde entier"
[2]: https://openclassrooms.com/fr/projects/utilisez-les-donnees-publiques-de-lopenfoodfacts "Utilisez les données publiques de l'OpenFoodFact"
[3]: https://docs.python.org/fr/3.6/library/doctest.html "Test interactive Python examples"
[4]: https://github.com/freezed/ocp5/blob/master/doc/approach.md
[5]: https://github.com/freezed/ocp5/projects/1
[6]: https://pypi.org/project/requests/#description "Requests is the only Non-GMO HTTP library for Python, safe for human consumption"
[7]: https://pymysql.readthedocs.io/en/latest/ "Pure Python MySQL Client"
[8]: https://mariadb.org/ "One of the most popular database servers. Made by the original developers of MySQL. Guaranteed to stay open source."
[9]: https://en.wiki.openfoodfacts.org/API "Open Food Facts API"
