create table pairing
(
    new_device_id varchar(64)                                                                     not null
        constraint pairing_pk
            primary key,
    code          varchar(4)                                                                      not null
        constraint pairing_pk_2
            unique
        constraint "A code is a 4-digit hex number"
            check ((code)::text ~ '^[0-9a-f]{4}$'::text),
    expire_time   timestamp default ((now())::timestamp without time zone + '00:01:00'::interval) not null
);
