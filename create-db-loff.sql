-- ---------------------------------------------
-- Creates a local DB to avoid requesting API --
-- ---------------------------------------------

DROP DATABASE IF EXISTS loff;
CREATE DATABASE loff CHARACTER SET 'utf8';
USE loff;

CREATE TABLE category(
    `id`INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(200) UNIQUE

)ENGINE=InnoDB;

CREATE TABLE product(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `code` BIGINT UNSIGNED NOT NULL UNIQUE,
    `url` VARCHAR(200),
    `name` VARCHAR(200) UNIQUE,
    `nutrition_grades` VARCHAR(1),
    `category_id`INT UNSIGNED,
    `substitute_id` INT UNSIGNED,
    CONSTRAINT `fk_product_category`
        FOREIGN KEY (category_id) REFERENCES category(id)
        ON DELETE CASCADE,
    CONSTRAINT `fk_product_substitute`
        FOREIGN KEY (substitute_id) REFERENCES product(id)
        ON DELETE SET NULL
)ENGINE=InnoDB;
