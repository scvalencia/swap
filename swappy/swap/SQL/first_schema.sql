begin
for i in (select * from user_tables) loop
execute immediate ('drop table ' || i.table_name || ' cascade constraints');
end loop;
end;
/

create table users(
    login varchar(20) primary key,
    user_id varchar(20) not null,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    email varchar(20) not null,
    phone varchar(15) not null
);

create table passives(
    passive_register varchar(20) primary key,
    user_login varchar(20) unique not null
    references users(login)
    on delete cascade
);

create table actives(
    user_login varchar(20) primary key
    references users(login)
    on delete cascade,
    passive_register varchar(20) unique not null
    references passives(passive_register)
    on delete set null,
    available_money double precision not null
);

create table legals(
    legal_id varchar(20) primary key,
    legal_name varchar(20) not null,
    user_login varchar(20) unique not null
    references users(login)
    on delete cascade
);

create table investors(
    user_login varchar(20) primary key
    references actives(user_login)
    on delete cascade,
    is_enterprise varchar(1) not null
);

create table offerants(
    user_login varchar(20) primary key
    references actives(user_login)
    on delete cascade,
    offerant_type varchar(1) not null
);

create table rents(
    pk_id int primary key,
    rent_name varchar(20) not null,
    description varchar(140) not null,
    rent_function varchar(1) not null,
    rent_length varchar(1) not null,
    rent_type varchar(1) not null,
    offerant_login varchar(20) not null
    references offerants(user_login)
    on delete cascade
);

create table vals(
    pk_id int primary key,
    val_name varchar(20) not null,
    description varchar(140) not null,
    val_type varchar(1) not null,
    amount int not null,
    price double precision not null,
    active_login varchar(20)
    references actives(user_login)
    on delete set null,
    rent_id int not null
    references rents(pk_id)
    on delete cascade
);

create table passwords(
    user_login varchar(20) primary key
    references users(login)
    on delete cascade,
    user_password varchar(20) not null,
    question varchar(20) not null,
    answer varchar(20) not null
);

create table requests(
    pk_id int primary key,
    request_type varchar(1) not null,
    amount double precision not null,
    created_at timestamp not null,
    total double precision not null,
    min_price double precision not null,
    bought varchar(1) not null,
    value_id int not null
    references vals(pk_id)
    on delete cascade,
    active_login varchar(20) not null
    references actives(user_login)
    on delete cascade,
    passive_login varchar(20) not null
    references passives(user_login)
    on delete cascade
);

create table swap_transactions(
    pk_id int primary key,
    created_at timestamp not null,
    passive_login varchar(20) not null
    references passives(user_login)
    on delete cascade,
    active_login varchar(20) not null
    references actives(user_login)
    on delete cascade,
    solved_request_id int not null
    references requests(pk_id)
    on delete cascade,
    sold_request_id int not null
    references requests(pk_id)
    on delete cascade
);

create table news(
    pk_id int primary key,
    title varchar(20) not null,
    taken_from varchar(50) not null,
    created_at timestamp not null
);

create table comments(
    pk_id int primary key,
    comment_content varchar(140) not null,
    created_at timestamp not null,
    news_pk int not null
    references news(pk_id)
    on delete cascade,
    user_login varchar(20) not null
    references actives(user_login)
    on delete cascade
);

create table profiles(
    user_login varchar(20) primary key
    references actives(user_login)
    on delete cascade,
    status varchar(50),
    biography varchar(1000),
    avatar varchar(50),
    currency varchar(1) not null,
    age integer not null,
    last_active timestamp not null
);

create table locations(
    user_login varchar(20) primary key
    references actives(user_login)
    on delete cascade,
    country varchar(20) not null,
    city varchar(20) not null,
    department varchar(20) not null,
    address varchar(20) not null,
    zip_code varchar(10) not null
);

create table contacts(
    user_login varchar(20)
    references actives(user_login)
    on delete cascade,
    contact_link varchar(50) not null,
    contact_name varchar(10) not null,
    primary key (user_login, contact_link)
);

create table professionals(
    user_login varchar(20) primary key
    references actives(user_login)
    on delete cascade,
    resume_pdf varchar(50) not null,
    current_job varchar(20) not null,
    current_org varchar(20) not null
);

create table follows(
    follower_login varchar(20)
    references investors(user_login)
    on delete cascade,
    following_login varchar2(20)
    references actives(user_login)
    on delete cascade,
    primary key (follower_login, following_login)
);