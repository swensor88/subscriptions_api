CREATE TABLE IF NOT EXISTS public.users
(
    id SERIAL PRIMARY KEY,
    email character varying(255),
    admin boolean,
    hashed_password character varying(255),
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now()
);

ALTER TABLE IF EXISTS public.users
    OWNER to subscription_user;


CREATE TABLE IF NOT EXISTS public.subscriptions
(
    id SERIAL PRIMARY KEY,
    user_id integer,
    industry character varying(255),
    source character varying(255),
    subcategory character varying(255),
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT subscriptions_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE IF EXISTS public.subscriptions
    OWNER to subscription_user;