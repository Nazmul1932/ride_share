GRANT ALL PRIVILEGES ON nhdb.* TO 'admin'@'%';
use nhdb;
CREATE TABLE Ratings (
    driver_name varchar(255),
    rating varchar(255)
);