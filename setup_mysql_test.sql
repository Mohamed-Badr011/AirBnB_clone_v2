-- Prepares a MySQL server:
--    1. A database hbnb_test_db
--    2. A new user hbnb_test (in localhost)
--    3. The password of hbnb_test should be set to hbnb_test_pwd
--    4. hbnb_test should have all privileges on the database 
--       hbnb_test_db (and only this database)
--    5. hbnb_test should have SELECT privilege on the database 
--       performance_schema (and only this database)
--    6. If the database hbnb_test_db or the user hbnb_test 
--       already exists, your script should not fail

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
