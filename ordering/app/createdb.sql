create table transactions(
    id integer primary key,
    film_ids varchar,
    user_id integer,
    total_cost integer,
    time_stamp datetime default current_timestamp not null
);
