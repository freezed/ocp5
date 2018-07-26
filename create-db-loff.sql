-- ---------------------------------------------
-- Creates a local DB to avoid requesting API --
-- ---------------------------------------------

DROP DATABASE IF EXISTS loff;
CREATE DATABASE loff CHARACTER SET 'utf8';
USE loff;

CREATE TABLE product(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `code` BIGINT UNSIGNED NOT NULL UNIQUE,
    `name` VARCHAR(200),
    `nutrition_grades` VARCHAR(1)
);

CREATE TABLE category(
    `id`INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(200)
);

CREATE TABLE asso_prod_cat(
    `category_id` INT UNSIGNED NOT NULL,
    `product_id` INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_asso_prod_cat_category`
        FOREIGN KEY(category_id)
        REFERENCES category(id)
        ON DELETE CASCADE,
    CONSTRAINT `fk_asso_prod_cat_product`
        FOREIGN KEY(product_id)
        REFERENCES product(id)
        ON DELETE CASCADE
);
