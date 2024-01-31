/*creates basic tenant table with pertinant tenant info */
CREATE TABLE Tenant ( 
    id INT AUTO_INCREMENT,
    first_name VARCHAR (50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    email VARCHAR (255) NOT NULL,
    phone_number VARCHAR(25) NOT NULL, 
    initial_lease_date DATE NOT NULL,
    PRIMARY KEY(id),
    UNIQUE (email),
    UNIQUE (phone_number)
);

/*creats basic unit table with pertinant unit info */
CREATE TABLE Unit ( 
    unit_number INT AUTO_INCREMENT,
    rent_amount DECIMAL NOT NULL,
    payment_due_date DATE,
    remaining_balance DECIMAL NOT NULL,
    current_tenant INT,
    PRIMARY KEY (unit_number),
    FOREIGN KEY (current_tenant) REFERENCES Tenant (id)
);

/*creates basic payment tracker table with pertinant payment info */
CREATE TABLE payment_log (
    id INT AUTO_INCREMENT,
    payment_date DATE NOT NULL,
    payment_amount DECIMAL NOT NULL,
    unit_number INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (unit_number) REFERENCES Unit (unit_number)
);