create table "user"
(
    user_id varchar(64)  not null
        constraint user_pk
            primary key,
    salt    varchar(256) not null,
    hash    varchar(256) not null
);
