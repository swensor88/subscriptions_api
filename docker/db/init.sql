CREATE TABLE IF NOT EXISTS users
(
    id SERIAL PRIMARY KEY,
    email character varying(255),
    admin bit,
    hashed_password character varying(255)
);

ALTER TABLE IF EXISTS users
    OWNER to subscription_user;

CREATE TABLE IF NOT EXISTS subscriptions
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users (id),
    industry character varying(255),
    source character varying(255),
    subcategory character varying(255)
);

ALTER TABLE IF EXISTS subscriptions
    OWNER to subscription_user;
