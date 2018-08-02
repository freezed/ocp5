USE loff;

SHOW TABLES;

SELECT table_schema "Full database",
    CONCAT(
        ROUND(
            SUM(data_length + index_length)
        / 1024 / 1024, 1),
    " MB") "dbsize"
FROM information_schema.tables
WHERE table_schema = "loff"
GROUP BY table_schema

UNION

SELECT "Rows in 'product' table", COUNT(*)
FROM product

UNION

SELECT "Rows in 'category' table", COUNT(*)
FROM category;
