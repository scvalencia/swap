create table users(
    login varchar2(20) primary key,
    id varchar2(20) not null,
    name varchar2(20) not null,
    email varchar2(20) not null,
    phone varchar2(15) not null
);

create table passives(
    register varchar2(20) primary key,
    user_login varchar2(20) unique not null,
    foreign key (user_login)
    references users(login)
    on delete cascade
);

create table actives(
    user_login varchar2(20) primary key,
    passive_register varchar2(20) unique not null,
    foreign key (user_login)
    references users(login)
    on delete cascade,
    foreign key (passive_register)
    references passives(register)
    on delete cascade
);

create table legals(
    id varchar2(20) primary key,
    name varchar2(20) not null,
    user_login varchar2(20) unique not null,
    foreign key (user_login)
    references users(login)
    on delete cascade
);

create table investors(
    user_login varchar2(20) primary key,
    is_enterprise varchar2(1) not null,
    foreign key (user_login)
    references actives(user_login)
    on delete cascade
);

create table offerants(
    user_login varchar2(20) primary key,
    type integer not null,
    foreign key (user_login)
    references actives(user_login)
    on delete cascade
);

create table rents(
    id varchar2(20) primary key,
    name varchar2(20) not null,
    description varchar2(200) not null,
    function integer not null,
    length integer not null,
    type integer not null,
    offerant_login varchar2(20) not null,
    foreign key (offerant_login)
    references offerants(user_login)
    on delete cascade
);

create table vals(
    id varchar2(100) primary key,
    name varchar2(20) not null,
    description varchar2(200) not null,
    type integer not null,
    amount integer not null,
    availability varchar2(1) not null,
    price double precision not null,
    active_login varchar2(20) not null,
    rent_id varchar(20) not null,
    foreign key (active_login)
    references actives(user_login)
    on delete cascade,
    foreign key (rent_id)
    references rents(id)
    on delete cascade
);

create table passwords(
    user_login varchar2(20) primary key,
    password varchar2(20) not null,
    question varchar2(20) not null,
    answer varchar2(20) not null,
    foreign key (user_login)
    references users(login)
    on delete cascade
);

create table requests(
    id varchar2(100) primary key,
    type integer not null,
    amount double precision not null,
    created_at date not null,
    total double precision not null,
    min_price double precision not null,
    bought varchar(1) not null,
    value_id varchar2(100) not null,
    active_login varchar2(20) not null,
    passive_login varchar2(20) not null,
    foreign key (value_id)
    references vals(id)
    on delete cascade,
    foreign key (active_login)
    references actives(user_login)
    on delete cascade,
    foreign key (passive_login)
    references passives(user_login)
    on delete cascade
);

create table transactions(
    id varchar2(20) primary key,
    created_at date not null,
    passive_login varchar2(20) not null,
    active_login varchar2(20) not null,
    solved_request_id varchar2(100) not null,
    sold_request_id varchar2(100) not null,
    foreign key (passive_login)
    references passives(user_login)
    on delete cascade,
    foreign key (active_login)
    references actives(user_login)
    on delete cascade,
    foreign key (solved_request_id)
    references requests(id)
    on delete cascade,
    foreign key (sold_request_id)
    references requests(id)
    on delete cascade
);

create table news(
    title varchar2(20),
    content varchar2(4000) not null,
    media varchar2(250) not null,
    taken_from varchar2(50),
    created_at date not null,
    primary key (title, taken_from)
);

create table comments(
    id varchar(100) primary key,
    content varchar2(4000) not null,
    created_at date not null,
    news_title varchar2(20) not null,
    news_taken_from varchar2(50) not null,
    user_login varchar2(20) not null,
    foreign key (news_title, news_taken_from)
    references news(title, taken_from)
    on delete cascade,
    foreign key (user_login)
    references actives(user_login)
    on delete cascade
);

create table payments(
    user_login varchar2(20) primary key,
    money double precision not null,
    foreign key (user_login)
    references actives (user_login)
    on delete cascade
);

create table profiles(
    user_login varchar2(20) primary key,
    status varchar2(100) not null,
    biography varchar2(4000) not null,
    avatar varchar2(50) not null,
    currency integer not null,
    age integer not null,
    last_active date not null,
    foreign key (user_login)
    references actives(user_login)
    on delete cascade
);

create table locations(
    user_login varchar2(20) primary key,
    country varchar2(20) not null,
    city varchar2(20) not null,
    department varchar2(20) not null,
    gmt varchar2(10) not null,
    address varchar2(20) not null,
    zip_code varchar2(10) not null,
    foreign key (user_login)
    references actives(user_login)
    on delete cascade
);

create table contacts(
    user_login varchar2(20),
    link varchar2(50),
    name varchar2(10) not null,
    primary key (user_login, link),
    foreign key (user_login)
    references actives(user_login)
    on delete cascade
);

create table professionals(
    user_login varchar2(20) primary key,
    resume_pdf varchar2(50) not null,
    current_job varchar2(20) not null,
    current_org varchar2(20) not null,
    foreign key (user_login)
    references actives(user_login)
    on delete cascade
);

create table follows(
    follower_login varchar2(20),
    following_login varchar2(20),
    primary key (follower_login, following_login),
    foreign key (follower_login)
    references investors(user_login)
    on delete cascade,
    foreign key (following_login)
    references actives(user_login)
    on delete cascade
);