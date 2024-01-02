create schema if not exists content;


create table if not exists content.film (
    id uuid primary key,
    title text not null,
    description text,
    creation_date date,
    rating float,
    type text not null,
    created timestamp with time zone,
    modified timestamp with time zone
); 

create table if not exists content.person (
    id uuid primary key,
    fullname text not null,
    description text,
    created timestamp with time zone,
    modified timestamp with time zone
); 

create table if not exists content.genre (
    id uuid primary key,
    name text not null,
    created timestamp with time zone,
    modified timestamp with time zone
); 


create table if not exists content.genre_film (
    id uuid primary key,
    genre_id uuid not null,
    film_id uuid not null,
    created timestamp with time zone,
    foreign key (genre_id) references content.genre(id),
    foreign key (film_id) references content.film(id)
); 

create table if not exists content.person_film (
    id uuid primary key,
    person_id uuid not null,
    film_id uuid not null,
    role text not null,
    created timestamp with time zone,
    foreign key (person_id) references content.person(id),
    foreign key (film_id) references content.film(id)
);
