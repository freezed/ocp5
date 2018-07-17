-[_Parcours Open Classrooms_](https://openclassrooms.com/fr/projects/utilisez-les-donnees-publiques-de-lopenfoodfacts "Utilisez les données publiques de l'OpenFoodFact")-

# [PyDev] Projet 5

## Utilisez les données publiques d'[Open Food Facts][3]

_La dernière version à jour de ce document est disponible sur [github](https://github.com/freezed/ocp5/blob/master/README.md)._

---
## Énoncé

La startup _Pur Beurre_ travaille connait bien les habitudes alimentaires françaises. Leur restaurant, _Ratatouille_, remporte un succès croissant et attire toujours plus de visiteurs sur la butte de Montmartre.

L'équipe a remarqué que leurs utilisateurs voulaient bien changer leur alimentation mais ne savaient pas bien par quoi commencer. Remplacer le Nxxxxxa par une pâte aux noisettes, oui, mais laquelle? Et dans quel magasin l'acheter? Leur idée est donc de créer un système qui interagirait avec la base [Open Food Facts][3] pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

## Cahier des charges

### Parcours utilisateur

1. Quel aliment souhaitez-vous remplacer?
    1. choix de la catégorie
    2. choix de l'aliment
    3. retour d'un substitut :
        * description
        * un magasin ou l'acheter (le cas échéant
        * un lien vers la page d'[Open Food Facts][3] de cet aliment.
    4. enregistrement du résultat (en BDD)
2. Retrouver mes aliments substitués

### Fonctionnalités

- recherche d'aliments dans la base [Open Food Facts][3]
- l'utilisateur interagit avec le système dans le terminal
- si l'utilisateur entre un caractère qui n'est pas un chiffre, le système doit lui répéter la question,
- la recherche doit s'effectuer sur une base MySql.

## Etapes

1. Organiser votre travail
    - [ ] Découpez votre système en user stories puis en tâches et sous-tâches
    - [ ] Créez [un tableau agile][5] et affectez des deadlines
    - [ ] Commencez à écrire la documentation avant de coder chaque nouvelle fonctionnalité
2. Construire la base de données
    - [ ] De quelles info j'ai besoin?
    - [ ] Définir le schéma de la base de données
    - [ ] Quelles informations allez-vous enregistrer?
    - [ ] Quelles données allez-vous manipuler?
    - [ ] Récupérer les données au format JSON via l'[API Open Food Facts][2]
    - [ ] Créez la base de données
    - [ ] Écrivez le script Python qui insèrera les de l'[API][2] dans votre base
3. Construire le système
    - [ ] Listez les fonctionnalités de votre système
    - [ ] Codez!
4. Interagir avec la base de données
    - [ ] Commencez par les question réponse (input, validation des champs)
    - [ ] Puis la recherche : quelles requêtes SQL? Dans quelle(s) table(s)?
    - [ ] Enregistrer les données générées par le système pour que l'utilisateur les retrouve

## Livrables

- [Code source publié sur _Github_][4]
- [Tableau agile][5]
- [Modèle physique de données][6]
- [Script de création de votre base de données][7]
- [Document texte expliquant la démarche][8]
    * difficultés rencontrées / solutions trouvées
    * lien _Github_
    * développez le choix de l'algorithme et la méthodologie choisie
    * format pdf n'éxcédant pas 2 pages A4
    * rédigé en anglais ou français (les fautes seront évaluées)

[1]: https://guides.github.com/features/mastering-markdown/
[2]: http://en.wiki.openfoodfacts.org/Project:API
[3]: https://world.openfoodfacts.org/
[4]: https://github.com/freezed/ocp5/blob/master/README.md
[5]: https://github.com/freezed/ocp5/projects/1
[6]: https://github.com/freezed/ocp5/blob/master/mpd.png
[7]: https://github.com/freezed/ocp5/blob/master/create-db.md
[8]: https://github.com/freezed/ocp5/blob/master/approach.md
