--
-- PostgreSQL database dump
-- Hệ thống đặt hẹn thầy dạy lái xe và xe tập lái
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) DEFAULT '123456'::character varying NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255),
    phone character varying(20),
    address text,
    "isActive" boolean DEFAULT true,
    "createdAt" timestamp with time zone DEFAULT now(),
    "updatedAt" timestamp with time zone DEFAULT now()
);

ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

--
-- Name: mentors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mentors (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) DEFAULT '123456'::character varying NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255),
    phone character varying(20),
    license_number character varying(50),
    experience_years integer DEFAULT 0,
    price_per_hour double precision DEFAULT 0,
    "isActive" boolean DEFAULT true,
    "createdAt" timestamp with time zone DEFAULT now(),
    "updatedAt" timestamp with time zone DEFAULT now()
);

ALTER TABLE public.mentors OWNER TO postgres;

--
-- Name: mentors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mentors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.mentors_id_seq OWNER TO postgres;

--
-- Name: mentors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mentors_id_seq OWNED BY public.mentors.id;

--
-- Name: cars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cars (
    id integer NOT NULL,
    license_plate character varying(20) NOT NULL,
    brand character varying(100),
    model character varying(100),
    color character varying(50),
    year integer,
    status character varying(20) DEFAULT 'available'::character varying,
    price_per_hour double precision DEFAULT 0,
    "isActive" boolean DEFAULT true,
    "createdAt" timestamp with time zone DEFAULT now(),
    "updatedAt" timestamp with time zone DEFAULT now()
);

ALTER TABLE public.cars OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cars_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.cars_id_seq OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cars_id_seq OWNED BY public.cars.id;

--
-- Name: reserves; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reserves (
    id integer NOT NULL,
    user_id integer NOT NULL,
    mentor_id integer NOT NULL,
    car_id integer NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying,
    "createdAt" timestamp with time zone DEFAULT now(),
    "updatedAt" timestamp with time zone DEFAULT now()
);

ALTER TABLE public.reserves OWNER TO postgres;

--
-- Name: reserves_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reserves_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.reserves_id_seq OWNER TO postgres;

--
-- Name: reserves_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reserves_id_seq OWNED BY public.reserves.id;

--
-- Name: reserve_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reserve_details (
    id integer NOT NULL,
    reserve_id integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    price double precision DEFAULT 0,
    notes text,
    status character varying(20) DEFAULT 'pending'::character varying,
    actual_start_time timestamp with time zone,
    actual_end_time timestamp with time zone,
    "createdAt" timestamp with time zone DEFAULT now(),
    "updatedAt" timestamp with time zone DEFAULT now()
);

ALTER TABLE public.reserve_details OWNER TO postgres;

--
-- Name: reserve_details_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reserve_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.reserve_details_id_seq OWNER TO postgres;

--
-- Name: reserve_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reserve_details_id_seq OWNED BY public.reserve_details.id;

--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

--
-- Name: mentors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentors ALTER COLUMN id SET DEFAULT nextval('public.mentors_id_seq'::regclass);

--
-- Name: cars id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars ALTER COLUMN id SET DEFAULT nextval('public.cars_id_seq'::regclass);

--
-- Name: reserves id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserves ALTER COLUMN id SET DEFAULT nextval('public.reserves_id_seq'::regclass);

--
-- Name: reserve_details id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserve_details ALTER COLUMN id SET DEFAULT nextval('public.reserve_details_id_seq'::regclass);

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, name, email, phone, address, "isActive", "createdAt", "updatedAt") FROM stdin;
1	user1	123456	Nguyễn Văn A	user1@example.com	0901234567	123 Đường ABC, Quận 1, TP.HCM	t	2025-01-20 10:00:00.000000+00	2025-01-20 10:00:00.000000+00
\.

--
-- Data for Name: mentors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mentors (id, username, password, name, email, phone, license_number, experience_years, price_per_hour, "isActive", "createdAt", "updatedAt") FROM stdin;
1	mentor1	123456	Trần Văn B	mentor1@example.com	0912345678	DL-123456	5	200000	t	2025-01-20 10:00:00.000000+00	2025-01-20 10:00:00.000000+00
\.

--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars (id, license_plate, brand, model, color, year, status, price_per_hour, "isActive", "createdAt", "updatedAt") FROM stdin;
1	30A-12345	Toyota	Vios	Trắng	2023	available	150000	t	2025-01-20 10:00:00.000000+00	2025-01-20 10:00:00.000000+00
\.

--
-- Data for Name: reserves; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reserves (id, user_id, mentor_id, car_id, status, "createdAt", "updatedAt") FROM stdin;
\.

--
-- Data for Name: reserve_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reserve_details (id, reserve_id, start_time, end_time, price, notes, status, "createdAt", "updatedAt") FROM stdin;
\.

--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);

--
-- Name: mentors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mentors_id_seq', 1, true);

--
-- Name: cars_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cars_id_seq', 1, true);

--
-- Name: reserves_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reserves_id_seq', 1, true);

--
-- Name: reserve_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reserve_details_id_seq', 1, true);

--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

--
-- Name: mentors mentors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentors
    ADD CONSTRAINT mentors_pkey PRIMARY KEY (id);

--
-- Name: mentors mentors_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mentors
    ADD CONSTRAINT mentors_username_key UNIQUE (username);

--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (id);

--
-- Name: cars cars_license_plate_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_license_plate_key UNIQUE (license_plate);

--
-- Name: reserves reserves_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT reserves_pkey PRIMARY KEY (id);

--
-- Name: reserve_details reserve_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserve_details
    ADD CONSTRAINT reserve_details_pkey PRIMARY KEY (id);

--
-- Name: reserves fk_reserves_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT fk_reserves_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE SET NULL;

--
-- Name: reserves fk_reserves_mentor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT fk_reserves_mentor FOREIGN KEY (mentor_id) REFERENCES public.mentors(id) ON UPDATE CASCADE ON DELETE SET NULL;

--
-- Name: reserves fk_reserves_car; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserves
    ADD CONSTRAINT fk_reserves_car FOREIGN KEY (car_id) REFERENCES public.cars(id) ON UPDATE CASCADE ON DELETE SET NULL;

--
-- Name: reserve_details fk_reserve_details_reserve; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reserve_details
    ADD CONSTRAINT fk_reserve_details_reserve FOREIGN KEY (reserve_id) REFERENCES public.reserves(id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: idx_reserves_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reserves_user_id ON public.reserves USING btree (user_id);

--
-- Name: idx_reserves_mentor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reserves_mentor_id ON public.reserves USING btree (mentor_id);

--
-- Name: idx_reserves_car_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reserves_car_id ON public.reserves USING btree (car_id);

--
-- Name: idx_reserves_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reserves_status ON public.reserves USING btree (status);

--
-- Name: idx_reserve_details_reserve_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reserve_details_reserve_id ON public.reserve_details USING btree (reserve_id);

--
-- Name: idx_reserve_details_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reserve_details_status ON public.reserve_details USING btree (status);

--
-- Name: idx_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_username ON public.users USING btree (username);

--
-- Name: idx_mentors_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_mentors_username ON public.mentors USING btree (username);

--
-- Name: idx_cars_license_plate; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cars_license_plate ON public.cars USING btree (license_plate);

--
-- Name: idx_cars_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cars_status ON public.cars USING btree (status);

--
-- PostgreSQL database dump complete
--
