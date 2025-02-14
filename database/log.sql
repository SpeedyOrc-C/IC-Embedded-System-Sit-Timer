create table log
(
    device_id varchar(64)                                            not null
        constraint log_device_device_id_fk
            references device
            on delete cascade,
    time      timestamp default (now())::timestamp without time zone not null,
    existence boolean                                                not null,
    constraint log_pk
        primary key (time, device_id)
);
