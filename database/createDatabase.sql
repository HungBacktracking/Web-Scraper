CREATE TABLE Laptop(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    info_link NVARCHAR(300),
    img_link NVARCHAR(300),
    brand NVARCHAR(20),
    screen FLOAT(32),
    cpu NVARCHAR(20),
    ram INT,
    disk_type NVARCHAR(20),
    disk_storage NVARCHAR(20),
    gpu NVARCHAR(200),
    shop CHAR(3),
    type NVARCHAR(20)    
);

CREATE TABLE PC(
	id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    
    info_link NVARCHAR(300),
    img_link NVARCHAR(300),
    brand NVARCHAR(20),
    cpu NVARCHAR(20),
    ram INT,
    disk_type NVARCHAR(20),
    disk_storage NVARCHAR(20),
    shop CHAR(3),
    type NVARCHAR(20)
);

CREATE TABLE Screen(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    info_link NVARCHAR(300),
    img_link NVARCHAR(300),
    brand NVARCHAR(20),
    screen FLOAT(32),
    refresh_rate INT,
    shop CHAR(3),
    type NVARCHAR(20)    
);

CREATE TABLE Mouse(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    info_link NVARCHAR(300),
    img_link NVARCHAR(300),
    brand NVARCHAR(20),
    shop CHAR(3),
    type NVARCHAR(20)    
);

CREATE TABLE Keyboard(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name NVARCHAR(200),
    price INT,
    info_link NVARCHAR(300),
    img_link NVARCHAR(300),
    brand NVARCHAR(20),
    shop CHAR(3),
    type NVARCHAR(20)    
);