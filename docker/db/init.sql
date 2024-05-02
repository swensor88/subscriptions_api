CREATE USER subscription_user WITH PASSWORD 'S3cret';
CREATE DATABASE subscription_api;
ALTER DATABASE subscription_api OWNER TO subscription_user;


CREATE TABLE myapi.subscriptions
(
    id SERIAL PRIMARY KEY,
    industry character varying(255),
    source character varying(255),
    subcategory character varying(255)
);

ALTER TABLE IF EXISTS myapi.subscriptions
    OWNER to subscription_user;


CREATE TABLE myapi.subscriptions
(
    id SERIAL PRIMARY KEY,
    industry character varying(255),
    source character varying(255),
    subcategory character varying(255)
);

ALTER TABLE IF EXISTS myapi.subscriptions
    OWNER to subscription_user;


/*TODO: Add foreign key */