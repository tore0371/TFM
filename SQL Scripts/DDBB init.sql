CREATE DATABASE Tfm;
use tfm;

CREATE TABLE supermarket (
    SupermarketID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30),
    Zone VARCHAR(20)
);

CREATE TABLE supermarket_data (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    SupermarketID INT,
    ProductName VARCHAR(50),
    Price DECIMAL(10, 2),
    Weight DECIMAL(10, 2),
    KGPrice DECIMAL(10, 2),
    ImageURL VARCHAR(255),
    FOREIGN KEY (SupermarketID) REFERENCES supermarket(SupermarketID)
);

ALTER TABLE supermarket_data MODIFY ProductName VARCHAR(255);