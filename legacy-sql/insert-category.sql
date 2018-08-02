USE loff;

INSERT INTO category (name) VALUES ('biscuits');

INSERT INTO product (code, url, name, nutrition_grades, category_id)
SELECT
    '8480000141323',
    'https://fr-en.openfoodfacts.org/product/8480000141323/galletas-maria-dorada-hacendado',
    'Galletas María Dorada Hacendado',
    'd',
    id AS category_id
FROM category
WHERE name = 'biscuits';

INSERT INTO product (code, name, nutrition_grades, category_id, url)
VALUES ('3593551174971', 'Les Broyés du Poitou', 'e', 1, 'https://fr-en.openfoodfacts.org/product/3593551174971/les-broyes-du-poitou-les-mousquetaires'),
       ('2000000052047', 'Palets solognots', 'e', 1, 'https://fr-en.openfoodfacts.org/product/2000000052047/palets-solognots-biscuiterie-de-chambord'),
       ('3175681771772', 'Moelleux POMME FRAMBOISE', 'c', 1, 'https://fr-en.openfoodfacts.org/product/3175681771772/moelleux-pomme-framboise-gerble'),
       ('26035642', 'Cookies nougatine + pépites de chocolat', 'e', 1, 'https://fr-en.openfoodfacts.org/product/26035642/cookies-nougatine-pepites-de-chocolat-arizona')
