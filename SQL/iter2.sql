begin
for i in (select * from user_tables) loop
execute immediate ('drop table ' || i.table_name || ' cascade constraints');
end loop;
end;
/

CREATE TABLE genericuser (
    login VARCHAR2(25) PRIMARY KEY,
    password VARCHAR2(25) NOT NULL,
    time_created TIMESTAMP NOT NULL
);

CREATE TABLE passive (
    login VARCHAR2(25) NOT NULL UNIQUE,
    reg_numa VARCHAR(25) PRIMARY KEY,
    FOREIGN KEY (login)
    REFERENCES genericuser(login)
    ON DELETE CASCADE
);

CREATE TABLE active (
    login VARCHAR2(25) PRIMARY KEY,
    passive VARCHAR2(25) NOT NULL,
    FOREIGN KEY (login)
    REFERENCES genericuser(login)
    ON DELETE CASCADE,
    FOREIGN KEY (passive)
    REFERENCES passive(login)
    ON DELETE CASCADE
);

CREATE TABLE val (
    pk_id INTEGER PRIMARY KEY,
    name VARCHAR2(25) NOT NULL,
    price INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    offerant VARCHAR2(25) NOT NULL, 
    rent_type VARCHAR2(25),
    val_type VARCHAR2(25) 
);

CREATE TABLE solicitude (
    pk_id INTEGER PRIMARY KEY, 
    operation_type VARCHAR2(1) NOT NULL,
    val INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    quantity_type VARCHAR2(1) NOT NULL,
    time_created TIMESTAMP NOT NULL,
    active_login VARCHAR2(25) NOT NULL,
    solved VARCHAR2(1) NOT NULL,
    is_active VARCHAR2(1) NOT NULL,
    FOREIGN KEY (val)
    REFERENCES val(pk_id)
    ON DELETE CASCADE,
    FOREIGN KEY (active_login)
    REFERENCES active(login)
    ON DELETE CASCADE
);

CREATE TABLE ownerval (
    val INTEGER NOT NULL,
    owner VARCHAR(25) NOT NULL,
    PRIMARY KEY (val, owner)
    FOREIGN KEY (val)
    PREFERENCES val(pk_id)
    ON DELETE CASCADE
    FOREIGN KEY (owner)
    PREFERENCES active(login)
    ON DELETE CASCADE
);

CREATE TABLE swaptransaction (
    pk_id INTEGER PRIMARY KEY,
    time_created TIMESTAMP NOT NULL,
    sell_solicitude INTEGER NOT NULL,
    buy_solicitude INTEGER NOT NULL,
    FOREIGN KEY (sell_solicitude)
    REFERENCES solicitude(pk_id)
    ON DELETE CASCADE,
    FOREIGN KEY (buy_solicitude)
    REFERENCES solicitude(pk_id)
    ON DELETE CASCADE
);