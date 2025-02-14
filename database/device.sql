create table device
(
    device_id varchar(64)                                              not null
        constraint device_pk
            primary key,
    owner     varchar(64)                                              not null
        constraint device_user_user_id_fk
            references "user",
    name      varchar(64) default 'Untitled Device'::character varying not null
        constraint "Name is not an empty string"
            check (length((name)::text) > 0)
);
