-[_Courses Open Classrooms_][2]-

# [PyDev] Project 5 : Use public data of [Open Food Facts][1] project

_Last version of this document is avaiable on [github][4]._

## Approach

### Introduction

Search substitute for food product in the [Open Food Facts][1] DB and displays products informations

The user can:

 - interacts with the system in the terminal
 - saves products for later retrieval

In my opinion, this is a nice cross-techiques project :

- manipulating REST API, with the help of the `requests` package
- connecting a `MySQL` DB with the help of the `PyMySQL` package
- working on a (local) `MariaDB` server with the help of the `MySQL` client `mycli`
- creating an interactive script

The whole project description is avaiable on [OpenClassrooms site][2].

The project is hosted on [github][5].

### Workflow

 - plan the work : features, scripts, tool needed
 - creates issues for each autonomous package
 - organize it all in a table
 - write documentation, as text & (doc)test
 - writes code


### Code construction

To build the script, I followed this approach :

1. take in hand the necessary tools
2. get started with some the basic features/tools
3. then add more specificdetailed fonctionalities

Concretely this is expressed by :

- familiarize myself with the data stored in the DB (playing with the CSV file)
- use the API in a basic way (see `get_product()` function)
- imagine the main SQL queries
- using PyMySQL in a basic way
- create an interface object with the DB
- create the script interfacing the API and the DB
- creation of the DB client used by the client


### Code organisation

- `config.py`          : configuration
- `cli.py`             : the user interface script
- `db.py`              : DB class used by all scripts
- `function.py`        : files with functions used by all scripts
- `populate-db.py`     : backoffice script used to populate DB using API
- `create-db-loff.sql` : backoffice script used to creates local (empty) DB
- `doc`                : documentation folder
- `legacy-sql`         : first SQL manipulations (just for memories)
- `sample`             : OpenFF JSON category & product files (to work offline and lower API usage)
- `requirements.txt`   : _as itself_
- `LICENSE`            : _as itself_
- `README.md`          : _as itself_
- `.gitignore`         : _as itself_


### Difficulties encountered

#### How to interact between the API and the DB

Before exchanging with my mentor I think about using the CSV file as a resource for creating the local DB and then the API will allow to keep it up to date afterwards. This version would have required a large amount of time without bringing a gain of interest.

#### Creating class Db():

Tests are not required in this project but, using [`doctest`][3] is a precious help when I code. Here was an opportunity for me to use them in a class, causing trouble where the test are usefull : In the class declaration or in the methods?

#### Stay in the scope

Not easy to settle for initial specifications that can be interpreted. Similarly for the levels of detail, it is easy to get caught up in a design where they are places for evolutions/new features.


[1]: https://fr.openfoodfacts.org/ "Open Food Facts répertorie les produits alimentaires du monde entier"
[2]: https://openclassrooms.com/fr/projects/utilisez-les-donnees-publiques-de-lopenfoodfacts "Utilisez les données publiques de l'OpenFoodFact"
[3]: https://docs.python.org/fr/3.6/library/doctest.html "Test interactive Python examples"
[4]: https://github.com/freezed/ocp5/blob/master/doc/approach.md
[5]: https://github.com/freezed/ocp5/projects/1
