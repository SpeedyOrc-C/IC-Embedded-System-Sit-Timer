create table session
(
    key     varchar(256) not null
        constraint session_pk
            primary key,
    user_id varchar(64)  not null
        constraint session_user_user_id_fk
            references "user"
);
