--
-- PostgreSQL database dump
--

\restrict oHSTRIiKeULM5Ts2ItJzFa3lZ3PVwjNhpIHIAqtdYyJOAwQfWqXalRDlAA1J0kZ

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-06-28 00:14:17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 16580)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 5155 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 236 (class 1259 OID 25948)
-- Name: contract_counters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contract_counters (
    id integer NOT NULL,
    prefix character varying NOT NULL,
    last_number integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.contract_counters OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 25947)
-- Name: contract_counters_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contract_counters_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contract_counters_id_seq OWNER TO postgres;

--
-- TOC entry 5157 (class 0 OID 0)
-- Dependencies: 235
-- Name: contract_counters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contract_counters_id_seq OWNED BY public.contract_counters.id;


--
-- TOC entry 219 (class 1259 OID 16581)
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16586)
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_id_seq OWNER TO postgres;

--
-- TOC entry 5158 (class 0 OID 0)
-- Dependencies: 220
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- TOC entry 221 (class 1259 OID 16587)
-- Name: fields; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fields (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.fields OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16592)
-- Name: fields_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fields_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fields_id_seq OWNER TO postgres;

--
-- TOC entry 5159 (class 0 OID 0)
-- Dependencies: 222
-- Name: fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fields_id_seq OWNED BY public.fields.id;


--
-- TOC entry 223 (class 1259 OID 16593)
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16600)
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.locations_id_seq OWNER TO postgres;

--
-- TOC entry 5160 (class 0 OID 0)
-- Dependencies: 224
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- TOC entry 225 (class 1259 OID 16601)
-- Name: paths; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paths (
    id integer NOT NULL,
    description character varying NOT NULL
);


ALTER TABLE public.paths OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16608)
-- Name: paths_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.paths_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.paths_id_seq OWNER TO postgres;

--
-- TOC entry 5161 (class 0 OID 0)
-- Dependencies: 226
-- Name: paths_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.paths_id_seq OWNED BY public.paths.id;


--
-- TOC entry 234 (class 1259 OID 25920)
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refresh_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token_hash character varying NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    revoked boolean DEFAULT false
);


ALTER TABLE public.refresh_tokens OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 25919)
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.refresh_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.refresh_tokens_id_seq OWNER TO postgres;

--
-- TOC entry 5162 (class 0 OID 0)
-- Dependencies: 233
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.refresh_tokens_id_seq OWNED BY public.refresh_tokens.id;


--
-- TOC entry 238 (class 1259 OID 26004)
-- Name: request_before; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.request_before (
    id integer NOT NULL,
    customer character varying(200) NOT NULL,
    contract_num character varying(50) NOT NULL,
    contract_date date,
    eol_fio character varying(200) NOT NULL,
    user_id integer NOT NULL,
    "position" character varying(100),
    gender character varying(10),
    full_name character varying(200),
    field_id integer NOT NULL,
    check_in date NOT NULL,
    check_out date NOT NULL,
    days integer,
    room_id integer,
    comment text,
    status character varying(20) DEFAULT 'pending'::character varying,
    admin_comment text,
    created_at date DEFAULT CURRENT_DATE
);


ALTER TABLE public.request_before OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 26003)
-- Name: request_before_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.request_before_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.request_before_id_seq OWNER TO postgres;

--
-- TOC entry 5163 (class 0 OID 0)
-- Dependencies: 237
-- Name: request_before_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.request_before_id_seq OWNED BY public.request_before.id;


--
-- TOC entry 242 (class 1259 OID 26051)
-- Name: requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requests (
    id integer NOT NULL,
    customer_id integer NOT NULL,
    contract_num character varying(50) NOT NULL,
    contract_date date,
    eol_fio character varying(200) NOT NULL,
    user_id integer NOT NULL,
    "position" character varying(100),
    field_id integer NOT NULL,
    check_in date NOT NULL,
    check_out date NOT NULL,
    days integer,
    room_id integer,
    comment text,
    status character varying(20) DEFAULT 'pending'::character varying,
    admin_comment text,
    created_at timestamp with time zone DEFAULT CURRENT_DATE,
    resident_id integer
);


ALTER TABLE public.requests OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 26050)
-- Name: requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.requests_id_seq OWNER TO postgres;

--
-- TOC entry 5164 (class 0 OID 0)
-- Dependencies: 241
-- Name: requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.requests_id_seq OWNED BY public.requests.id;


--
-- TOC entry 240 (class 1259 OID 26039)
-- Name: residents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.residents (
    id integer NOT NULL,
    full_name character varying(200) NOT NULL,
    "position" character varying(100),
    gender character varying(10),
    birthday date,
    first_name character varying(100),
    last_name character varying(100),
    middle_name character varying(100)
);


ALTER TABLE public.residents OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 26038)
-- Name: residents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.residents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.residents_id_seq OWNER TO postgres;

--
-- TOC entry 5165 (class 0 OID 0)
-- Dependencies: 239
-- Name: residents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.residents_id_seq OWNED BY public.residents.id;


--
-- TOC entry 227 (class 1259 OID 16631)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16636)
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO postgres;

--
-- TOC entry 5166 (class 0 OID 0)
-- Dependencies: 228
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 229 (class 1259 OID 16637)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    id integer NOT NULL,
    room_number character varying,
    field_id integer,
    capacity integer DEFAULT 0,
    location_id integer,
    path_id integer,
    room_unique_id character varying(30),
    status integer
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16644)
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rooms_id_seq OWNER TO postgres;

--
-- TOC entry 5167 (class 0 OID 0)
-- Dependencies: 230
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_id_seq OWNED BY public.rooms.id;


--
-- TOC entry 231 (class 1259 OID 16645)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    role_id integer,
    field_id integer,
    resident_id integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16651)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5168 (class 0 OID 0)
-- Dependencies: 232
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4921 (class 2604 OID 25951)
-- Name: contract_counters id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contract_counters ALTER COLUMN id SET DEFAULT nextval('public.contract_counters_id_seq'::regclass);


--
-- TOC entry 4911 (class 2604 OID 16659)
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- TOC entry 4912 (class 2604 OID 16660)
-- Name: fields id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fields ALTER COLUMN id SET DEFAULT nextval('public.fields_id_seq'::regclass);


--
-- TOC entry 4913 (class 2604 OID 16661)
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- TOC entry 4914 (class 2604 OID 16662)
-- Name: paths id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paths ALTER COLUMN id SET DEFAULT nextval('public.paths_id_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 25923)
-- Name: refresh_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('public.refresh_tokens_id_seq'::regclass);


--
-- TOC entry 4923 (class 2604 OID 26007)
-- Name: request_before id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before ALTER COLUMN id SET DEFAULT nextval('public.request_before_id_seq'::regclass);


--
-- TOC entry 4927 (class 2604 OID 26054)
-- Name: requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests ALTER COLUMN id SET DEFAULT nextval('public.requests_id_seq'::regclass);


--
-- TOC entry 4926 (class 2604 OID 26042)
-- Name: residents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.residents ALTER COLUMN id SET DEFAULT nextval('public.residents_id_seq'::regclass);


--
-- TOC entry 4915 (class 2604 OID 16665)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 4916 (class 2604 OID 16666)
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN id SET DEFAULT nextval('public.rooms_id_seq'::regclass);


--
-- TOC entry 4918 (class 2604 OID 16667)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5143 (class 0 OID 25948)
-- Dependencies: 236
-- Data for Name: contract_counters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contract_counters (id, prefix, last_number) FROM stdin;
1	ШИН	122
2	ЗАП	3
\.


--
-- TOC entry 5126 (class 0 OID 16581)
-- Dependencies: 219
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (id, name) FROM stdin;
1	ООО «ГПНЭС»
2	—
3	ФГБУ "ЦЛАТИ по СФО"
483	Партнеры Томск
484	ГПН-В
485	ГПНВ
486	ГПН-Энергосистемы
487	ИнТех
488	УТТ-Югра
489	ТИТЦ
490	МСБ
491	ООО "Газпромнефть-Снабжение"
492	ГПН-Снабжение
493	ГПН-Автоматизация
494	ГПНЭС ООО "ЯСЦ"
495	СибМедЦентр
496	ООО "Автоделюкс"
497	ООО " Нефтеспас"
498	 Сервис центр ЭПУ
499	ГПН-ИТО
500	ООО " Уралтрубопроводстройпроект"
501	ИП Кураков
502	 
503	ООО ЧОП "Отечество-С"
504	ООО "УТТ-Югра"
505	ООО " Русэнерго"
506	АНО ДПО "ЮУЦ"
507	Сибирское управление Росехнадзора
508	ФГБУ "ЦЛАТИ по СФО" 
509	ООО "Газпромнефть  сервисные технологии"
510	ФБУ Омский ЦСМ
511	ООО "Газпромнефть Бизнес сервис"
512	РК " Нефтесервис"
513	ИП Кураков (ТК СПП)
514	ООО "БСК ГРАНД"
515	ООО   "ТрансСервис"
516	ФБУ Томский ЦСМ
517	Сервис центр ЭПУ
518	АО "НПИИЭК"
519	ООО "Сибирская Экспертная Компания"
520	ООО НПФ "Пакер"
521	ООО "ТрансСервис"
522	ООО ТПНВО "СИАМ"
523	ООО " ВЕТЭК"
524	ООО " Газпромгазобезопасность"
525	Департамент охотничьего и рыбного хозяйства Томской области
526	ООО "Томская инжиниринговая компания"
527	ООО "Инженерный центр  Энергосервис"
528	ИП Коротков
529	АНО ДПО "Двипраз"
530	=$I$87
531	ООО "Аналитпроф"
532	ООО НПП  " Петролайн-А"
533	ООО " Нефтемодульстрой"
534	ООО "БСК" Гранд"
535	АО "ГазпромДобычаТомск"
536	ООО "Техснабкомплект"
537	ООО НПФ " ТеплоЭнергоПром"
538	ПАО "Ростелеком"
539	ООО "Газпромгазобезопасность"
540	Буртехнология
541	ООО "Газпромнефть сервисные технологии"
542	ООО "Газпромнефть Ямал"
543	ООО "ГАЦ ЗСР НАКС"
544	ООО "Инженерный центр Энергосервис"
545	ООО "Нефтемодульстрой"
546	ООО "Нефтеспас"
547	ООО "НИЦ"
548	ООО "НПО Мир"
549	ООО "НьютехВелл Сервис"
550	ООО "Русэнерго"
551	ООО "Уралтрубопроводстройпроект"
552	ПАО Газпром нефть
553	РК "Нефтесервис"
554	ФГБУ 
555	ООО 
556	ЗАО "СтройИнвест"
557	ГБОУ "Школа №10"
558	ООО
559	ИП Кузнецов
560	ООО "Рога и Копыта"
561	ОАО "Энергосбыт"
574	ООО «НВИАЙ СОЛЮШЕНС»
575	ООО «Газпромнефть-Восток»
576	АО «Томскнефть»
577	ООО Тест
578	(пусто)
\.


--
-- TOC entry 5128 (class 0 OID 16587)
-- Dependencies: 221
-- Data for Name: fields; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fields (id, name) FROM stdin;
1	Шингинское
2	Западно-Лугинецкое
3	Урманское
4	Ю.З.Крапивинского
10	Каменское
14	Шингинское месторождение
15	Ванкорское
16	(пусто)
\.


--
-- TOC entry 5130 (class 0 OID 16593)
-- Dependencies: 223
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations (id, name) FROM stdin;
1	Общежитие
2	Вагон
51	ОБЩЕЖИТИЕ
52	ВАГОН
53	ВАГОНЫ
54	АБЖК
55	НОВОЕ ОБЩЕЖИТИЕ
56	ОБЩЕЖИТИЕ УПН
\.


--
-- TOC entry 5132 (class 0 OID 16601)
-- Dependencies: 225
-- Data for Name: paths; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paths (id, description) FROM stdin;
1	1 этаж левое крыло
245	1 этаж правое крыло (ПО)
246	2 этаж левое крыло
247	2 этаж, правое крыло
248	1 этаж, левое крыло
249	1
250	3
251	2
252	5
253	
254	Без пути
\.


--
-- TOC entry 5141 (class 0 OID 25920)
-- Dependencies: 234
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refresh_tokens (id, user_id, token_hash, expires_at, revoked) FROM stdin;
3	9	258fcbf89d4b2752153e42ed438b531475901ba8a192e371db378fc2c97ccb6e	2026-06-11 02:34:10	t
5	9	f87830b2235f31f1445768170e5e792b5be0af01344575fe34d12d7a9193d5fd	2026-06-11 03:35:28	t
7	9	8ee72d95048789b7128ecbef10104bc6b96f198b730d2a55e2179417fd8d1141	2026-06-11 03:43:10	t
11	9	73c05eb1b42f084005a9b7a471b9aa428cce646b18d298e1c227e8d9c3277eaf	2026-06-19 06:00:25	t
14	9	c2ef262e6f7885b34c7f75e17fc6162865f21db3c1bf7171e2184cf68425c043	2026-06-21 06:50:54	t
1	1	c4d875958904ba2c3275267b5494c7bb3e2d7c46c8cc993cec993924c267a3e9	2026-06-10 00:40:47	t
2	1	69d56117d3ccbfe7f84108d68d3f149a130d21b5265d2354baefcba7aa2eb6d9	2026-06-10 16:02:32	t
4	1	bf1c4cee5cabe6927d3ac5f74063b6bbb8cd091dfe62931cd11870cc6015d222	2026-06-11 02:52:50	t
6	1	7f2fe644d962f87438e27a293835b6e2c616bd711e9a6e73d3850d07839b27e0	2026-06-11 03:42:39	t
8	1	3fd846e1ed72eac4849f031877ff3a9952e6237b7af71452dece60d3d6fa9d48	2026-06-19 03:01:18	t
9	1	707f429535f19c905b338e684bc47d02a2f42328e6194ce5bd876cc91527bb31	2026-06-19 03:23:47	t
10	1	7a40c68dbfe2a4681fa0ee801c9f5a7c3c57981b5ac29424f1cc77cc99d98dcb	2026-06-19 05:38:44	t
16	1	07d90e9d81e359a4cf3223f670fa79d80d025f12155c08c834fe8044ce2c7c39	2026-06-21 07:27:33	t
19	1	ef637915f0693b482e91a48cb3dfea47902d6262564573769af8238cc1a20469	2026-06-24 16:36:45	t
20	1	ba8c8ac75bc82b779b9caa06c1c5f660edafff29bc1f3763235452f400f7562c	2026-07-03 17:49:23	t
17	9	3c9c26bb31672cefacf93e1af1cde921988fdba3cb22cbc55db8209e1113fade	2026-06-21 11:10:27	f
12	1	fa1fc3dab6aaf4fd1918f3571a2d8548dd9e0893595abb3a865bde8e51a3b923	2026-06-19 06:02:00	t
13	1	240ebbcc09349c0f1b6460e664d7a90f7de2b8270fd179984e7b63288e5c3650	2026-06-19 06:53:17	t
21	1	b58279718cb3bcb08bd46f14d09b0264fcce72630fac2253f04d8481cc610938	2026-07-05 00:05:08	f
15	1	45eecb4b241165f2c57a9326a25061ba470a77512d7529d2571819020bfaba01	2026-06-21 06:51:54	t
18	1	32d7f4e046a5c7b67f69470f5913de318a046893e679fe3521d4ed995b515c90	2026-06-21 11:12:39	t
\.


--
-- TOC entry 5145 (class 0 OID 26004)
-- Dependencies: 238
-- Data for Name: request_before; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.request_before (id, customer, contract_num, contract_date, eol_fio, user_id, "position", gender, full_name, field_id, check_in, check_out, days, room_id, comment, status, admin_comment, created_at) FROM stdin;
1	ООО «Газпромнефть-Восток»	ГВ-001	2026-01-10	Кузнецов Андрей Владимирович	1	Инженер	male	Сидоров Максим Петрович	1	2026-02-01	2026-03-01	28	1	Гостевая заявка	approved	\N	2026-01-05
2	ООО «Газпромнефть-Восток»	ГВ-002	2026-01-15	Кузнецов Андрей Владимирович	1	Лаборант	female	Козлова Анна Викторовна	1	2026-02-05	2026-03-05	28	2	\N	approved	\N	2026-01-10
3	ООО «Газпромнефть-Восток»	ГВ-003	2026-02-01	Кузнецов Андрей Владимирович	1	Техник	male	Морозов Денис Андреевич	2	2026-03-01	2026-03-29	28	17	\N	approved	\N	2026-02-01
4	АО «Томскнефть»	ТН-001	2026-02-10	Кузнецов Андрей Владимирович	1	Геолог	female	Гаврилова Елена Станиславовна	2	2026-03-10	2026-04-07	28	18	Гостевая заявка по обмену опытом	approved	\N	2026-02-05
5	ООО «Газпромнефть-Восток»	ГВ-004	2026-02-20	Петрова Ольга Сергеевна	1	Машинист	male	Никитин Артём Олегович	3	2026-03-20	2026-04-17	28	29	\N	approved	\N	2026-02-15
6	ООО «Газпромнефть-Восток»	ГВ-005	2026-03-01	Петрова Ольга Сергеевна	1	Лаборант	female	Федотова Татьяна Игоревна	1	2026-04-01	2026-05-01	30	3	\N	approved	\N	2026-03-01
7	ООО «Газпромнефть-Восток»	ГВ-006	2026-03-05	Петрова Ольга Сергеевна	1	Электромонтер	male	Васильев Роман Валерьевич	2	2026-04-05	2026-05-03	28	19	\N	approved	\N	2026-03-01
8	ООО «Газпромнефть-Восток»	ГВ-007	2026-03-10	Петрова Ольга Сергеевна	1	Кладовщик	female	Смирнова Ольга Александровна	3	2026-04-10	2026-05-10	30	30	Гостевая заявка	approved	\N	2026-03-05
10	ООО «Газпромнефть-Восток»	ГВ-009	2026-03-20	Михайлов Дмитрий Алексеевич	1	Инженер	female	Ковалёва Марина Викторовна	2	2026-04-20	2026-05-20	30	20	\N	approved	\N	2026-03-15
11	ООО «Газпромнефть-Восток»	ГВ-010	2026-04-01	Михайлов Дмитрий Алексеевич	1	Бурильщик	male	Сорокин Владислав Артурович	3	2026-05-01	2026-05-31	30	31	\N	approved	\N	2026-04-01
12	ООО «Газпромнефть-Восток»	ГВ-011	2026-04-05	Михайлов Дмитрий Алексеевич	1	Механик	female	Зайцева Вероника Павловна	1	2026-05-05	2026-06-04	30	5	\N	approved	\N	2026-04-01
13	ООО «Газпромнефть-Восток»	ГВ-012	2026-04-10	Васильева Елена Игоревна	1	Водитель автомобиля	male	Белов Геннадий Сергеевич	2	2026-05-10	2026-06-09	30	21	\N	approved	\N	2026-04-05
14	ООО «Газпромнефть-Восток»	ГВ-013	2026-04-15	Васильева Елена Игоревна	1	Оператор ДНГ	female	Дмитриева Анастасия Ивановна	3	2026-05-15	2026-06-14	30	32	Заявка от партнёра	approved	\N	2026-04-10
15	ООО «Газпромнефть-Восток»	ГВ-014	2026-04-20	Васильева Елена Игоревна	1	Мастер участка	male	Филиппов Илья Романович	1	2026-05-20	2026-06-19	30	6	\N	approved	\N	2026-04-15
16	ООО «Газпромнефть-Восток»	ГВ-015	2026-05-01	Васильева Елена Игоревна	1	Техник	female	Калинина Юлия Михайловна	2	2026-06-01	2026-07-01	30	22	\N	approved	\N	2026-05-01
17	ООО «Газпромнефть-Восток»	ГВ-016	2026-05-05	Соколов Максим Петрович	1	Электрогазосварщик	male	Медведев Станислав Аркадьевич	3	2026-06-05	2026-07-05	30	33	\N	approved	\N	2026-05-01
18	ООО «Газпромнефть-Восток»	ГВ-017	2026-05-10	Соколов Максим Петрович	1	Начальник смены	female	Гордеева Дарья Валерьевна	1	2026-06-10	2026-07-10	30	7	\N	approved	\N	2026-05-05
20	ООО «Газпромнефть-Восток»	ГВ-019	2026-05-20	Соколов Максим Петрович	1	Лаборант	female	Ершова Полина Алексеевна	3	2026-06-20	2026-07-20	30	34	\N	approved	\N	2026-05-15
21	ООО «Газпромнефть-Восток»	ГВ-020	2026-06-01	Федорова Анна Викторовна	1	Машинист	male	Афанасьев Егор Станиславович	1	2026-07-01	2026-07-29	28	8	\N	approved	\N	2026-06-01
22	ООО «Газпромнефть-Восток»	ГВ-021	2026-06-05	Федорова Анна Викторовна	1	Инженер	female	Крылова Валерия Сергеевна	2	2026-07-05	2026-08-02	28	24	\N	approved	\N	2026-06-01
23	ООО «Газпромнефть-Восток»	ГВ-022	2026-06-10	Федорова Анна Викторовна	1	Слесарь-ремонтник	male	Лукин Марк Петрович	3	2026-07-10	2026-08-07	28	35	\N	approved	\N	2026-06-05
25	ООО «Газпромнефть-Восток»	ГВ-024	2026-06-20	Егоров Артём Александрович	1	Водитель автомобиля	male	Маслов Артур Геннадьевич	2	2026-07-20	2026-08-17	28	25	Срочная заявка	approved	\N	2026-06-15
26	ООО «Газпромнефть-Восток»	ГВ-025	2026-07-01	Егоров Артём Александрович	1	Бурильщик	female	Кабанова Алина Руслановна	3	2026-08-01	2026-08-29	28	36	\N	approved	\N	2026-07-01
29	ООО «Газпромнефть-Восток»	ГВ-028	2026-07-15	Никитина Татьяна Станиславовна	1	Техник	female	Бирюкова Кристина Вячеславовна	3	2026-08-15	2026-09-12	28	37	\N	approved	\N	2026-07-10
30	ООО «Газпромнефть-Восток»	ГВ-029	2026-08-01	Никитина Татьяна Станиславовна	1	Мастер участка	male	Агафонов Савелий Артемьевич	1	2026-09-01	2026-10-01	30	11	\N	approved	\N	2026-08-01
31	ООО «Газпромнефть-Восток»	ГВ-030	2026-08-05	Никитина Татьяна Станиславовна	1	Начальник смены	female	Рябова Василиса Даниловна	2	2026-09-05	2026-10-05	30	27	\N	approved	\N	2026-08-01
33	ООО «Газпромнефть-Восток»	ГВ-032	2026-08-15	Григорьев Павел Николаевич	1	Геолог	female	Горшкова Злата Арсеньевна	1	2026-09-15	2026-10-15	30	12	Заявка на стажировку	approved	\N	2026-08-10
34	ООО «Газпромнефть-Восток»	ГВ-033	2026-09-01	Григорьев Павел Николаевич	1	Водитель автомобиля	male	Зуев Мирон Борисович	2	2026-10-01	2026-11-15	45	28	\N	approved	\N	2026-09-01
35	ООО «Газпромнефть-Восток»	ГВ-034	2026-09-05	Григорьев Павел Николаевич	1	Лаборант	female	Харитонова Ярослава Даниловна	3	2026-10-05	2026-11-19	45	\N	Заявка без номера	rejected	Нет свободных мест на запрошенный период	2026-09-01
36	ООО «Газпромнефть-Восток»	ГВ-035	2026-09-10	Григорьев Павел Николаевич	1	Слесарь-ремонтник	male	Гусев Адриан Данилович	1	2026-10-10	2026-11-24	45	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-09-05
38	ООО «Газпромнефть-Восток»	ГВ-037	2026-10-01	Семенова Виктория Валерьевна	1	Оператор ДНГ	female	Филимонова Алиса Эдуардовна	3	2026-11-01	2026-12-16	45	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-10-01
39	ООО «Газпромнефть-Восток»	ГВ-038	2026-10-05	Семенова Виктория Валерьевна	1	Машинист	male	Бобров Платон Никитич	1	2026-11-05	2026-12-20	45	13	\N	approved	\N	2026-10-01
41	ООО «Газпромнефть-Восток»	ГВ-040	2026-10-15	Кузнецов Андрей Владимирович	1	Геолог	male	Воробьёв Демьян Тимофеевич	3	2026-11-15	2026-12-30	45	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-10-10
42	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Инженер	\N	Поцелуев Артемий Сергеевич	3	2026-04-28	2026-04-28	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
43	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Галкин Виктор Алексеевич	3	2026-04-28	2026-04-28	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
44	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Калашников Илья Николаевич	3	2026-04-28	2026-04-28	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
45	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Инженер	\N	Поцелуев Артемий Сергеевич	3	2026-04-28	2026-05-28	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
46	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Галкин Виктор Алексеевич	3	2026-04-28	2026-05-29	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
47	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Калашников Илья Николаевич	3	2026-04-28	2026-05-30	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
48	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Инженер	\N	Поцелуев Артемий Сергеевич	3	2026-04-28	2026-05-28	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
49	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Галкин Виктор Алексеевич	3	2026-04-28	2026-05-29	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
50	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Калашников Илья Николаевич	3	2026-04-28	2026-05-30	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
51	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Инженер	\N	Поцелуев Артемий Сергеевич	3	2026-04-28	2026-05-28	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
52	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Галкин Виктор Алексеевич	3	2026-04-28	2026-05-29	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
53	ООО «НВИАЙ СОЛЮШЕНС»	ВСТ-24/09000/00289/Р	2024-12-28	Шмагаренко АН	1	Техник	\N	Калашников Илья Николаевич	3	2026-04-28	2026-05-30	29	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-18
54	ООО «Газпромнефть-Восток»	ГВ-101	2026-01-05	Кузнецов Андрей Владимирович	1	Техник	male	Гостевой Сидоров Иван Петрович	1	2026-01-10	2026-02-07	28	4	Гость занимает свободный блок	approved	\N	2026-01-05
55	ООО «Газпромнефть-Восток»	ГВ-102	2026-01-06	Петрова Ольга Сергеевна	1	Инженер	female	Гостевая Орлова Светлана	1	2026-01-15	2026-02-12	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-01-06
56	АО «Томскнефть»	ТН-101	2026-02-01	Соколов Максим Петрович	1	Геолог	male	Гость Петров Аркадий	1	2026-02-05	2026-03-05	28	8	Занимаем свободный блок	approved	\N	2026-02-01
57	АО «Томскнефть»	ТН-102	2026-02-02	Соколов Максим Петрович	1	Механик	male	Гость Захаров Илья	1	2026-02-10	2026-03-10	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-02-02
58	ООО «Газпромнефть-Восток»	ГВ-103	2026-09-15	Никитина Татьяна Станиславовна	1	Бурильщик	male	Гость Сафин Рустем	1	2026-11-12	2026-12-10	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-09-15
59	ООО «Газпромнефть-Восток»	ГВ-104	2026-03-01	Федорова Анна Викторовна	1	Оператор ДНГ	female	Гостевая Фёдорова Марина	2	2026-03-05	2026-04-02	28	18	Свободный блок	approved	\N	2026-03-01
60	ООО «Газпромнефть-Восток»	ГВ-105	2026-03-02	Федорова Анна Викторовна	1	Электромонтер	male	Гость Кукушкин Пётр	2	2026-03-10	2026-04-07	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-03-02
61	ООО «Газпромнефть-Восток»	ГВ-106	2026-04-01	Егоров Артём Александрович	1	Слесарь-ремонтник	male	Гость Семёнов Рушан	3	2026-04-05	2026-05-03	28	30	Свободный блок	approved	\N	2026-04-01
62	ООО «Газпромнефть-Восток»	ГВ-107	2026-04-02	Егоров Артём Александрович	1	Машинист	male	Гость Закиров Ильдар	3	2026-04-10	2026-05-08	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-04-02
63	ООО «Газпромнефть-Восток»	ГВ-108	2026-08-10	Григорьев Павел Николаевич	1	Водитель автомобиля	male	Гость Яковлев Марат	3	2026-10-10	2026-11-07	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-08-10
64	ООО «Газпромнефть-Восток»	ГВ-109	2026-05-20	Михайлов Дмитрий Алексеевич	1	Геолог	male	Гость Нигматуллин Булат	1	2026-07-05	2026-08-02	28	4	Летний период	approved	\N	2026-05-20
67	ООО «Газпромнефть-Восток»	ШИН-77	\N	Гость Абдуллин Роман	1	Техник	\N	Гость Абдуллин Роман	1	2026-04-05	2026-05-05	30	83	\N	approved	\N	2026-06-19
68	ООО «Газпромнефть-Восток»	ШИН-78	\N	Гость Кузнецов Андрей	1	Техник	\N	Гость Кузнецов Андрей	1	2026-05-01	2026-05-31	30	88	\N	approved	\N	2026-06-19
69	ООО «Газпромнефть-Восток»	ШИН-87	\N	Козлов Павел	1	Техник	\N	Козлов Павел	1	2026-04-01	2026-04-30	29	100	\N	approved	\N	2026-06-19
65	ООО «Газпромнефть-Восток»	ГВ-110	2026-11-01	Васильева Елена Игоревна	1	Электрогазосварщик	male	Гость Хабибуллин Айрат	3	2026-11-05	2026-12-03	28	34	Последний блок	rejected	\N	2026-11-01
\.


--
-- TOC entry 5149 (class 0 OID 26051)
-- Dependencies: 242
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requests (id, customer_id, contract_num, contract_date, eol_fio, user_id, "position", field_id, check_in, check_out, days, room_id, comment, status, admin_comment, created_at, resident_id) FROM stdin;
547	1	ШИН-001	2025-11-10	Кузнецов Андрей Владимирович	1	\N	1	2026-01-05	2026-02-02	28	1	\N	approved	\N	2025-11-10 08:15:00+07	1
548	1	ШИН-002	2025-12-15	Кузнецов Андрей Владимирович	1	\N	1	2026-02-10	2026-03-10	28	1	\N	approved	\N	2025-12-15 09:20:00+07	26
549	1	ШИН-003	2026-01-10	Кузнецов Андрей Владимирович	1	\N	1	2026-03-20	2026-04-17	28	1	\N	approved	\N	2026-01-10 10:30:00+07	51
550	1	ШИН-004	2026-03-01	Кузнецов Андрей Владимирович	1	\N	1	2026-05-01	2026-05-31	30	1	Продление по согласованию	approved	\N	2026-03-01 11:00:00+07	76
551	1	ШИН-005	2025-11-12	Петрова Ольга Сергеевна	1	\N	1	2026-01-05	2026-02-02	28	2	\N	approved	\N	2025-11-12 08:45:00+07	2
553	1	ШИН-007	2026-01-15	Петрова Ольга Сергеевна	1	\N	1	2026-03-22	2026-04-19	28	2	\N	approved	\N	2026-01-15 10:05:00+07	52
554	1	ШИН-008	2026-03-05	Петрова Ольга Сергеевна	1	\N	1	2026-05-03	2026-06-02	30	2	\N	approved	\N	2026-03-05 11:20:00+07	77
555	1	ШИН-009	2025-11-14	Михайлов Дмитрий Алексеевич	1	\N	1	2026-01-07	2026-02-04	28	3	\N	approved	\N	2025-11-14 08:30:00+07	3
556	1	ШИН-010	2025-12-20	Михайлов Дмитрий Алексеевич	1	\N	1	2026-02-15	2026-03-15	28	3	\N	approved	\N	2025-12-20 09:25:00+07	28
557	1	ШИН-011	2026-01-18	Михайлов Дмитрий Алексеевич	1	\N	1	2026-03-25	2026-04-22	28	3	\N	approved	\N	2026-01-18 10:40:00+07	53
558	1	ШИН-012	2026-03-10	Михайлов Дмитрий Алексеевич	1	\N	1	2026-05-10	2026-06-09	30	3	Без замечаний	approved	\N	2026-03-10 11:35:00+07	78
559	1	ШИН-013	2025-11-16	Васильева Елена Игоревна	1	\N	1	2026-01-10	2026-02-07	28	4	\N	approved	\N	2025-11-16 08:55:00+07	4
560	1	ШИН-014	2025-12-22	Васильева Елена Игоревна	1	\N	1	2026-02-18	2026-03-18	28	4	\N	approved	\N	2025-12-22 09:40:00+07	29
561	1	ШИН-015	2026-01-20	Васильева Елена Игоревна	1	\N	1	2026-03-28	2026-04-25	28	4	\N	approved	\N	2026-01-20 10:50:00+07	54
562	1	ШИН-016	2026-03-15	Васильева Елена Игоревна	1	\N	1	2026-05-15	2026-06-14	30	4	\N	approved	\N	2026-03-15 11:45:00+07	79
563	1	ШИН-017	2025-11-18	Соколов Максим Петрович	1	\N	1	2026-01-12	2026-02-09	28	5	\N	approved	\N	2025-11-18 08:10:00+07	5
564	1	ШИН-018	2025-12-25	Соколов Максим Петрович	1	\N	1	2026-02-20	2026-03-20	28	5	\N	approved	\N	2025-12-25 09:15:00+07	30
565	1	ШИН-019	2026-02-01	Соколов Максим Петрович	1	\N	1	2026-04-01	2026-04-29	28	5	\N	approved	\N	2026-02-01 10:25:00+07	55
566	1	ШИН-020	2026-03-20	Соколов Максим Петрович	1	\N	1	2026-05-20	2026-06-19	30	5	\N	approved	\N	2026-03-20 11:55:00+07	80
567	1	ШИН-021	2025-11-20	Федорова Анна Викторовна	1	\N	1	2026-01-15	2026-02-12	28	6	\N	approved	\N	2025-11-20 08:35:00+07	6
568	1	ШИН-022	2025-12-28	Федорова Анна Викторовна	1	\N	1	2026-02-22	2026-03-22	28	6	\N	approved	\N	2025-12-28 09:50:00+07	31
569	1	ШИН-023	2026-02-05	Федорова Анна Викторовна	1	\N	1	2026-04-05	2026-05-03	28	6	\N	approved	\N	2026-02-05 10:15:00+07	56
570	1	ШИН-024	2026-03-25	Федорова Анна Викторовна	1	\N	1	2026-05-25	2026-06-24	30	6	\N	approved	\N	2026-03-25 12:05:00+07	81
571	1	ШИН-025	2025-11-22	Егоров Артём Александрович	1	\N	1	2026-01-18	2026-02-15	28	7	\N	approved	\N	2025-11-22 08:20:00+07	7
572	1	ШИН-026	2025-12-30	Егоров Артём Александрович	1	\N	1	2026-02-25	2026-03-25	28	7	\N	approved	\N	2025-12-30 09:30:00+07	32
573	1	ШИН-027	2026-02-08	Егоров Артём Александрович	1	\N	1	2026-04-08	2026-05-06	28	7	\N	approved	\N	2026-02-08 10:10:00+07	57
575	1	ШИН-029	2025-11-24	Никитина Татьяна Станиславовна	1	\N	1	2026-01-20	2026-02-17	28	8	\N	approved	\N	2025-11-24 08:40:00+07	8
576	1	ШИН-030	2026-01-02	Никитина Татьяна Станиславовна	1	\N	1	2026-02-28	2026-03-28	28	8	\N	approved	\N	2026-01-02 09:55:00+07	33
577	1	ШИН-031	2026-02-12	Никитина Татьяна Станиславовна	1	\N	1	2026-04-12	2026-05-10	28	8	\N	approved	\N	2026-02-12 10:35:00+07	58
578	1	ШИН-032	2026-04-05	Никитина Татьяна Станиславовна	1	\N	1	2026-06-05	2026-07-05	30	8	\N	approved	\N	2026-04-05 12:25:00+07	83
579	1	ШИН-033	2025-11-26	Григорьев Павел Николаевич	1	\N	1	2026-01-22	2026-02-19	28	9	\N	approved	\N	2025-11-26 08:50:00+07	9
580	1	ШИН-034	2026-01-05	Григорьев Павел Николаевич	1	\N	1	2026-03-02	2026-03-30	28	9	\N	approved	\N	2026-01-05 10:05:00+07	34
581	1	ШИН-035	2026-02-15	Григорьев Павел Николаевич	1	\N	1	2026-04-15	2026-05-13	28	9	\N	approved	\N	2026-02-15 11:10:00+07	59
582	1	ШИН-036	2026-04-10	Григорьев Павел Николаевич	1	\N	1	2026-06-10	2026-07-10	30	9	\N	approved	\N	2026-04-10 12:35:00+07	84
583	1	ШИН-037	2025-11-28	Семенова Виктория Валерьевна	1	\N	1	2026-01-25	2026-02-22	28	10	\N	approved	\N	2025-11-28 09:00:00+07	10
584	1	ШИН-038	2026-01-08	Семенова Виктория Валерьевна	1	\N	1	2026-03-05	2026-04-02	28	10	\N	approved	\N	2026-01-08 10:15:00+07	35
585	1	ШИН-039	2026-02-20	Семенова Виктория Валерьевна	1	\N	1	2026-04-20	2026-05-18	28	10	\N	approved	\N	2026-02-20 11:20:00+07	60
586	1	ШИН-040	2026-04-15	Семенова Виктория Валерьевна	1	\N	1	2026-06-15	2026-07-15	30	10	\N	approved	\N	2026-04-15 12:45:00+07	85
588	1	ШИН-042	2026-01-10	Кузнецов Андрей Владимирович	1	\N	1	2026-03-08	2026-04-05	28	11	\N	approved	\N	2026-01-10 10:25:00+07	36
589	1	ШИН-043	2026-02-25	Кузнецов Андрей Владимирович	1	\N	1	2026-04-25	2026-05-23	28	11	\N	approved	\N	2026-02-25 11:30:00+07	61
590	1	ШИН-044	2026-04-20	Кузнецов Андрей Владимирович	1	\N	1	2026-06-20	2026-07-20	30	11	\N	approved	\N	2026-04-20 12:55:00+07	86
592	1	ШИН-046	2026-01-12	Петрова Ольга Сергеевна	1	\N	1	2026-03-10	2026-04-07	28	12	\N	approved	\N	2026-01-12 10:35:00+07	37
593	1	ШИН-047	2026-02-28	Петрова Ольга Сергеевна	1	\N	1	2026-04-28	2026-05-26	28	12	\N	approved	\N	2026-02-28 11:40:00+07	62
595	1	ШИН-049	2025-12-05	Михайлов Дмитрий Алексеевич	1	\N	1	2026-02-01	2026-03-01	28	13	\N	approved	\N	2025-12-05 09:30:00+07	13
596	1	ШИН-050	2026-01-15	Михайлов Дмитрий Алексеевич	1	\N	1	2026-03-15	2026-04-12	28	13	\N	approved	\N	2026-01-15 10:45:00+07	38
597	1	ШИН-051	2026-03-05	Михайлов Дмитрий Алексеевич	1	\N	1	2026-05-05	2026-06-02	28	13	\N	approved	\N	2026-03-05 11:50:00+07	63
598	1	ШИН-052	2026-05-01	Михайлов Дмитрий Алексеевич	1	\N	1	2026-07-01	2026-07-29	28	13	\N	approved	\N	2026-05-01 13:15:00+07	88
599	1	ШИН-053	2025-12-07	Васильева Елена Игоревна	1	\N	1	2026-02-03	2026-03-03	28	14	\N	approved	\N	2025-12-07 09:40:00+07	14
600	1	ШИН-054	2026-01-18	Васильева Елена Игоревна	1	\N	1	2026-03-18	2026-04-15	28	14	\N	approved	\N	2026-01-18 10:55:00+07	39
601	1	ШИН-055	2026-03-10	Васильева Елена Игоревна	1	\N	1	2026-05-10	2026-06-07	28	14	\N	approved	\N	2026-03-10 12:00:00+07	64
603	1	ШИН-057	2025-12-09	Соколов Максим Петрович	1	\N	1	2026-02-05	2026-03-05	28	15	\N	approved	\N	2025-12-09 09:50:00+07	15
604	1	ШИН-058	2026-01-22	Соколов Максим Петрович	1	\N	1	2026-03-22	2026-04-19	28	15	\N	approved	\N	2026-01-22 11:05:00+07	40
605	1	ШИН-059	2026-03-15	Соколов Максим Петрович	1	\N	1	2026-05-15	2026-06-12	28	15	\N	approved	\N	2026-03-15 12:10:00+07	65
606	1	ШИН-060	2026-05-10	Соколов Максим Петрович	1	\N	1	2026-07-10	2026-08-07	28	15	Заявка отклонена по инициативе заказчика	rejected	Отказ: несоответствие требованиям безопасности	2026-05-10 13:35:00+07	90
607	1	ШИН-061	2025-12-11	Федорова Анна Викторовна	1	\N	1	2026-02-08	2026-03-08	28	16	\N	approved	\N	2025-12-11 10:00:00+07	16
608	1	ШИН-062	2026-01-25	Федорова Анна Викторовна	1	\N	1	2026-03-25	2026-04-22	28	16	\N	approved	\N	2026-01-25 11:15:00+07	41
609	1	ШИН-063	2026-03-20	Федорова Анна Викторовна	1	\N	1	2026-05-20	2026-06-17	28	16	\N	approved	\N	2026-03-20 12:20:00+07	66
610	1	ШИН-064	2026-05-15	Федорова Анна Викторовна	1	\N	1	2026-07-15	2026-08-12	28	16	\N	approved	\N	2026-05-15 13:45:00+07	91
611	2	ВСТ-001	2025-11-15	Егоров Артём Александрович	1	\N	2	2026-01-10	2026-02-07	28	17	\N	approved	\N	2025-11-15 08:00:00+07	17
612	2	ВСТ-002	2025-12-20	Егоров Артём Александрович	1	\N	2	2026-02-20	2026-03-20	28	17	\N	approved	\N	2025-12-20 09:00:00+07	42
613	2	ВСТ-003	2026-02-01	Егоров Артём Александрович	1	\N	2	2026-04-01	2026-04-29	28	17	\N	approved	\N	2026-02-01 10:00:00+07	67
614	2	ВСТ-004	2026-03-15	Егоров Артём Александрович	1	\N	2	2026-05-15	2026-06-14	30	17	\N	approved	\N	2026-03-15 11:00:00+07	92
615	2	ВСТ-005	2025-11-18	Никитина Татьяна Станиславовна	1	\N	2	2026-01-12	2026-02-09	28	18	\N	approved	\N	2025-11-18 08:10:00+07	18
616	2	ВСТ-006	2025-12-22	Никитина Татьяна Станиславовна	1	\N	2	2026-02-22	2026-03-22	28	18	\N	approved	\N	2025-12-22 09:10:00+07	43
617	2	ВСТ-007	2026-02-05	Никитина Татьяна Станиславовна	1	\N	2	2026-04-05	2026-05-03	28	18	\N	approved	\N	2026-02-05 10:10:00+07	68
618	2	ВСТ-008	2026-03-20	Никитина Татьяна Станиславовна	1	\N	2	2026-05-20	2026-06-19	30	18	\N	approved	\N	2026-03-20 11:10:00+07	93
619	2	ВСТ-009	2025-11-20	Григорьев Павел Николаевич	1	\N	2	2026-01-15	2026-02-12	28	19	\N	approved	\N	2025-11-20 08:20:00+07	19
620	2	ВСТ-010	2025-12-25	Григорьев Павел Николаевич	1	\N	2	2026-02-25	2026-03-25	28	19	\N	approved	\N	2025-12-25 09:20:00+07	44
621	2	ВСТ-011	2026-02-08	Григорьев Павел Николаевич	1	\N	2	2026-04-08	2026-05-06	28	19	\N	approved	\N	2026-02-08 10:20:00+07	69
623	2	ВСТ-013	2025-11-22	Семенова Виктория Валерьевна	1	\N	2	2026-01-18	2026-02-15	28	20	\N	approved	\N	2025-11-22 08:30:00+07	20
624	2	ВСТ-014	2025-12-28	Семенова Виктория Валерьевна	1	\N	2	2026-02-28	2026-03-28	28	20	\N	approved	\N	2025-12-28 09:30:00+07	45
625	2	ВСТ-015	2026-02-12	Семенова Виктория Валерьевна	1	\N	2	2026-04-12	2026-05-10	28	20	\N	approved	\N	2026-02-12 10:30:00+07	70
626	2	ВСТ-016	2026-04-01	Семенова Виктория Валерьевна	1	\N	2	2026-06-01	2026-07-01	30	20	\N	approved	\N	2026-04-01 11:30:00+07	95
627	2	ВСТ-017	2025-11-24	Кузнецов Андрей Владимирович	1	\N	2	2026-01-20	2026-02-17	28	21	\N	approved	\N	2025-11-24 08:40:00+07	21
628	2	ВСТ-018	2026-01-02	Кузнецов Андрей Владимирович	1	\N	2	2026-03-02	2026-03-30	28	21	\N	approved	\N	2026-01-02 09:40:00+07	46
629	2	ВСТ-019	2026-02-15	Кузнецов Андрей Владимирович	1	\N	2	2026-04-15	2026-05-13	28	21	\N	approved	\N	2026-02-15 10:40:00+07	71
630	2	ВСТ-020	2026-04-05	Кузнецов Андрей Владимирович	1	\N	2	2026-06-05	2026-07-05	30	21	\N	approved	\N	2026-04-05 11:40:00+07	96
631	2	ВСТ-021	2025-11-26	Петрова Ольга Сергеевна	1	\N	2	2026-01-22	2026-02-19	28	22	\N	approved	\N	2025-11-26 08:50:00+07	22
632	2	ВСТ-022	2026-01-05	Петрова Ольга Сергеевна	1	\N	2	2026-03-05	2026-04-02	28	22	\N	approved	\N	2026-01-05 09:50:00+07	47
633	2	ВСТ-023	2026-02-18	Петрова Ольга Сергеевна	1	\N	2	2026-04-18	2026-05-16	28	22	\N	approved	\N	2026-02-18 10:50:00+07	72
634	2	ВСТ-024	2026-04-10	Петрова Ольга Сергеевна	1	\N	2	2026-06-10	2026-07-10	30	22	Отказ заказчика	rejected	Недостаточный стаж	2026-04-10 11:50:00+07	97
635	2	ВСТ-025	2025-11-28	Михайлов Дмитрий Алексеевич	1	\N	2	2026-01-25	2026-02-22	28	23	\N	approved	\N	2025-11-28 09:00:00+07	23
636	2	ВСТ-026	2026-01-08	Михайлов Дмитрий Алексеевич	1	\N	2	2026-03-08	2026-04-05	28	23	\N	approved	\N	2026-01-08 10:00:00+07	48
637	2	ВСТ-027	2026-02-22	Михайлов Дмитрий Алексеевич	1	\N	2	2026-04-22	2026-05-20	28	23	\N	approved	\N	2026-02-22 11:00:00+07	73
638	2	ВСТ-028	2026-04-15	Михайлов Дмитрий Алексеевич	1	\N	2	2026-06-15	2026-07-15	30	23	\N	approved	\N	2026-04-15 12:00:00+07	98
639	2	ВСТ-029	2025-12-01	Васильева Елена Игоревна	1	\N	2	2026-01-28	2026-02-25	28	24	\N	approved	\N	2025-12-01 09:10:00+07	24
640	2	ВСТ-030	2026-01-12	Васильева Елена Игоревна	1	\N	2	2026-03-12	2026-04-09	28	24	\N	approved	\N	2026-01-12 10:10:00+07	49
641	2	ВСТ-031	2026-02-26	Васильева Елена Игоревна	1	\N	2	2026-04-26	2026-05-24	28	24	\N	approved	\N	2026-02-26 11:10:00+07	74
643	2	ВСТ-033	2025-12-03	Соколов Максим Петрович	1	\N	2	2026-02-01	2026-03-01	28	25	\N	approved	\N	2025-12-03 09:20:00+07	25
644	2	ВСТ-034	2026-01-15	Соколов Максим Петрович	1	\N	2	2026-03-15	2026-04-12	28	25	\N	approved	\N	2026-01-15 10:20:00+07	50
645	2	ВСТ-035	2026-03-01	Соколов Максим Петрович	1	\N	2	2026-05-01	2026-05-29	28	25	\N	approved	\N	2026-03-01 11:20:00+07	75
646	2	ВСТ-036	2026-04-25	Соколов Максим Петрович	1	\N	2	2026-06-25	2026-07-25	30	25	\N	approved	\N	2026-04-25 12:20:00+07	100
647	3	ИГЛ-001	2025-11-10	Федорова Анна Викторовна	1	\N	3	2026-01-05	2026-02-02	28	29	\N	approved	\N	2025-11-10 08:00:00+07	101
648	3	ИГЛ-002	2025-12-15	Федорова Анна Викторовна	1	\N	3	2026-02-10	2026-03-10	28	29	\N	approved	\N	2025-12-15 09:00:00+07	126
649	3	ИГЛ-003	2026-01-20	Федорова Анна Викторовна	1	\N	3	2026-03-20	2026-04-17	28	29	\N	approved	\N	2026-01-20 10:00:00+07	151
650	3	ИГЛ-004	2025-11-12	Егоров Артём Александрович	1	\N	3	2026-01-07	2026-02-04	28	30	\N	approved	\N	2025-11-12 08:10:00+07	102
651	3	ИГЛ-005	2025-12-20	Егоров Артём Александрович	1	\N	3	2026-02-15	2026-03-15	28	30	\N	approved	\N	2025-12-20 09:10:00+07	127
652	3	ИГЛ-006	2026-01-25	Егоров Артём Александрович	1	\N	3	2026-03-25	2026-04-22	28	30	\N	approved	\N	2026-01-25 10:10:00+07	152
653	3	ИГЛ-007	2025-11-15	Никитина Татьяна Станиславовна	1	\N	3	2026-01-10	2026-02-07	28	31	\N	approved	\N	2025-11-15 08:20:00+07	103
654	3	ИГЛ-008	2025-12-22	Никитина Татьяна Станиславовна	1	\N	3	2026-02-18	2026-03-18	28	31	\N	approved	\N	2025-12-22 09:20:00+07	128
655	3	ИГЛ-009	2026-02-01	Никитина Татьяна Станиславовна	1	\N	3	2026-04-01	2026-04-29	28	31	\N	approved	\N	2026-02-01 10:20:00+07	153
656	3	ИГЛ-010	2025-11-18	Григорьев Павел Николаевич	1	\N	3	2026-01-12	2026-02-09	28	32	\N	approved	\N	2025-11-18 08:30:00+07	104
657	3	ИГЛ-011	2025-12-25	Григорьев Павел Николаевич	1	\N	3	2026-02-22	2026-03-22	28	32	\N	approved	\N	2025-12-25 09:30:00+07	129
658	3	ИГЛ-012	2026-02-05	Григорьев Павел Николаевич	1	\N	3	2026-04-05	2026-05-03	28	32	\N	approved	\N	2026-02-05 10:30:00+07	154
659	3	ИГЛ-013	2025-11-20	Семенова Виктория Валерьевна	1	\N	3	2026-01-15	2026-02-12	28	33	\N	approved	\N	2025-11-20 08:40:00+07	105
660	3	ИГЛ-014	2025-12-28	Семенова Виктория Валерьевна	1	\N	3	2026-02-25	2026-03-25	28	33	\N	approved	\N	2025-12-28 09:40:00+07	130
661	3	ИГЛ-015	2026-02-10	Семенова Виктория Валерьевна	1	\N	3	2026-04-10	2026-05-08	28	33	\N	approved	\N	2026-02-10 10:40:00+07	155
662	3	ИГЛ-016	2025-11-22	Кузнецов Андрей Владимирович	1	\N	3	2026-01-18	2026-02-15	28	34	\N	approved	\N	2025-11-22 08:50:00+07	106
663	3	ИГЛ-017	2026-01-01	Кузнецов Андрей Владимирович	1	\N	3	2026-03-01	2026-03-29	28	34	\N	approved	\N	2026-01-01 09:50:00+07	131
664	3	ИГЛ-018	2026-02-15	Кузнецов Андрей Владимирович	1	\N	3	2026-04-15	2026-05-13	28	34	\N	approved	\N	2026-02-15 10:50:00+07	156
665	3	ИГЛ-019	2025-11-24	Петрова Ольга Сергеевна	1	\N	3	2026-01-20	2026-02-17	28	35	\N	approved	\N	2025-11-24 09:00:00+07	107
666	3	ИГЛ-020	2026-01-05	Петрова Ольга Сергеевна	1	\N	3	2026-03-05	2026-04-02	28	35	\N	approved	\N	2026-01-05 10:00:00+07	132
667	3	ИГЛ-021	2026-02-20	Петрова Ольга Сергеевна	1	\N	3	2026-04-20	2026-05-18	28	35	\N	approved	\N	2026-02-20 11:00:00+07	157
668	3	ИГЛ-022	2025-11-26	Михайлов Дмитрий Алексеевич	1	\N	3	2026-01-22	2026-02-19	28	36	\N	approved	\N	2025-11-26 09:10:00+07	108
669	3	ИГЛ-023	2026-01-08	Михайлов Дмитрий Алексеевич	1	\N	3	2026-03-08	2026-04-05	28	36	\N	approved	\N	2026-01-08 10:10:00+07	133
671	3	ИГЛ-025	2025-11-28	Васильева Елена Игоревна	1	\N	3	2026-01-25	2026-02-22	28	37	\N	approved	\N	2025-11-28 09:20:00+07	109
672	3	ИГЛ-026	2026-01-12	Васильева Елена Игоревна	1	\N	3	2026-03-12	2026-04-09	28	37	\N	approved	\N	2026-01-12 10:20:00+07	134
673	3	ИГЛ-027	2026-03-01	Васильева Елена Игоревна	1	\N	3	2026-05-01	2026-05-29	28	37	\N	approved	\N	2026-03-01 11:20:00+07	159
674	3	ИГЛ-028	2025-12-01	Соколов Максим Петрович	1	\N	3	2026-01-28	2026-02-25	28	38	\N	approved	\N	2025-12-01 09:30:00+07	110
675	3	ИГЛ-029	2026-01-15	Соколов Максим Петрович	1	\N	3	2026-03-15	2026-04-12	28	38	\N	approved	\N	2026-01-15 10:30:00+07	135
676	3	ИГЛ-030	2026-03-05	Соколов Максим Петрович	1	\N	3	2026-05-05	2026-06-02	28	38	\N	rejected	Не соответствие квалификационным требованиям	2026-03-05 11:30:00+07	160
677	3	ИГЛ-031	2026-04-01	Федорова Анна Викторовна	1	\N	3	2026-06-01	2026-07-01	30	29	\N	approved	\N	2026-04-01 12:00:00+07	136
678	3	ИГЛ-032	2026-05-01	Егоров Артём Александрович	1	\N	3	2026-07-01	2026-08-30	60	30	Длительная вахта	approved	\N	2026-05-01 12:30:00+07	161
681	1	ШИН-066	2026-07-01	Никитина Татьяна Станиславовна	1	\N	1	2026-09-01	2026-10-01	30	15	Не пройден инструктаж	rejected	Отказ в размещении	2026-07-01 14:20:00+07	113
683	574	ШИН-21	2024-12-28	Шмагаренко АН	1	Инженер	1	2026-02-28	2026-03-28	29	70	Договор по заявке: ВСТ-24/09000/00289/Р от 28.12.2024	approved	\N	2026-06-19 00:00:00+07	577
684	574	ШИН-22	2024-12-28	Шмагаренко АН	1	Техник	1	2026-02-28	2026-03-28	29	70	Договор по заявке: ВСТ-24/09000/00289/Р от 28.12.2024	approved	\N	2026-06-19 00:00:00+07	578
685	574	ШИН-23	2024-12-28	Шмагаренко АН	1	Техник	1	2026-02-28	2026-03-28	29	71	Договор по заявке: ВСТ-24/09000/00289/Р от 28.12.2024	approved	\N	2026-06-19 00:00:00+07	579
779	577	ШИН-100	\N	Петров	1	Геолог	1	2026-07-01	2026-07-31	30	83	\N	approved	\N	2026-06-19 00:00:00+07	610
686	574	ЗАП-1	2024-12-28	Шмагаренко АН	1	Инженер	2	2026-04-28	2026-05-28	29	58	Договор по заявке: ВСТ-24/09000/00289/Р от 28.12.2024	approved	\N	2026-06-19 00:00:00+07	577
687	574	ЗАП-2	2024-12-28	Шмагаренко АН	1	Техник	2	2026-04-28	2026-05-29	29	58	Договор по заявке: ВСТ-24/09000/00289/Р от 28.12.2024	approved	\N	2026-06-19 00:00:00+07	578
688	574	ЗАП-3	2024-12-28	Шмагаренко АН	1	Техник	2	2026-04-28	2026-05-30	29	8	Договор по заявке: ВСТ-24/09000/00289/Р от 28.12.2024	approved	\N	2026-06-19 00:00:00+07	579
689	1	ШИН-101-доп	2025-12-01	Денисов Артур Мухаметович	1	\N	1	2026-01-10	2026-02-07	28	2	Занимаем второй блок	approved	\N	2025-12-01 10:00:00+07	161
690	1	ШИН-101-отказ	2025-12-02	Митрофанов Эмиль Харисович	1	\N	1	2026-01-12	2026-02-09	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2025-12-02 10:30:00+07	162
691	1	ШИН-103-один	2026-06-15	Мамонова Елена Александровна	1	\N	1	2026-08-01	2026-08-29	28	5	Только один блок из двух	approved	\N	2026-06-15 11:00:00+07	163
692	1	ШИН-103-второй	2026-06-20	Вишняков Валентин Игоревич	1	\N	1	2026-08-05	2026-09-02	28	6	Второй блок – номер заполнен	approved	\N	2026-06-20 11:30:00+07	164
693	1	ШИН-103-отказ	2026-06-25	Галкин Олег Николаевич	1	\N	1	2026-08-10	2026-09-07	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-06-25 12:00:00+07	165
694	1	ШИН-105-блок1	2026-09-01	Назаров Денис Петрович	1	\N	1	2026-11-01	2026-11-29	28	9	\N	approved	\N	2026-09-01 10:00:00+07	166
695	1	ШИН-105-блок2	2026-09-10	Аксёнов Максим Дмитриевич	1	\N	1	2026-11-10	2026-12-08	28	10	Второй блок	approved	\N	2026-09-10 10:30:00+07	167
696	1	ШИН-106-доп	2025-12-10	Лаптев Владимир Сергеевич	1	\N	1	2026-01-30	2026-02-26	27	12	Пересечение с блоками 11,12 частично	approved	\N	2025-12-10 12:00:00+07	168
697	1	ШИН-106-отказ	2025-12-15	Зотов Андрей Александрович	1	\N	1	2026-02-01	2026-02-28	27	\N	\N	rejected	Нет свободных мест на запрошенный период	2025-12-15 12:30:00+07	169
698	2	ВСТ-102-один	2026-10-01	Кудряшов Павел Владимирович	1	\N	2	2026-12-01	2026-12-29	28	19	Один блок из двух	approved	\N	2026-10-01 09:00:00+07	170
699	2	ВСТ-102-второй	2026-10-05	Горбачёв Сергей Викторович	1	\N	2	2026-12-05	2027-01-02	28	20	Второй блок	approved	\N	2026-10-05 09:30:00+07	171
700	2	ВСТ-102-отказ	2026-10-10	Тихонов Роман Андреевич	1	\N	2	2026-12-10	2027-01-07	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-10-10 10:00:00+07	172
701	3	ИГЛ-102-один	2026-08-01	Агапова Ольга Викторовна	1	\N	3	2026-10-01	2026-10-29	28	31	Один блок	approved	\N	2026-08-01 10:00:00+07	173
702	3	ИГЛ-102-второй	2026-08-05	Федотова Татьяна Сергеевна	1	\N	3	2026-10-05	2026-11-02	28	32	Второй блок	approved	\N	2026-08-05 10:30:00+07	174
703	1	ШИН-101-лето	2026-05-15	Климова Наталья Игоревна	1	\N	1	2026-07-01	2026-07-29	28	2	Летний период, свободно	approved	\N	2026-05-15 12:00:00+07	175
704	2	ВСТ-101-сент	2026-07-01	Никифорова Светлана Александровна	1	\N	2	2026-09-01	2026-09-29	28	17	Осенний заезд	approved	\N	2026-07-01 09:00:00+07	176
705	2	ВСТ-101-сент2	2026-07-05	Беляева Юлия Владимировна	1	\N	2	2026-09-05	2026-10-03	28	18	Заполняем номер	approved	\N	2026-07-05 09:30:00+07	177
706	2	ВСТ-101-отказ	2026-07-10	Сорокина Марина Дмитриевна	1	\N	2	2026-09-10	2026-10-08	28	\N	\N	rejected	Нет свободных мест на запрошенный период	2026-07-10 10:00:00+07	178
707	575	ШИН-24	\N	Кузнецов Андрей Владимирович	1	Техник	1	2026-01-10	2026-02-07	28	70	Договор по заявке: ГВ-101	approved	\N	2026-06-19 00:00:00+07	580
708	575	ШИН-25	\N	Петрова Ольга Сергеевна	1	Инженер	1	2026-01-15	2026-02-12	28	70	Договор по заявке: ГВ-102	approved	\N	2026-06-19 00:00:00+07	581
709	576	ШИН-26	\N	Соколов Максим Петрович	1	Геолог	1	2026-02-05	2026-03-05	28	72	Договор по заявке: ТН-101	approved	\N	2026-06-19 00:00:00+07	582
710	576	ШИН-27	\N	Соколов Максим Петрович	1	Механик	1	2026-02-10	2026-03-10	28	72	Договор по заявке: ТН-102	approved	\N	2026-06-19 00:00:00+07	583
711	575	ШИН-28	\N	Никитина Татьяна Станиславовна	1	Бурильщик	1	2026-11-12	2026-12-10	28	70	Договор по заявке: ГВ-103	approved	\N	2026-06-19 00:00:00+07	584
712	575	ШИН-29	\N	Федорова Анна Викторовна	1	Оператор ДНГ	1	2026-03-05	2026-04-02	28	71	Договор по заявке: ГВ-104	approved	\N	2026-06-19 00:00:00+07	585
713	575	ШИН-30	\N	Федорова Анна Викторовна	1	Электромонтер	1	2026-03-10	2026-04-07	28	72	Договор по заявке: ГВ-105	approved	\N	2026-06-19 00:00:00+07	586
714	575	ШИН-31	\N	Егоров Артём Александрович	1	Слесарь-ремонтник	1	2026-04-05	2026-05-03	28	70	Договор по заявке: ГВ-106	approved	\N	2026-06-19 00:00:00+07	587
715	575	ШИН-32	\N	Егоров Артём Александрович	1	Машинист	1	2026-04-10	2026-05-08	28	70	Договор по заявке: ГВ-107	approved	\N	2026-06-19 00:00:00+07	588
716	575	ШИН-33	\N	Григорьев Павел Николаевич	1	Водитель автомобиля	1	2026-10-10	2026-11-07	28	70	Договор по заявке: ГВ-108	approved	\N	2026-06-19 00:00:00+07	589
717	575	ШИН-34	\N	Михайлов Дмитрий Алексеевич	1	Геолог	1	2026-07-05	2026-08-02	28	70	Договор по заявке: ГВ-109	approved	\N	2026-06-19 00:00:00+07	590
718	575	ШИН-35	\N	Васильева Елена Игоревна	1	Электрогазосварщик	1	2026-11-05	2026-12-03	28	71	Договор по заявке: ГВ-110	approved	\N	2026-06-19 00:00:00+07	591
719	575	ШИН-36	\N	Кузнецов Андрей Владимирович	1	Техник	1	2026-01-10	2026-02-07	28	71	Договор по заявке: ГВ-101	approved	\N	2026-06-19 00:00:00+07	580
720	575	ШИН-37	\N	Петрова Ольга Сергеевна	1	Инженер	1	2026-01-15	2026-02-12	28	71	Договор по заявке: ГВ-102	approved	\N	2026-06-19 00:00:00+07	581
721	576	ШИН-38	\N	Соколов Максим Петрович	1	Геолог	1	2026-02-05	2026-03-05	28	73	Договор по заявке: ТН-101	approved	\N	2026-06-19 00:00:00+07	582
722	576	ШИН-39	\N	Соколов Максим Петрович	1	Механик	1	2026-02-10	2026-03-10	28	74	Договор по заявке: ТН-102	approved	\N	2026-06-19 00:00:00+07	583
723	575	ШИН-40	\N	Никитина Татьяна Станиславовна	1	Бурильщик	1	2026-11-12	2026-12-10	28	70	Договор по заявке: ГВ-103	approved	\N	2026-06-19 00:00:00+07	584
724	575	ШИН-41	\N	Федорова Анна Викторовна	1	Оператор ДНГ	1	2026-03-05	2026-04-02	28	74	Договор по заявке: ГВ-104	approved	\N	2026-06-19 00:00:00+07	585
725	575	ШИН-42	\N	Федорова Анна Викторовна	1	Электромонтер	1	2026-03-10	2026-04-07	28	73	Договор по заявке: ГВ-105	approved	\N	2026-06-19 00:00:00+07	586
726	575	ШИН-43	\N	Егоров Артём Александрович	1	Слесарь-ремонтник	1	2026-04-05	2026-05-03	28	71	Договор по заявке: ГВ-106	approved	\N	2026-06-19 00:00:00+07	587
727	575	ШИН-44	\N	Егоров Артём Александрович	1	Машинист	1	2026-04-10	2026-05-08	28	71	Договор по заявке: ГВ-107	approved	\N	2026-06-19 00:00:00+07	588
728	575	ШИН-45	\N	Григорьев Павел Николаевич	1	Водитель автомобиля	1	2026-10-10	2026-11-07	28	70	Договор по заявке: ГВ-108	approved	\N	2026-06-19 00:00:00+07	589
729	575	ШИН-46	\N	Михайлов Дмитрий Алексеевич	1	Геолог	1	2026-07-05	2026-08-02	28	70	Договор по заявке: ГВ-109	approved	\N	2026-06-19 00:00:00+07	590
730	575	ШИН-47	\N	Васильева Елена Игоревна	1	Электрогазосварщик	1	2026-11-05	2026-12-03	28	72	Договор по заявке: ГВ-110	approved	\N	2026-06-19 00:00:00+07	591
731	575	ШИН-48	\N	Кузнецов Андрей Владимирович	1	Техник	1	2026-01-10	2026-02-07	28	83	Договор по заявке: ГВ-101	approved	\N	2026-06-19 00:00:00+07	580
732	575	ШИН-49	\N	Петрова Ольга Сергеевна	1	Инженер	1	2026-01-15	2026-02-12	28	86	Договор по заявке: ГВ-102	approved	\N	2026-06-19 00:00:00+07	581
733	576	ШИН-50	\N	Соколов Максим Петрович	1	Геолог	1	2026-02-05	2026-03-05	28	88	Договор по заявке: ТН-101	approved	\N	2026-06-19 00:00:00+07	582
734	576	ШИН-51	\N	Соколов Максим Петрович	1	Механик	1	2026-02-10	2026-03-10	28	83	Договор по заявке: ТН-102	approved	\N	2026-06-19 00:00:00+07	583
735	575	ШИН-52	\N	Никитина Татьяна Станиславовна	1	Бурильщик	1	2026-11-12	2026-12-10	28	83	Договор по заявке: ГВ-103	approved	\N	2026-06-19 00:00:00+07	584
736	575	ШИН-53	\N	Федорова Анна Викторовна	1	Оператор ДНГ	1	2026-03-05	2026-04-02	28	86	Договор по заявке: ГВ-104	approved	\N	2026-06-19 00:00:00+07	585
737	575	ШИН-54	\N	Федорова Анна Викторовна	1	Электромонтер	1	2026-03-10	2026-04-07	28	88	Договор по заявке: ГВ-105	approved	\N	2026-06-19 00:00:00+07	586
738	575	ШИН-55	\N	Егоров Артём Александрович	1	Слесарь-ремонтник	1	2026-04-05	2026-05-03	28	83	Договор по заявке: ГВ-106	approved	\N	2026-06-19 00:00:00+07	587
739	575	ШИН-56	\N	Егоров Артём Александрович	1	Машинист	1	2026-04-10	2026-05-08	28	86	Договор по заявке: ГВ-107	approved	\N	2026-06-19 00:00:00+07	588
740	575	ШИН-57	\N	Григорьев Павел Николаевич	1	Водитель автомобиля	1	2026-10-10	2026-11-07	28	83	Договор по заявке: ГВ-108	approved	\N	2026-06-19 00:00:00+07	589
741	575	ШИН-58	\N	Михайлов Дмитрий Алексеевич	1	Геолог	1	2026-07-05	2026-08-02	28	83	Договор по заявке: ГВ-109	approved	\N	2026-06-19 00:00:00+07	590
742	575	ШИН-59	\N	Васильева Елена Игоревна	1	Электрогазосварщик	1	2026-11-05	2026-12-03	28	86	Договор по заявке: ГВ-110	approved	\N	2026-06-19 00:00:00+07	591
743	575	ШИН-60	\N	Кузнецов Андрей Владимирович	1	Техник	1	2026-02-10	2026-02-07	28	83	\N	approved	\N	2026-06-19 00:00:00+07	580
744	575	ШИН-61	\N	Петрова Ольга Сергеевна	1	Инженер	1	2026-02-15	2026-02-12	28	86	\N	approved	\N	2026-06-19 00:00:00+07	581
745	575	ШИН-62	\N	Егоров Артём Александрович	1	Машинист	1	2026-05-10	2026-06-08	28	83	\N	approved	\N	2026-06-19 00:00:00+07	588
748	577	ШИН-65	\N	Иванов А.А.	1	Геолог	1	2026-02-01	2026-03-01	28	88	\N	approved	\N	2026-06-19 00:00:00+07	593
749	577	ШИН-66	\N	Иванов А.А.	1	Геолог	1	2026-02-01	2026-03-01	28	100	\N	approved	\N	2026-06-19 00:00:00+07	594
750	577	ШИН-67	\N	Иванов А.А.	1	Геолог	1	2026-02-01	2026-03-01	28	77	\N	approved	\N	2026-06-19 00:00:00+07	595
751	577	ШИН-68	\N	Иванов А.А.	1	Геолог	1	2026-02-01	2026-03-01	28	86	\N	approved	\N	2026-06-19 00:00:00+07	596
752	577	ШИН-69	\N	Иванов А.А.	1	Геолог	1	2026-02-01	2026-03-01	28	88	\N	approved	\N	2026-06-19 00:00:00+07	597
753	577	ШИН-70	\N	Иванов А.А.	1	Геолог	1	2026-02-10	2026-06-08	999	100	\N	approved	\N	2026-06-19 00:00:00+07	598
754	577	ШИН-71	\N	Иванов А.А.	1	Геолог	1	2026-03-01	2026-03-31	30	83	\N	approved	\N	2026-06-19 00:00:00+07	599
755	577	ШИН-72	\N	Иванов А.А.	1	Геолог	1	2026-03-01	2026-03-31	30	83	\N	approved	\N	2026-06-19 00:00:00+07	600
756	577	ШИН-73	\N	Иванов А.А.	1	Геолог	1	2026-03-01	2026-03-31	30	86	\N	approved	\N	2026-06-19 00:00:00+07	601
757	577	ШИН-74	\N	Иванов А.А.	1	Геолог	1	2026-03-01	2026-03-31	30	101	\N	approved	\N	2026-06-19 00:00:00+07	602
758	577	ШИН-75	\N	Иванов А.А.	1	Геолог	1	2026-03-01	2026-03-31	30	77	\N	approved	\N	2026-06-19 00:00:00+07	603
765	577	ШИН-85	\N	Иванов А.А.	1	Геолог	1	2026-03-01	2026-03-31	30	78	\N	approved	\N	2026-06-19 00:00:00+07	593
766	577	ШИН-86	\N	Иванов А.А.	1	Геолог	1	2026-04-01	2026-04-30	29	88	\N	approved	\N	2026-06-19 00:00:00+07	602
772	577	ШИН-93	\N	Иванов А.А.	1	Инженер	1	2026-01-20	2026-02-20	31	101	\N	approved	\N	2026-06-19 00:00:00+07	592
773	577	ШИН-94	\N	Иванов А.А.	1	Инженер	1	2026-02-15	2026-03-15	28	80	\N	approved	\N	2026-06-19 00:00:00+07	604
774	578	ШИН-95	\N	(пусто)	1	Водитель	1	2026-05-15	2026-06-15	31	86	\N	approved	\N	2026-06-19 00:00:00+07	605
775	577	ШИН-96	\N	Иванов А.А.	1	Инженер	1	2026-06-05	2026-07-05	30	88	\N	approved	\N	2026-06-19 00:00:00+07	606
776	577	ШИН-97	\N	Иванов А.А.	1	Инженер	1	2026-07-20	2026-08-20	31	86	\N	approved	\N	2026-06-19 00:00:00+07	607
777	577	ШИН-98	\N	Иванов А.А.	1	Инженер	1	2026-08-01	2026-08-31	30	88	\N	approved	\N	2026-06-19 00:00:00+07	608
778	578	ШИН-99	\N	(пусто)	1	Инженер	1	2026-06-15	2026-07-15	30	100	\N	approved	\N	2026-06-19 00:00:00+07	609
780	578	ШИН-101	\N	(пусто)	1	Геолог	1	2026-07-10	2026-08-10	31	86	\N	approved	\N	2026-06-19 00:00:00+07	611
781	578	ШИН-102	\N	(пусто)	1	Водитель	1	2026-08-01	2026-08-31	30	100	\N	approved	\N	2026-06-19 00:00:00+07	612
782	577	ШИН-103	\N	(пусто)	1	Инженер	1	2026-08-05	2026-09-05	31	83	\N	approved	\N	2026-06-19 00:00:00+07	613
783	578	ШИН-104	\N	(пусто)	1	Инженер	1	2026-08-05	2026-09-05	31	83	\N	approved	\N	2026-06-19 00:00:00+07	614
785	577	ШИН-106	\N	Иванов	1	Инженер	1	2026-10-01	2026-10-31	30	88	\N	approved	\N	2026-06-19 00:00:00+07	616
786	578	ШИН-107	\N	(пусто)	1	Инженер	1	2026-10-01	2026-10-31	30	100	\N	approved	\N	2026-06-19 00:00:00+07	617
788	578	ШИН-109	\N	(пусто)	1	Водитель	1	2026-10-10	2026-11-10	31	88	\N	approved	\N	2026-06-19 00:00:00+07	619
789	577	ШИН-110	\N	Петров	1	Геолог	1	2026-10-15	2026-11-15	31	100	\N	approved	\N	2026-06-19 00:00:00+07	620
790	577	ШИН-111	\N	Сидоров	1	Геолог	1	2026-11-15	2026-12-15	30	88	\N	approved	\N	2026-06-19 00:00:00+07	615
791	577	ШИН-112	\N	Иванов	1	Инженер	1	2026-11-01	2026-11-30	29	86	\N	approved	\N	2026-06-19 00:00:00+07	621
792	578	ШИН-113	\N	Петров	1	Геолог	1	2026-11-05	2026-12-05	30	100	\N	approved	\N	2026-06-19 00:00:00+07	622
793	577	ШИН-114	\N	(пусто)	1	Водитель	1	2026-11-10	2026-12-10	30	83	\N	approved	\N	2026-06-19 00:00:00+07	623
794	578	ШИН-115	\N	(пусто)	1	Техник	1	2026-11-15	2026-12-15	30	88	\N	approved	\N	2026-06-19 00:00:00+07	624
795	577	ШИН-116	\N	Смирнов	1	Инженер	1	2026-11-20	2026-12-20	30	100	\N	approved	\N	2026-06-19 00:00:00+07	625
796	577	ШИН-117	\N	Иванов	1	Инженер	1	2026-12-01	2026-12-31	30	86	\N	approved	\N	2026-06-19 00:00:00+07	626
797	578	ШИН-118	\N	Петров	1	Геолог	1	2026-12-05	2027-01-05	31	86	\N	approved	\N	2026-06-19 00:00:00+07	627
798	577	ШИН-119	\N	Сидоров	1	Водитель	1	2026-12-10	2027-01-10	31	100	\N	approved	\N	2026-06-19 00:00:00+07	628
799	577	ШИН-120	\N	(пусто)	1	Техник	1	2026-12-15	2027-01-15	31	83	\N	approved	\N	2026-06-19 00:00:00+07	618
800	487	ШИН-121	2026-06-22	Фаизова Софья	1	Повар	1	2026-06-01	2026-06-30	30	112		approved	\N	2026-06-22 00:00:00+07	629
801	558	ШИН-122	2026-06-27	Андронов Артем Андреевич	1	Рабочий	1	2026-06-01	2026-06-30	30	93		approved	\N	2026-06-27 00:00:00+07	630
\.


--
-- TOC entry 5147 (class 0 OID 26039)
-- Dependencies: 240
-- Data for Name: residents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.residents (id, full_name, "position", gender, birthday, first_name, last_name, middle_name) FROM stdin;
385	Иванов Александр Сергеевич	Инженер	male	1985-04-12	Александр	Иванов	Сергеевич
386	Петров Сергей Иванович	Инженер	male	1978-11-23	Сергей	Петров	Иванович
387	Сидоров Дмитрий Алексеевич	Инженер	male	1990-07-15	Дмитрий	Сидоров	Алексеевич
388	Кузнецов Андрей Владимирович	Инженер	male	1982-02-28	Андрей	Кузнецов	Владимирович
389	Смирнов Иван Александрович	Инженер	male	1987-09-03	Иван	Смирнов	Александрович
390	Попов Алексей Дмитриевич	Инженер	male	1993-05-19	Алексей	Попов	Дмитриевич
391	Васильев Владимир Сергеевич	Инженер	male	1975-12-08	Владимир	Васильев	Сергеевич
392	Михайлов Николай Иванович	Инженер	male	1988-03-22	Николай	Михайлов	Иванович
393	Фёдоров Денис Андреевич	Инженер	male	1995-08-14	Денис	Фёдоров	Андреевич
394	Морозов Максим Викторович	Инженер	male	1980-06-30	Максим	Морозов	Викторович
395	Яковлев Роман Петрович	Инженер	male	1991-01-25	Роман	Яковлев	Петрович
396	Зайцев Артём Сергеевич	Инженер	male	1984-10-17	Артём	Зайцев	Сергеевич
397	Соловьёв Игорь Александрович	Инженер	male	1977-07-09	Игорь	Соловьёв	Александрович
398	Борисов Геннадий Валерьевич	Инженер	male	1992-12-04	Геннадий	Борисов	Валерьевич
399	Григорьев Павел Николаевич	Инженер	male	1986-04-28	Павел	Григорьев	Николаевич
400	Орлов Валерий Дмитриевич	Инженер	male	1979-09-11	Валерий	Орлов	Дмитриевич
401	Антонов Константин Сергеевич	Инженер	male	1994-02-14	Константин	Антонов	Сергеевич
402	Тимофеев Егор Владимирович	Инженер	male	1983-11-05	Егор	Тимофеев	Владимирович
403	Никитин Станислав Игоревич	Инженер	male	1996-06-21	Станислав	Никитин	Игоревич
404	Козлов Олег Андреевич	Инженер	male	1981-08-07	Олег	Козлов	Андреевич
405	Лебедев Виктор Степанович	Инженер	male	1974-01-19	Виктор	Лебедев	Степанович
406	Новиков Юрий Михайлович	Инженер	male	1989-03-31	Юрий	Новиков	Михайлович
407	Марков Антон Павлович	Инженер	male	1997-10-26	Антон	Марков	Павлович
408	Филиппов Евгений Викторович	Инженер	male	1976-12-15	Евгений	Филиппов	Викторович
409	Данилов Ренат Равильевич	Инженер	male	1988-07-02	Ренат	Данилов	Равильевич
410	Семёнов Григорий Алексеевич	Техник	male	1990-05-18	Григорий	Семёнов	Алексеевич
411	Тарасов Степан Иванович	Техник	male	1984-11-09	Степан	Тарасов	Иванович
412	Виноградов Матвей Сергеевич	Техник	male	1993-09-27	Матвей	Виноградов	Сергеевич
413	Егоров Вадим Дмитриевич	Техник	male	1980-03-14	Вадим	Егоров	Дмитриевич
414	Павлов Даниил Андреевич	Техник	male	1995-08-03	Даниил	Павлов	Андреевич
415	Комаров Илья Владимирович	Техник	male	1987-02-22	Илья	Комаров	Владимирович
416	Алексеев Тимофей Николаевич	Техник	male	1978-06-17	Тимофей	Алексеев	Николаевич
417	Калинин Фёдор Петрович	Техник	male	1991-10-12	Фёдор	Калинин	Петрович
418	Крылов Эдуард Михайлович	Техник	male	1983-12-29	Эдуард	Крылов	Михайлович
419	Медведев Аркадий Викторович	Техник	male	1997-04-08	Аркадий	Медведев	Викторович
420	Белов Станислав Олегович	Техник	male	1985-09-15	Станислав	Белов	Олегович
421	Гаврилов Анатолий Сергеевич	Техник	male	1975-01-30	Анатолий	Гаврилов	Сергеевич
422	Кириллов Вячеслав Александрович	Техник	male	1992-07-24	Вячеслав	Кириллов	Александрович
423	Богданов Руслан Игоревич	Техник	male	1986-05-07	Руслан	Богданов	Игоревич
424	Савельев Артур Валерьевич	Техник	male	1994-11-11	Артур	Савельев	Валерьевич
425	Королёв Леонид Дмитриевич	Техник	male	1981-08-19	Леонид	Королёв	Дмитриевич
426	Фомин Владислав Андреевич	Техник	male	1999-03-25	Владислав	Фомин	Андреевич
427	Игнатов Арсений Николаевич	Техник	male	1977-10-06	Арсений	Игнатов	Николаевич
428	Дмитриев Борис Владимирович	Техник	male	1989-12-15	Борис	Дмитриев	Владимирович
429	Логинов Денис Сергеевич	Техник	male	1996-02-28	Денис	Логинов	Сергеевич
430	Громов Никита Петрович	Техник	male	1982-09-04	Никита	Громов	Петрович
431	Титов Виталий Геннадьевич	Техник	male	1990-04-17	Виталий	Титов	Геннадьевич
432	Рогов Лев Александрович	Техник	male	1979-07-22	Лев	Рогов	Александрович
433	Шевченко Валерий Семёнович	Техник	male	1993-01-06	Валерий	Шевченко	Семёнович
434	Сорокин Михаил Олегович	Техник	male	1984-06-14	Михаил	Сорокин	Олегович
435	Ковалёв Пётр Игоревич	Машинист	male	1998-08-30	Пётр	Ковалёв	Игоревич
593	Петров Петр	Геолог	\N	\N	\N	\N	\N
436	Николаев Давид Романович	Машинист	male	1987-03-19	Давид	Николаев	Романович
437	Сафонов Глеб Алексеевич	Машинист	male	1995-11-28	Глеб	Сафонов	Алексеевич
438	Исаев Ярослав Викторович	Машинист	male	1980-05-03	Ярослав	Исаев	Викторович
439	Лазарев Артемий Дмитриевич	Машинист	male	1992-12-11	Артемий	Лазарев	Дмитриевич
440	Баранов Сергей Юрьевич	Машинист	male	1976-09-25	Сергей	Баранов	Юрьевич
441	Кузьмин Родион Эдуардович	Машинист	male	1988-02-07	Родион	Кузьмин	Эдуардович
442	Трофимов Тимур Станиславович	Машинист	male	1994-07-13	Тимур	Трофимов	Станиславович
443	Ефимов Филипп Аркадьевич	Машинист	male	1983-04-26	Филипп	Ефимов	Аркадьевич
444	Дементьев Богдан Ильич	Машинист	male	1999-10-08	Богдан	Дементьев	Ильич
445	Максимов Святослав Егорович	Машинист	male	1977-01-15	Святослав	Максимов	Егорович
446	Ершов Прохор Вячеславович	Машинист	male	1991-06-29	Прохор	Ершов	Вячеславович
447	Афанасьев Демьян Тимофеевич	Машинист	male	1985-08-22	Демьян	Афанасьев	Тимофеевич
448	Герасимов Платон Никитич	Машинист	male	1996-03-04	Платон	Герасимов	Никитич
449	Власов Эмиль Русланович	Машинист	male	1981-12-18	Эмиль	Власов	Русланович
450	Лукин Алан Артурович	Водитель автомобиля	male	1993-09-01	Алан	Лукин	Артурович
451	Панфилов Герман Вадимович	Водитель автомобиля	male	1980-05-10	Герман	Панфилов	Вадимович
452	Субботин Марк Леонидович	Водитель автомобиля	male	1997-11-23	Марк	Субботин	Леонидович
453	Князев Клим Владиславович	Водитель автомобиля	male	1984-02-14	Клим	Князев	Владиславович
454	Белоусов Эрик Денисович	Водитель автомобиля	male	1992-07-31	Эрик	Белоусов	Денисович
455	Шаров Венедикт Арсеньевич	Водитель автомобиля	male	1978-04-27	Венедикт	Шаров	Арсеньевич
456	Маслов Мирон Борисович	Водитель автомобиля	male	1995-08-09	Мирон	Маслов	Борисович
457	Кабанов Адриан Данилович	Водитель автомобиля	male	1986-01-13	Адриан	Кабанов	Данилович
458	Коновалов Савелий Матвеевич	Водитель автомобиля	male	1990-06-05	Савелий	Коновалов	Матвеевич
459	Жуков Фаддей Тимофеевич	Водитель автомобиля	male	1982-10-19	Фаддей	Жуков	Тимофеевич
460	Овчинников Лаврентий Григорьевич	Водитель автомобиля	male	1998-12-07	Лаврентий	Овчинников	Григорьевич
461	Бирюков Игнат Степанович	Водитель автомобиля	male	1979-03-29	Игнат	Бирюков	Степанович
462	Агафонов Афанасий Олегович	Электромонтер	male	1994-09-14	Афанасий	Агафонов	Олегович
463	Рябов Вадим Петрович	Электромонтер	male	1983-05-22	Вадим	Рябов	Петрович
464	Мельников Кузьма Валерьевич	Электромонтер	male	1988-11-06	Кузьма	Мельников	Валерьевич
465	Горшков Фрол Геннадьевич	Электромонтер	male	1991-02-18	Фрол	Горшков	Геннадьевич
466	Зуев Трофим Ильич	Электромонтер	male	1980-07-05	Трофим	Зуев	Ильич
467	Харитонов Евсей Фёдорович	Электромонтер	male	1996-10-30	Евсей	Харитонов	Фёдорович
468	Гусев Анисим Александрович	Электромонтер	male	1977-12-15	Анисим	Гусев	Александрович
469	Ларионов Захар Дмитриевич	Электромонтер	male	1989-04-09	Захар	Ларионов	Дмитриевич
470	Филимонов Влас Николаевич	Электромонтер	male	1992-08-24	Влас	Филимонов	Николаевич
471	Бобров Дорофей Викторович	Электромонтер	male	1985-01-31	Дорофей	Бобров	Викторович
472	Самойлов Кондрат Сергеевич	Электромонтер	male	1993-06-16	Кондрат	Самойлов	Сергеевич
473	Воробьёв Арслан Андреевич	Электромонтер	male	1981-09-07	Арслан	Воробьёв	Андреевич
474	Сергеев Аким Романович	Слесарь-ремонтник	male	1997-03-13	Аким	Сергеев	Романович
475	Андреев Никанор Игоревич	Слесарь-ремонтник	male	1984-07-28	Никанор	Андреев	Игоревич
476	Волков Тихон Эдуардович	Слесарь-ремонтник	male	1990-12-02	Тихон	Волков	Эдуардович
477	Глухов Макар Станиславович	Слесарь-ремонтник	male	1978-05-19	Макар	Глухов	Станиславович
478	Абрамов Ратмир Вячеславович	Слесарь-ремонтник	male	1995-10-11	Ратмир	Абрамов	Вячеславович
479	Щербаков Любомир Аркадьевич	Слесарь-ремонтник	male	1982-02-27	Любомир	Щербаков	Аркадьевич
480	Мартынов Назар Тимурович	Слесарь-ремонтник	male	1998-06-14	Назар	Мартынов	Тимурович
481	Емельянов Яромир Денисович	Слесарь-ремонтник	male	1986-09-23	Яромир	Емельянов	Денисович
482	Колесников Камиль Русланович	Слесарь-ремонтник	male	1991-04-08	Камиль	Колесников	Русланович
590	Гость Нигматуллин Булат	Геолог	\N	\N	\N	\N	\N
483	Фролов Дамир Артурович	Слесарь-ремонтник	male	1980-01-14	Дамир	Фролов	Артурович
484	Куликов Искандер Эмилевич	Слесарь-ремонтник	male	1994-08-29	Искандер	Куликов	Эмилевич
485	Зимин Тимур Маратович	Слесарь-ремонтник	male	1987-11-16	Тимур	Зимин	Маратович
486	Ильин Сабир Равилевич	Бурильщик	male	1999-05-04	Сабир	Ильин	Равилевич
487	Соболев Булат Альбертович	Бурильщик	male	1983-03-21	Булат	Соболев	Альбертович
488	Мясников Айдар Мансурович	Бурильщик	male	1977-10-07	Айдар	Мясников	Мансурович
489	Цветков Ильдар Рашидович	Бурильщик	male	1992-01-26	Ильдар	Цветков	Рашидович
490	Нестеров Марат Ирекович	Бурильщик	male	1985-07-12	Марат	Нестеров	Ирекович
491	Лапин Рушан Фаритович	Бурильщик	male	1996-12-03	Рушан	Лапин	Фаритович
492	Дроздов Асланбек Салманович	Бурильщик	male	1981-06-18	Асланбек	Дроздов	Салманович
493	Архипов Русланбек Хасанович	Бурильщик	male	1990-09-09	Русланбек	Архипов	Хасанович
494	Шестаков Мурат Заурович	Бурильщик	male	1979-04-25	Мурат	Шестаков	Заурович
495	Беляев Арсен Борисович	Бурильщик	male	1988-02-13	Арсен	Беляев	Борисович
496	Воронов Салават Наилевич	Бурильщик	male	1994-11-30	Салават	Воронов	Наилевич
497	Лобанов Айрат Рафикович	Бурильщик	male	1982-08-05	Айрат	Лобанов	Рафикович
498	Голубев Замир Ахметович	Бурильщик	male	1998-05-17	Замир	Голубев	Ахметович
499	Исаков Газинур Габдуллович	Бурильщик	male	1976-03-11	Газинур	Исаков	Габдуллович
500	Осипов Рафаэль Ринатович	Бурильщик	male	1993-10-22	Рафаэль	Осипов	Ринатович
501	Третьяков Ильгиз Асхатович	Оператор ДНГ	male	1986-01-09	Ильгиз	Третьяков	Асхатович
502	Мамонтов Данис Фаридович	Оператор ДНГ	male	1991-07-30	Данис	Мамонтов	Фаридович
503	Гордеев Айнур Дамирович	Оператор ДНГ	male	1980-04-16	Айнур	Гордеев	Дамирович
504	Дьячков Ленар Ильдусович	Оператор ДНГ	male	1997-09-02	Ленар	Дьячков	Ильдусович
505	Русаков Азат Рамилевич	Оператор ДНГ	male	1984-12-27	Азат	Русаков	Рамилевич
506	Лыткин Роберт Альфритович	Оператор ДНГ	male	1995-06-10	Роберт	Лыткин	Альфритович
507	Жданов Инсаф Шамилевич	Оператор ДНГ	male	1978-02-22	Инсаф	Жданов	Шамилевич
508	Котов Альберт Газинурович	Оператор ДНГ	male	1989-11-14	Альберт	Котов	Газинурович
509	Сазонов Рашид Мунирович	Оператор ДНГ	male	1996-08-06	Рашид	Сазонов	Мунирович
510	Поляков Карим Зуфарович	Оператор ДНГ	male	1983-05-29	Карим	Поляков	Зуфарович
511	Меркулов Ирек Асгатович	Оператор ДНГ	male	1990-01-15	Ирек	Меркулов	Асгатович
512	Быков Фанис Аглямович	Оператор ДНГ	male	1987-07-03	Фанис	Быков	Аглямович
513	Кондратьев Ильшат Рафаилович	Оператор ДНГ	male	1992-04-19	Ильшат	Кондратьев	Рафаилович
514	Копылов Радик Ахнафович	Оператор ДНГ	male	1981-10-31	Радик	Копылов	Ахнафович
515	Чернов Гаяз Габдрахманович	Оператор ДНГ	male	1994-03-25	Гаяз	Чернов	Габдрахманович
516	Ширяев Нафис Мисбахович	Мастер участка	male	1985-08-12	Нафис	Ширяев	Мисбахович
517	Молчанов Мансур Фаязович	Мастер участка	male	1979-12-01	Мансур	Молчанов	Фаязович
518	Агапов Халил Галимзянович	Мастер участка	male	1993-06-27	Халил	Агапов	Галимзянович
519	Левин Ришат Нуриевич	Мастер участка	male	1986-02-11	Ришат	Левин	Нуриевич
520	Терехов Ильнур Фанилевич	Мастер участка	male	1997-10-05	Ильнур	Терехов	Фанилевич
521	Карпов Динар Азатович	Мастер участка	male	1982-07-20	Динар	Карпов	Азатович
522	Гуляев Альфред Рауфович	Мастер участка	male	1991-04-09	Альфред	Гуляев	Рауфович
523	Мишин Энгель Нагимович	Мастер участка	male	1980-09-23	Энгель	Мишин	Нагимович
524	Панов Вильдан Ильгизович	Мастер участка	male	1995-01-18	Вильдан	Панов	Ильгизович
525	Рожков Асхат Сагитович	Начальник смены	male	1984-06-06	Асхат	Рожков	Сагитович
526	Зверев Раиль Маннапович	Начальник смены	male	1978-11-03	Раиль	Зверев	Маннапович
527	Потапов Ильмир Бариевич	Начальник смены	male	1992-03-27	Ильмир	Потапов	Бариевич
528	Кудрявцев Мунир Закиевич	Начальник смены	male	1988-08-14	Мунир	Кудрявцев	Закиевич
529	Родионов Габдулла Сабирович	Начальник смены	male	1996-12-08	Габдулла	Родионов	Сабирович
530	Крюков Фаяз Камилевич	Начальник смены	male	1981-05-25	Фаяз	Крюков	Камилевич
531	Беляков Наиль Гараевич	Начальник смены	male	1990-10-19	Наиль	Беляков	Гараевич
532	Большаков Рамис Ильгизарович	Начальник смены	male	1987-02-07	Рамис	Большаков	Ильгизарович
533	Селезнёв Айбулат Данисович	Начальник смены	male	1994-07-15	Айбулат	Селезнёв	Данисович
534	Латышев Рамзис Салихович	Электрогазосварщик	male	1979-04-02	Рамзис	Латышев	Салихович
535	Блохин Ринат Замирович	Электрогазосварщик	male	1985-09-28	Ринат	Блохин	Замирович
536	Наумов Салим Кирамович	Электрогазосварщик	male	1993-01-11	Салим	Наумов	Кирамович
537	Зыков Аслан Гафурович	Электрогазосварщик	male	1988-06-22	Аслан	Зыков	Гафурович
538	Дорофеев Даян Альтафович	Электрогазосварщик	male	1997-03-09	Даян	Дорофеев	Альтафович
539	Токарев Загир Фаритович	Электрогазосварщик	male	1982-12-24	Загир	Токарев	Фаритович
540	Анисимов Гамиль Асхатович	Электрогазосварщик	male	1991-08-17	Гамиль	Анисимов	Асхатович
541	Ермаков Ильяс Халитович	Электрогазосварщик	male	1980-02-13	Ильяс	Ермаков	Халитович
542	Брагин Ранис Назипович	Электрогазосварщик	male	1996-10-06	Ранис	Брагин	Назипович
543	Воронцов Айназ Рафаэлевич	Геолог	male	1984-05-30	Айназ	Воронцов	Рафаэлевич
544	Шмелёв Дамир Камилевич	Геолог	male	1977-09-15	Дамир	Шмелёв	Камилевич
545	Денисов Артур Мухаметович	Геолог	male	1992-01-03	Артур	Денисов	Мухаметович
546	Митрофанов Эмиль Харисович	Геолог	male	1986-06-19	Эмиль	Митрофанов	Харисович
547	Мамонова Елена Александровна	Геолог	female	1989-08-27	Елена	Мамонова	Александровна
548	Вишняков Валентин Игоревич	Механик	male	1983-04-14	Валентин	Вишняков	Игоревич
549	Галкин Олег Николаевич	Механик	male	1990-09-07	Олег	Галкин	Николаевич
550	Назаров Денис Петрович	Механик	male	1985-01-22	Денис	Назаров	Петрович
551	Аксёнов Максим Дмитриевич	Механик	male	1994-06-15	Максим	Аксёнов	Дмитриевич
552	Лаптев Владимир Сергеевич	Механик	male	1981-12-08	Владимир	Лаптев	Сергеевич
553	Зотов Андрей Александрович	Механик	male	1978-07-31	Андрей	Зотов	Александрович
554	Кудряшов Павел Владимирович	Механик	male	1993-02-19	Павел	Кудряшов	Владимирович
555	Горбачёв Сергей Викторович	Механик	male	1988-11-04	Сергей	Горбачёв	Викторович
556	Тихонов Роман Андреевич	Механик	male	1997-05-26	Роман	Тихонов	Андреевич
557	Агапова Ольга Викторовна	Механик	female	1984-10-10	Ольга	Агапова	Викторовна
558	Федотова Татьяна Сергеевна	Лаборант	female	1990-04-02	Татьяна	Федотова	Сергеевна
559	Климова Наталья Игоревна	Лаборант	female	1982-09-18	Наталья	Климова	Игоревна
560	Никифорова Светлана Александровна	Лаборант	female	1987-12-29	Светлана	Никифорова	Александровна
561	Беляева Юлия Владимировна	Лаборант	female	1995-06-13	Юлия	Беляева	Владимировна
562	Сорокина Марина Дмитриевна	Кладовщик	female	1981-03-07	Марина	Сорокина	Дмитриевна
563	Волкова Алина Олеговна	Кладовщик	female	1992-08-23	Алина	Волкова	Олеговна
564	Киселёва Анна Романовна	Кладовщик	female	1986-11-15	Анна	Киселёва	Романовна
565	Емельянова Дарья Игоревна	Инженер	female	1998-01-09	Дарья	Емельянова	Игоревна
566	Маркова Кристина Павловна	Инженер	female	1989-07-22	Кристина	Маркова	Павловна
567	Калинина Евгения Валерьевна	Инженер	female	1994-04-05	Евгения	Калинина	Валерьевна
568	Медведева Вероника Станиславовна	Техник	female	1985-09-30	Вероника	Медведева	Станиславовна
569	Игнатова Полина Денисовна	Техник	female	1991-02-14	Полина	Игнатова	Денисовна
570	Фомина Валерия Артёмовна	Техник	female	1983-06-28	Валерия	Фомина	Артёмовна
571	Борисова Анастасия Егоровна	Электромонтер	female	1996-11-11	Анастасия	Борисова	Егоровна
572	Логинова Екатерина Тимуровна	Слесарь-ремонтник	female	1988-05-19	Екатерина	Логинова	Тимуровна
573	Данилова Алиса Эдуардовна	Оператор ДНГ	female	1999-08-03	Алиса	Данилова	Эдуардовна
574	Семёнова Василиса Руслановна	Мастер участка	female	1980-12-17	Василиса	Семёнова	Руслановна
575	Титова Злата Арсеньевна	Водитель автомобиля	female	1993-03-26	Злата	Титова	Арсеньевна
576	Ковалёва Ярослава Даниловна	Бурильщик	female	1986-10-01	Ярослава	Ковалёва	Даниловна
1	Иванов Александр Сергеевич	Инженер	male	1985-04-12	Александр	Иванов	Сергеевич
2	Петров Сергей Иванович	Инженер	male	1978-11-23	Сергей	Петров	Иванович
3	Сидоров Дмитрий Алексеевич	Инженер	male	1990-07-15	Дмитрий	Сидоров	Алексеевич
4	Кузнецов Андрей Владимирович	Инженер	male	1982-02-28	Андрей	Кузнецов	Владимирович
594	Захаров Илья	Геолог	\N	\N	\N	\N	\N
5	Смирнов Иван Александрович	Инженер	male	1987-09-03	Иван	Смирнов	Александрович
6	Попов Алексей Дмитриевич	Инженер	male	1993-05-19	Алексей	Попов	Дмитриевич
7	Васильев Владимир Сергеевич	Инженер	male	1975-12-08	Владимир	Васильев	Сергеевич
8	Михайлов Николай Иванович	Инженер	male	1988-03-22	Николай	Михайлов	Иванович
9	Фёдоров Денис Андреевич	Инженер	male	1995-08-14	Денис	Фёдоров	Андреевич
10	Морозов Максим Викторович	Инженер	male	1980-06-30	Максим	Морозов	Викторович
11	Яковлев Роман Петрович	Инженер	male	1991-01-25	Роман	Яковлев	Петрович
12	Зайцев Артём Сергеевич	Инженер	male	1984-10-17	Артём	Зайцев	Сергеевич
13	Соловьёв Игорь Александрович	Инженер	male	1977-07-09	Игорь	Соловьёв	Александрович
14	Борисов Геннадий Валерьевич	Инженер	male	1992-12-04	Геннадий	Борисов	Валерьевич
15	Григорьев Павел Николаевич	Инженер	male	1986-04-28	Павел	Григорьев	Николаевич
16	Орлов Валерий Дмитриевич	Инженер	male	1979-09-11	Валерий	Орлов	Дмитриевич
17	Антонов Константин Сергеевич	Инженер	male	1994-02-14	Константин	Антонов	Сергеевич
18	Тимофеев Егор Владимирович	Инженер	male	1983-11-05	Егор	Тимофеев	Владимирович
19	Никитин Станислав Игоревич	Инженер	male	1996-06-21	Станислав	Никитин	Игоревич
20	Козлов Олег Андреевич	Инженер	male	1981-08-07	Олег	Козлов	Андреевич
21	Лебедев Виктор Степанович	Инженер	male	1974-01-19	Виктор	Лебедев	Степанович
22	Новиков Юрий Михайлович	Инженер	male	1989-03-31	Юрий	Новиков	Михайлович
23	Марков Антон Павлович	Инженер	male	1997-10-26	Антон	Марков	Павлович
24	Филиппов Евгений Викторович	Инженер	male	1976-12-15	Евгений	Филиппов	Викторович
25	Данилов Ренат Равильевич	Инженер	male	1988-07-02	Ренат	Данилов	Равильевич
26	Семёнов Григорий Алексеевич	Техник	male	1990-05-18	Григорий	Семёнов	Алексеевич
27	Тарасов Степан Иванович	Техник	male	1984-11-09	Степан	Тарасов	Иванович
28	Виноградов Матвей Сергеевич	Техник	male	1993-09-27	Матвей	Виноградов	Сергеевич
29	Егоров Вадим Дмитриевич	Техник	male	1980-03-14	Вадим	Егоров	Дмитриевич
30	Павлов Даниил Андреевич	Техник	male	1995-08-03	Даниил	Павлов	Андреевич
31	Комаров Илья Владимирович	Техник	male	1987-02-22	Илья	Комаров	Владимирович
32	Алексеев Тимофей Николаевич	Техник	male	1978-06-17	Тимофей	Алексеев	Николаевич
33	Калинин Фёдор Петрович	Техник	male	1991-10-12	Фёдор	Калинин	Петрович
34	Крылов Эдуард Михайлович	Техник	male	1983-12-29	Эдуард	Крылов	Михайлович
35	Медведев Аркадий Викторович	Техник	male	1997-04-08	Аркадий	Медведев	Викторович
36	Белов Станислав Олегович	Техник	male	1985-09-15	Станислав	Белов	Олегович
37	Гаврилов Анатолий Сергеевич	Техник	male	1975-01-30	Анатолий	Гаврилов	Сергеевич
38	Кириллов Вячеслав Александрович	Техник	male	1992-07-24	Вячеслав	Кириллов	Александрович
39	Богданов Руслан Игоревич	Техник	male	1986-05-07	Руслан	Богданов	Игоревич
40	Савельев Артур Валерьевич	Техник	male	1994-11-11	Артур	Савельев	Валерьевич
41	Королёв Леонид Дмитриевич	Техник	male	1981-08-19	Леонид	Королёв	Дмитриевич
42	Фомин Владислав Андреевич	Техник	male	1999-03-25	Владислав	Фомин	Андреевич
43	Игнатов Арсений Николаевич	Техник	male	1977-10-06	Арсений	Игнатов	Николаевич
44	Дмитриев Борис Владимирович	Техник	male	1989-12-15	Борис	Дмитриев	Владимирович
45	Логинов Денис Сергеевич	Техник	male	1996-02-28	Денис	Логинов	Сергеевич
46	Громов Никита Петрович	Техник	male	1982-09-04	Никита	Громов	Петрович
47	Титов Виталий Геннадьевич	Техник	male	1990-04-17	Виталий	Титов	Геннадьевич
48	Рогов Лев Александрович	Техник	male	1979-07-22	Лев	Рогов	Александрович
49	Шевченко Валерий Семёнович	Техник	male	1993-01-06	Валерий	Шевченко	Семёнович
50	Сорокин Михаил Олегович	Техник	male	1984-06-14	Михаил	Сорокин	Олегович
51	Ковалёв Пётр Игоревич	Машинист	male	1998-08-30	Пётр	Ковалёв	Игоревич
52	Николаев Давид Романович	Машинист	male	1987-03-19	Давид	Николаев	Романович
53	Сафонов Глеб Алексеевич	Машинист	male	1995-11-28	Глеб	Сафонов	Алексеевич
54	Исаев Ярослав Викторович	Машинист	male	1980-05-03	Ярослав	Исаев	Викторович
55	Лазарев Артемий Дмитриевич	Машинист	male	1992-12-11	Артемий	Лазарев	Дмитриевич
56	Баранов Сергей Юрьевич	Машинист	male	1976-09-25	Сергей	Баранов	Юрьевич
57	Кузьмин Родион Эдуардович	Машинист	male	1988-02-07	Родион	Кузьмин	Эдуардович
58	Трофимов Тимур Станиславович	Машинист	male	1994-07-13	Тимур	Трофимов	Станиславович
59	Ефимов Филипп Аркадьевич	Машинист	male	1983-04-26	Филипп	Ефимов	Аркадьевич
60	Дементьев Богдан Ильич	Машинист	male	1999-10-08	Богдан	Дементьев	Ильич
61	Максимов Святослав Егорович	Машинист	male	1977-01-15	Святослав	Максимов	Егорович
62	Ершов Прохор Вячеславович	Машинист	male	1991-06-29	Прохор	Ершов	Вячеславович
63	Афанасьев Демьян Тимофеевич	Машинист	male	1985-08-22	Демьян	Афанасьев	Тимофеевич
64	Герасимов Платон Никитич	Машинист	male	1996-03-04	Платон	Герасимов	Никитич
65	Власов Эмиль Русланович	Машинист	male	1981-12-18	Эмиль	Власов	Русланович
66	Лукин Алан Артурович	Водитель автомобиля	male	1993-09-01	Алан	Лукин	Артурович
67	Панфилов Герман Вадимович	Водитель автомобиля	male	1980-05-10	Герман	Панфилов	Вадимович
68	Субботин Марк Леонидович	Водитель автомобиля	male	1997-11-23	Марк	Субботин	Леонидович
69	Князев Клим Владиславович	Водитель автомобиля	male	1984-02-14	Клим	Князев	Владиславович
70	Белоусов Эрик Денисович	Водитель автомобиля	male	1992-07-31	Эрик	Белоусов	Денисович
71	Шаров Венедикт Арсеньевич	Водитель автомобиля	male	1978-04-27	Венедикт	Шаров	Арсеньевич
72	Маслов Мирон Борисович	Водитель автомобиля	male	1995-08-09	Мирон	Маслов	Борисович
73	Кабанов Адриан Данилович	Водитель автомобиля	male	1986-01-13	Адриан	Кабанов	Данилович
74	Коновалов Савелий Матвеевич	Водитель автомобиля	male	1990-06-05	Савелий	Коновалов	Матвеевич
75	Жуков Фаддей Тимофеевич	Водитель автомобиля	male	1982-10-19	Фаддей	Жуков	Тимофеевич
76	Овчинников Лаврентий Григорьевич	Водитель автомобиля	male	1998-12-07	Лаврентий	Овчинников	Григорьевич
77	Бирюков Игнат Степанович	Водитель автомобиля	male	1979-03-29	Игнат	Бирюков	Степанович
78	Агафонов Афанасий Олегович	Электромонтер	male	1994-09-14	Афанасий	Агафонов	Олегович
79	Рябов Вадим Петрович	Электромонтер	male	1983-05-22	Вадим	Рябов	Петрович
80	Мельников Кузьма Валерьевич	Электромонтер	male	1988-11-06	Кузьма	Мельников	Валерьевич
81	Горшков Фрол Геннадьевич	Электромонтер	male	1991-02-18	Фрол	Горшков	Геннадьевич
82	Зуев Трофим Ильич	Электромонтер	male	1980-07-05	Трофим	Зуев	Ильич
83	Харитонов Евсей Фёдорович	Электромонтер	male	1996-10-30	Евсей	Харитонов	Фёдорович
84	Гусев Анисим Александрович	Электромонтер	male	1977-12-15	Анисим	Гусев	Александрович
85	Ларионов Захар Дмитриевич	Электромонтер	male	1989-04-09	Захар	Ларионов	Дмитриевич
86	Филимонов Влас Николаевич	Электромонтер	male	1992-08-24	Влас	Филимонов	Николаевич
87	Бобров Дорофей Викторович	Электромонтер	male	1985-01-31	Дорофей	Бобров	Викторович
88	Самойлов Кондрат Сергеевич	Электромонтер	male	1993-06-16	Кондрат	Самойлов	Сергеевич
89	Воробьёв Арслан Андреевич	Электромонтер	male	1981-09-07	Арслан	Воробьёв	Андреевич
90	Сергеев Аким Романович	Слесарь-ремонтник	male	1997-03-13	Аким	Сергеев	Романович
91	Андреев Никанор Игоревич	Слесарь-ремонтник	male	1984-07-28	Никанор	Андреев	Игоревич
92	Волков Тихон Эдуардович	Слесарь-ремонтник	male	1990-12-02	Тихон	Волков	Эдуардович
93	Глухов Макар Станиславович	Слесарь-ремонтник	male	1978-05-19	Макар	Глухов	Станиславович
94	Абрамов Ратмир Вячеславович	Слесарь-ремонтник	male	1995-10-11	Ратмир	Абрамов	Вячеславович
95	Щербаков Любомир Аркадьевич	Слесарь-ремонтник	male	1982-02-27	Любомир	Щербаков	Аркадьевич
96	Мартынов Назар Тимурович	Слесарь-ремонтник	male	1998-06-14	Назар	Мартынов	Тимурович
97	Емельянов Яромир Денисович	Слесарь-ремонтник	male	1986-09-23	Яромир	Емельянов	Денисович
98	Колесников Камиль Русланович	Слесарь-ремонтник	male	1991-04-08	Камиль	Колесников	Русланович
99	Фролов Дамир Артурович	Слесарь-ремонтник	male	1980-01-14	Дамир	Фролов	Артурович
100	Куликов Искандер Эмилевич	Слесарь-ремонтник	male	1994-08-29	Искандер	Куликов	Эмилевич
101	Зимин Тимур Маратович	Слесарь-ремонтник	male	1987-11-16	Тимур	Зимин	Маратович
102	Ильин Сабир Равилевич	Бурильщик	male	1999-05-04	Сабир	Ильин	Равилевич
591	Гость Хабибуллин Айрат	Электрогазосварщик	\N	\N	\N	\N	\N
103	Соболев Булат Альбертович	Бурильщик	male	1983-03-21	Булат	Соболев	Альбертович
104	Мясников Айдар Мансурович	Бурильщик	male	1977-10-07	Айдар	Мясников	Мансурович
105	Цветков Ильдар Рашидович	Бурильщик	male	1992-01-26	Ильдар	Цветков	Рашидович
106	Нестеров Марат Ирекович	Бурильщик	male	1985-07-12	Марат	Нестеров	Ирекович
107	Лапин Рушан Фаритович	Бурильщик	male	1996-12-03	Рушан	Лапин	Фаритович
108	Дроздов Асланбек Салманович	Бурильщик	male	1981-06-18	Асланбек	Дроздов	Салманович
109	Архипов Русланбек Хасанович	Бурильщик	male	1990-09-09	Русланбек	Архипов	Хасанович
110	Шестаков Мурат Заурович	Бурильщик	male	1979-04-25	Мурат	Шестаков	Заурович
111	Беляев Арсен Борисович	Бурильщик	male	1988-02-13	Арсен	Беляев	Борисович
112	Воронов Салават Наилевич	Бурильщик	male	1994-11-30	Салават	Воронов	Наилевич
113	Лобанов Айрат Рафикович	Бурильщик	male	1982-08-05	Айрат	Лобанов	Рафикович
114	Голубев Замир Ахметович	Бурильщик	male	1998-05-17	Замир	Голубев	Ахметович
115	Исаков Газинур Габдуллович	Бурильщик	male	1976-03-11	Газинур	Исаков	Габдуллович
116	Осипов Рафаэль Ринатович	Бурильщик	male	1993-10-22	Рафаэль	Осипов	Ринатович
117	Третьяков Ильгиз Асхатович	Оператор ДНГ	male	1986-01-09	Ильгиз	Третьяков	Асхатович
118	Мамонтов Данис Фаридович	Оператор ДНГ	male	1991-07-30	Данис	Мамонтов	Фаридович
119	Гордеев Айнур Дамирович	Оператор ДНГ	male	1980-04-16	Айнур	Гордеев	Дамирович
120	Дьячков Ленар Ильдусович	Оператор ДНГ	male	1997-09-02	Ленар	Дьячков	Ильдусович
121	Русаков Азат Рамилевич	Оператор ДНГ	male	1984-12-27	Азат	Русаков	Рамилевич
122	Лыткин Роберт Альфритович	Оператор ДНГ	male	1995-06-10	Роберт	Лыткин	Альфритович
123	Жданов Инсаф Шамилевич	Оператор ДНГ	male	1978-02-22	Инсаф	Жданов	Шамилевич
124	Котов Альберт Газинурович	Оператор ДНГ	male	1989-11-14	Альберт	Котов	Газинурович
125	Сазонов Рашид Мунирович	Оператор ДНГ	male	1996-08-06	Рашид	Сазонов	Мунирович
126	Поляков Карим Зуфарович	Оператор ДНГ	male	1983-05-29	Карим	Поляков	Зуфарович
127	Меркулов Ирек Асгатович	Оператор ДНГ	male	1990-01-15	Ирек	Меркулов	Асгатович
128	Быков Фанис Аглямович	Оператор ДНГ	male	1987-07-03	Фанис	Быков	Аглямович
129	Кондратьев Ильшат Рафаилович	Оператор ДНГ	male	1992-04-19	Ильшат	Кондратьев	Рафаилович
130	Копылов Радик Ахнафович	Оператор ДНГ	male	1981-10-31	Радик	Копылов	Ахнафович
131	Чернов Гаяз Габдрахманович	Оператор ДНГ	male	1994-03-25	Гаяз	Чернов	Габдрахманович
132	Ширяев Нафис Мисбахович	Мастер участка	male	1985-08-12	Нафис	Ширяев	Мисбахович
133	Молчанов Мансур Фаязович	Мастер участка	male	1979-12-01	Мансур	Молчанов	Фаязович
134	Агапов Халил Галимзянович	Мастер участка	male	1993-06-27	Халил	Агапов	Галимзянович
135	Левин Ришат Нуриевич	Мастер участка	male	1986-02-11	Ришат	Левин	Нуриевич
136	Терехов Ильнур Фанилевич	Мастер участка	male	1997-10-05	Ильнур	Терехов	Фанилевич
137	Карпов Динар Азатович	Мастер участка	male	1982-07-20	Динар	Карпов	Азатович
138	Гуляев Альфред Рауфович	Мастер участка	male	1991-04-09	Альфред	Гуляев	Рауфович
139	Мишин Энгель Нагимович	Мастер участка	male	1980-09-23	Энгель	Мишин	Нагимович
140	Панов Вильдан Ильгизович	Мастер участка	male	1995-01-18	Вильдан	Панов	Ильгизович
141	Рожков Асхат Сагитович	Начальник смены	male	1984-06-06	Асхат	Рожков	Сагитович
142	Зверев Раиль Маннапович	Начальник смены	male	1978-11-03	Раиль	Зверев	Маннапович
143	Потапов Ильмир Бариевич	Начальник смены	male	1992-03-27	Ильмир	Потапов	Бариевич
144	Кудрявцев Мунир Закиевич	Начальник смены	male	1988-08-14	Мунир	Кудрявцев	Закиевич
145	Родионов Габдулла Сабирович	Начальник смены	male	1996-12-08	Габдулла	Родионов	Сабирович
146	Крюков Фаяз Камилевич	Начальник смены	male	1981-05-25	Фаяз	Крюков	Камилевич
147	Беляков Наиль Гараевич	Начальник смены	male	1990-10-19	Наиль	Беляков	Гараевич
148	Большаков Рамис Ильгизарович	Начальник смены	male	1987-02-07	Рамис	Большаков	Ильгизарович
149	Селезнёв Айбулат Данисович	Начальник смены	male	1994-07-15	Айбулат	Селезнёв	Данисович
150	Латышев Рамзис Салихович	Электрогазосварщик	male	1979-04-02	Рамзис	Латышев	Салихович
151	Блохин Ринат Замирович	Электрогазосварщик	male	1985-09-28	Ринат	Блохин	Замирович
592	Сидоров Иван	Инженер	\N	\N	\N	\N	\N
152	Наумов Салим Кирамович	Электрогазосварщик	male	1993-01-11	Салим	Наумов	Кирамович
153	Зыков Аслан Гафурович	Электрогазосварщик	male	1988-06-22	Аслан	Зыков	Гафурович
154	Дорофеев Даян Альтафович	Электрогазосварщик	male	1997-03-09	Даян	Дорофеев	Альтафович
155	Токарев Загир Фаритович	Электрогазосварщик	male	1982-12-24	Загир	Токарев	Фаритович
156	Анисимов Гамиль Асхатович	Электрогазосварщик	male	1991-08-17	Гамиль	Анисимов	Асхатович
157	Ермаков Ильяс Халитович	Электрогазосварщик	male	1980-02-13	Ильяс	Ермаков	Халитович
158	Брагин Ранис Назипович	Электрогазосварщик	male	1996-10-06	Ранис	Брагин	Назипович
159	Воронцов Айназ Рафаэлевич	Геолог	male	1984-05-30	Айназ	Воронцов	Рафаэлевич
160	Шмелёв Дамир Камилевич	Геолог	male	1977-09-15	Дамир	Шмелёв	Камилевич
161	Денисов Артур Мухаметович	Геолог	male	1992-01-03	Артур	Денисов	Мухаметович
162	Митрофанов Эмиль Харисович	Геолог	male	1986-06-19	Эмиль	Митрофанов	Харисович
163	Мамонова Елена Александровна	Геолог	female	1989-08-27	Елена	Мамонова	Александровна
164	Вишняков Валентин Игоревич	Механик	male	1983-04-14	Валентин	Вишняков	Игоревич
165	Галкин Олег Николаевич	Механик	male	1990-09-07	Олег	Галкин	Николаевич
166	Назаров Денис Петрович	Механик	male	1985-01-22	Денис	Назаров	Петрович
167	Аксёнов Максим Дмитриевич	Механик	male	1994-06-15	Максим	Аксёнов	Дмитриевич
168	Лаптев Владимир Сергеевич	Механик	male	1981-12-08	Владимир	Лаптев	Сергеевич
169	Зотов Андрей Александрович	Механик	male	1978-07-31	Андрей	Зотов	Александрович
170	Кудряшов Павел Владимирович	Механик	male	1993-02-19	Павел	Кудряшов	Владимирович
171	Горбачёв Сергей Викторович	Механик	male	1988-11-04	Сергей	Горбачёв	Викторович
172	Тихонов Роман Андреевич	Механик	male	1997-05-26	Роман	Тихонов	Андреевич
173	Агапова Ольга Викторовна	Механик	female	1984-10-10	Ольга	Агапова	Викторовна
174	Федотова Татьяна Сергеевна	Лаборант	female	1990-04-02	Татьяна	Федотова	Сергеевна
175	Климова Наталья Игоревна	Лаборант	female	1982-09-18	Наталья	Климова	Игоревна
176	Никифорова Светлана Александровна	Лаборант	female	1987-12-29	Светлана	Никифорова	Александровна
177	Беляева Юлия Владимировна	Лаборант	female	1995-06-13	Юлия	Беляева	Владимировна
178	Сорокина Марина Дмитриевна	Кладовщик	female	1981-03-07	Марина	Сорокина	Дмитриевна
179	Волкова Алина Олеговна	Кладовщик	female	1992-08-23	Алина	Волкова	Олеговна
180	Киселёва Анна Романовна	Кладовщик	female	1986-11-15	Анна	Киселёва	Романовна
181	Емельянова Дарья Игоревна	Инженер	female	1998-01-09	Дарья	Емельянова	Игоревна
182	Маркова Кристина Павловна	Инженер	female	1989-07-22	Кристина	Маркова	Павловна
183	Калинина Евгения Валерьевна	Инженер	female	1994-04-05	Евгения	Калинина	Валерьевна
184	Медведева Вероника Станиславовна	Техник	female	1985-09-30	Вероника	Медведева	Станиславовна
185	Игнатова Полина Денисовна	Техник	female	1991-02-14	Полина	Игнатова	Денисовна
186	Фомина Валерия Артёмовна	Техник	female	1983-06-28	Валерия	Фомина	Артёмовна
187	Борисова Анастасия Егоровна	Электромонтер	female	1996-11-11	Анастасия	Борисова	Егоровна
188	Логинова Екатерина Тимуровна	Слесарь-ремонтник	female	1988-05-19	Екатерина	Логинова	Тимуровна
189	Данилова Алиса Эдуардовна	Оператор ДНГ	female	1999-08-03	Алиса	Данилова	Эдуардовна
190	Семёнова Василиса Руслановна	Мастер участка	female	1980-12-17	Василиса	Семёнова	Руслановна
191	Титова Злата Арсеньевна	Водитель автомобиля	female	1993-03-26	Злата	Титова	Арсеньевна
192	Ковалёва Ярослава Даниловна	Бурильщик	female	1986-10-01	Ярослава	Ковалёва	Даниловна
577	Поцелуев Артемий Сергеевич	Инженер	\N	\N	\N	\N	\N
578	Галкин Виктор Алексеевич	Техник	\N	\N	\N	\N	\N
579	Калашников Илья Николаевич	Техник	\N	\N	\N	\N	\N
580	Гостевой Сидоров Иван Петрович	Техник	\N	\N	\N	\N	\N
581	Гостевая Орлова Светлана	Инженер	\N	\N	\N	\N	\N
582	Гость Петров Аркадий	Геолог	\N	\N	\N	\N	\N
583	Гость Захаров Илья	Механик	\N	\N	\N	\N	\N
584	Гость Сафин Рустем	Бурильщик	\N	\N	\N	\N	\N
585	Гостевая Фёдорова Марина	Оператор ДНГ	\N	\N	\N	\N	\N
586	Гость Кукушкин Пётр	Электромонтер	\N	\N	\N	\N	\N
587	Гость Семёнов Рушан	Слесарь-ремонтник	\N	\N	\N	\N	\N
588	Гость Закиров Ильдар	Машинист	\N	\N	\N	\N	\N
589	Гость Яковлев Марат	Водитель автомобиля	\N	\N	\N	\N	\N
595	Сафин Рустем	Геолог	\N	\N	\N	\N	\N
596	Семёнов Рушан	Геолог	\N	\N	\N	\N	\N
597	Орлова Светлана	Геолог	\N	\N	\N	\N	\N
598	Закиров Ильдар	Геолог	\N	\N	\N	\N	\N
599	Хабибуллин Айрат	Геолог	\N	\N	\N	\N	\N
600	Фёдоров Сергей	Геолог	\N	\N	\N	\N	\N
601	Михайлов Артем	Геолог	\N	\N	\N	\N	\N
602	Козлов Павел	Геолог	\N	\N	\N	\N	\N
603	Новиков Денис	Геолог	\N	\N	\N	\N	\N
604	Иванов Сергей	Инженер	\N	\N	\N	\N	\N
605	Смирнов Алексей	Водитель	\N	\N	\N	\N	\N
606	Кузнецов Николай	Инженер	\N	\N	\N	\N	\N
607	Попов Андрей	Инженер	\N	\N	\N	\N	\N
608	Соколов Дмитрий	Инженер	\N	\N	\N	\N	\N
609	Гостевой Иван	Инженер	\N	\N	\N	\N	\N
610	Формальный Пётр	Геолог	\N	\N	\N	\N	\N
611	Гостевой Пётр	Геолог	\N	\N	\N	\N	\N
612	Смешанный Алексей	Водитель	\N	\N	\N	\N	\N
613	Только договор Игорь	Инженер	\N	\N	\N	\N	\N
614	Только ФИО Игорь	Инженер	\N	\N	\N	\N	\N
615	Замена Старый	Инженер	\N	\N	\N	\N	\N
616	Тестов Тестович	Инженер	\N	\N	\N	\N	\N
617	Гость Без Договора	Инженер	\N	\N	\N	\N	\N
618	Нет ЕОЛ	Инженер	\N	\N	\N	\N	\N
619	Нет ничего	Водитель	\N	\N	\N	\N	\N
620	Дубликат Проверка	Геолог	\N	\N	\N	\N	\N
621	Иванов Иван	Инженер	\N	\N	\N	\N	\N
622	Петров Пётр	Геолог	\N	\N	\N	\N	\N
623	Сидоров С.	Водитель	\N	\N	\N	\N	\N
624	Козлов К.	Техник	\N	\N	\N	\N	\N
625	(пусто)	Инженер	\N	\N	\N	\N	\N
626	Корректный	Инженер	\N	\N	\N	\N	\N
627	Нет договора	Геолог	\N	\N	\N	\N	\N
628	Нет договора и ЕОЛ?	Водитель	\N	\N	\N	\N	\N
629	Фаизова Софья	Повар	Ж	2026-06-22	\N	\N	\N
630	Андронов Артем Андреевич	Рабочий	М	2026-06-27	\N	\N	\N
\.


--
-- TOC entry 5134 (class 0 OID 16631)
-- Dependencies: 227
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name) FROM stdin;
1	admin
2	user
3	field_admin
\.


--
-- TOC entry 5136 (class 0 OID 16637)
-- Dependencies: 229
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (id, room_number, field_id, capacity, location_id, path_id, room_unique_id, status) FROM stdin;
3	102	2	2	51	1	2a	\N
4	103	2	2	51	1	2a	\N
5	106	2	2	51	1	2a	\N
6	108	2	2	51	1	2a	\N
7	108	2	2	51	1	2b	\N
8	109	2	2	51	1	2b	\N
9	110	2	2	51	1	2b	\N
10	111	2	2	51	1	2a	\N
11	112	2	2	51	1	2b	\N
12	113	2	2	51	1	2b	\N
13	115	2	2	51	245	2b	\N
14	117	2	2	51	245	2a	\N
15	118	2	2	51	245	2a	\N
16	118	2	2	51	245	2b	\N
17	119	2	2	51	245	2a	\N
18	119	2	2	51	245	2b	\N
19	121	2	2	51	245	2a	\N
20	123	2	2	51	245	2a	\N
21	125	2	2	51	245	2a	\N
22	126	2	2	51	245	2a	\N
23	126	2	2	51	245	2b	\N
24	127	2	1	51	245	1a	\N
25	201	2	2	51	246	2a	\N
26	201	2	2	51	246	2b	\N
27	202	2	2	51	246	2a	\N
28	202	2	2	51	246	2b	\N
29	203 (гостевой)	2	1	51	246	1a	\N
30	206	2	2	51	246	2a	\N
31	206	2	2	51	246	2b	\N
32	207	2	2	51	246	2a	\N
33	208	2	2	51	246	2b	\N
34	209	2	2	51	246	2b	\N
35	210	2	2	51	246	2a	\N
36	210	2	2	51	246	2b	\N
37	211	2	2	51	246	2a	\N
38	211	2	2	51	246	2b	\N
39	212	2	2	51	246	2a	\N
40	213	2	2	51	247	2a	\N
41	213	2	2	51	247	2b	\N
42	214	2	2	51	247	2a	\N
43	214	2	2	51	247	2b	\N
44	215	2	2	51	247	2a	\N
45	215	2	2	51	247	2b	\N
46	216 (гостевой)	2	2	51	247	2a	\N
47	218	2	2	51	247	2a	\N
48	218	2	2	51	247	2b	\N
49	219	2	1	51	247	1a	\N
50	220 (гостевой)	2	2	51	247	2a	\N
51	221	2	2	51	247	2a	\N
52	221	2	2	51	247	2b	\N
53	222	2	2	51	247	2a	\N
54	222	2	2	51	247	2b	\N
55	223	2	2	51	247	2a	\N
56	223	2	2	51	247	2b	\N
57	224	2	2	51	247	2a	\N
58	102	2	2	51	1	2b	\N
59	109	2	2	51	1	2a	\N
60	110	2	2	51	1	2a	\N
61	112	2	2	51	1	2a	\N
62	114	2	2	51	1	2a	\N
63	115	2	2	51	245	2a	\N
64	122	2	2	51	245	2a	\N
65	124	2	2	51	245	2a	\N
66	125	2	2	51	245	2b	\N
67	204	2	1	51	246	1a	\N
68	208	2	2	51	246	2a	\N
69	217	2	1	51	247	1a	\N
70	205	1	2	51	246	2a	\N
71	205	1	2	51	246	2b	\N
72	Кедр"К.04.2.1.\n(12а)	1	2	52	248	2a	\N
73	Кедр"К.04.2.1.\n(12а)	1	2	52	248	2b	\N
74	Ермак (46)	1	2	52	248	2a	\N
75	Ермак (46)	1	2	52	248	2b	\N
76	Ермак (53)	1	2	52	248	2a	\N
77	Ермак (55)	1	2	52	248	2a	\N
78	Ермак (48)	1	2	52	248	2a	\N
79	К-10 (21)	1	2	52	248	2a	\N
80	Медведь-02 (41)	1	2	52	248	2a	\N
81	Ермак (б/н)	1	2	52	248	2a	\N
82	К-4К (не благ. 39)	1	2	52	248	2a	\N
83	К-4 (12)	1	4	52	248	4a	\N
84	К-4 (12)	1	4	52	248	4b	\N
86	к-4 (38)	1	4	52	248	4b	\N
87	-	1	4	52	248	4a	\N
88	К-4К                         (не благ. б/н)	1	4	52	248	4b	\N
89	Кедр-10	1	4	52	248	4a	\N
90	Новый (б/н)	1	4	52	248	4a	\N
91	104	1	2	51	1	2a	\N
92	107	1	1	51	1	1a	\N
93	113	1	2	51	1	2a	\N
94	207	1	2	51	246	2b	\N
95	Ермак (53)	1	2	52	248	2b	\N
96	Ермак (55)	1	1	52	248	1a	\N
97	Ермак (23)	1	2	52	248	2a	\N
98	Ермак (б/н)	1	2	52	248	2b	\N
99	К-4К                         (не благ. б/н)	1	4	52	248	4a	\N
100	новый (б/№)	1	2	52	248	2a	\N
101	новый (б/№)	1	2	52	248	2b	\N
102	107	1	2	51	1	2a	\N
103	116	1	2	51	245	2a	\N
104	116	1	2	51	245	2b	\N
105	120	1	2	51	245	2a	\N
106	120	1	2	51	245	2b	\N
107	новый (б/№)	1	4	52	248	4a	\N
109	105	1	1	51	1	1a	\N
110	Ермак (55)	1	3	52	248	3a	\N
111	Ермак (48)	1	3	52	248	3a	\N
113	105	1	2	51	1	2a	\N
1	101	2	2	51	1	2a	0
116	999	1	2	51	245	2a	0
114	101	1	1	1	253	\N	\N
115	101	1	2	1	253	\N	\N
2	101	2	2	51	1	2b	0
112	Медведь-02 (41)	1	3	52	248	3a	0
85	к-4 (38)	1	4	52	248	4a	0
108	209	1	1	51	246	1a	0
117	222	3	1	54	254	222a	1
118	221	3	1	54	254	221a	1
119	220	3	1	54	254	220a	1
120	219	3	1	54	254	219a	1
121	218	3	2	54	254	218a	1
122	217	3	2	54	254	217a	1
123	216	3	2	54	254	216a	1
124	215	3	2	54	254	215a	1
125	215	3	2	54	254	215b	1
126	214	3	2	54	254	214a	1
127	214	3	2	54	254	214b	1
128	213	3	2	54	254	213a	1
129	213	3	2	54	254	213b	1
130	212	3	2	54	254	212a	1
131	212	3	2	54	254	212b	1
132	211	3	2	54	254	211a	1
133	211	3	3	54	254	211b	1
134	210	3	2	54	254	210a	1
135	210	3	2	54	254	210b	1
136	209	3	2	54	254	209a	1
137	209	3	2	54	254	209b	1
138	208	3	5	54	254	208a	1
139	206	3	3	54	254	206a	1
140	206	3	2	54	254	206b	1
141	205	3	2	54	254	205a	1
142	205	3	2	54	254	205b	1
143	204	3	2	54	254	204a	1
144	204	3	2	54	254	204b	1
145	203	3	2	54	254	203a	1
146	203	3	2	54	254	203b	1
147	202	3	2	54	254	202a	1
148	202	3	2	54	254	202b	1
149	201	3	2	54	254	201a	1
150	201	3	2	54	254	201b	1
151	108	3	3	54	254	108a	1
152	108	3	3	54	254	108b	1
153	106	3	2	54	254	106a	1
154	106	3	2	54	254	106b	1
155	105	3	2	54	254	105a	1
156	105	3	2	54	254	105b	1
157	105	3	83	54	254	105c	1
158	1	3	2	55	254	1a	1
159	1	3	2	55	254	1b	1
160	2	3	2	55	254	2a	1
161	2	3	2	55	254	2b	1
162	3	3	2	55	254	3a	1
163	3	3	2	55	254	3b	1
164	4	3	2	55	254	4a	1
165	4	3	2	55	254	4b	1
166	5	3	2	55	254	5a	1
167	5	3	2	55	254	5b	1
168	6	3	2	55	254	6a	1
169	6	3	2	55	254	6b	1
170	7	3	1	55	254	7a	1
171	8	3	1	55	254	8a	1
172	9	3	2	55	254	9a	1
173	9	3	2	55	254	9b	1
174	10	3	2	55	254	10a	1
175	10	3	2	55	254	10b	1
176	11	3	2	55	254	11a	1
177	11	3	2	55	254	11b	1
178	12	3	2	55	254	12a	1
179	12	3	2	55	254	12b	1
180	14	3	2	55	254	14a	1
181	14	3	2	55	254	14b	1
182	15	3	1	55	254	15a	1
183	16	3	1	55	254	16a	1
184	16	3	48	55	254	16b	1
185	вагон №8 ГПН-Снабжение	3	1	52	254	вагон №8 ГПН-Снабжениеa	1
186	вагон №9 ГПН-Снабжение	3	2	52	254	вагон №9 ГПН-Снабжениеa	1
187	вагон №10	3	2	52	254	вагон №10a	1
188	Вагон №14 (ВИП) ГПНВ	3	2	52	254	Вагон №14 (ВИП) ГПНВa	1
189	Вагон №15 (ВИП) ГПНВ	3	2	52	254	Вагон №15 (ВИП) ГПНВa	1
190	вагон №16 ГПН-Снабжение	3	2	52	254	вагон №16 ГПН-Снабжениеa	1
191	вагон №16 ГПН-Снабжение	3	11	52	254	вагон №16 ГПН-Снабжениеb	1
192	вагон №2	3	5	56	254	вагон №2a	1
193	вагон №3	3	8	56	254	вагон №3a	1
194	вагон №3	3	31	56	254	вагон №3b	1
\.


--
-- TOC entry 5138 (class 0 OID 16645)
-- Dependencies: 231
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, role_id, field_id, resident_id) FROM stdin;
5	kyzma	$2b$12$JOEcLmcwyUSTJO2FBJ2kqO6VQSRcFqqeeesbOB.NsN5vcB.aP7dky	2	1	\N
6	admin_yral	$2b$12$X4YdhrmuBPcpvzy7ws19U.NUQ.hk2fARptHuBHApKKyDIxxwxJXdS	1	3	\N
7	admin_1	$2b$12$Tw2FXWbpfKdiiIsEK65X1.Z2aQGx86Zx.wtBQcoWDhdLCbejQ.3qu	1	4	\N
9	Kola	$2b$12$1gdhx8FkSiV/B9fYtW8CIOsE5fLT7cYo6Q14WMcG2eO7rehAGS/Xu	2	1	4
8	admin_kamen	$2b$12$wrStKpfbEeKIcGZlKsAsCebqQnzk20QenB0QSH25/qK9NGV9MIcua	1	10	5
1	admin	$2b$12$sZf5QALblDogiQyMsJwEruqaVlt.MAYySDJWPra93g0ktO9TvJjAO	1	1	42
\.


--
-- TOC entry 5169 (class 0 OID 0)
-- Dependencies: 235
-- Name: contract_counters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contract_counters_id_seq', 2, true);


--
-- TOC entry 5170 (class 0 OID 0)
-- Dependencies: 220
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_id_seq', 578, true);


--
-- TOC entry 5171 (class 0 OID 0)
-- Dependencies: 222
-- Name: fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fields_id_seq', 16, true);


--
-- TOC entry 5172 (class 0 OID 0)
-- Dependencies: 224
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_id_seq', 56, true);


--
-- TOC entry 5173 (class 0 OID 0)
-- Dependencies: 226
-- Name: paths_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.paths_id_seq', 254, true);


--
-- TOC entry 5174 (class 0 OID 0)
-- Dependencies: 233
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.refresh_tokens_id_seq', 21, true);


--
-- TOC entry 5175 (class 0 OID 0)
-- Dependencies: 237
-- Name: request_before_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.request_before_id_seq', 69, true);


--
-- TOC entry 5176 (class 0 OID 0)
-- Dependencies: 241
-- Name: requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requests_id_seq', 801, true);


--
-- TOC entry 5177 (class 0 OID 0)
-- Dependencies: 239
-- Name: residents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.residents_id_seq', 630, true);


--
-- TOC entry 5178 (class 0 OID 0)
-- Dependencies: 228
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, true);


--
-- TOC entry 5179 (class 0 OID 0)
-- Dependencies: 230
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_id_seq', 194, true);


--
-- TOC entry 5180 (class 0 OID 0)
-- Dependencies: 232
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 9, true);


--
-- TOC entry 4956 (class 2606 OID 25959)
-- Name: contract_counters contract_counters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contract_counters
    ADD CONSTRAINT contract_counters_pkey PRIMARY KEY (id);


--
-- TOC entry 4958 (class 2606 OID 25961)
-- Name: contract_counters contract_counters_prefix_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contract_counters
    ADD CONSTRAINT contract_counters_prefix_key UNIQUE (prefix);


--
-- TOC entry 4931 (class 2606 OID 16670)
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- TOC entry 4933 (class 2606 OID 16672)
-- Name: fields fields_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_pkey PRIMARY KEY (id);


--
-- TOC entry 4935 (class 2606 OID 16674)
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- TOC entry 4937 (class 2606 OID 16676)
-- Name: paths paths_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paths
    ADD CONSTRAINT paths_pkey PRIMARY KEY (id);


--
-- TOC entry 4952 (class 2606 OID 25932)
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 4954 (class 2606 OID 25934)
-- Name: refresh_tokens refresh_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_hash_key UNIQUE (token_hash);


--
-- TOC entry 4960 (class 2606 OID 26021)
-- Name: request_before request_before_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_pkey PRIMARY KEY (id);


--
-- TOC entry 4964 (class 2606 OID 26068)
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


--
-- TOC entry 4962 (class 2606 OID 26049)
-- Name: residents residents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.residents
    ADD CONSTRAINT residents_pkey PRIMARY KEY (id);


--
-- TOC entry 4939 (class 2606 OID 16682)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 4941 (class 2606 OID 16684)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 4944 (class 2606 OID 16686)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- TOC entry 4946 (class 2606 OID 16688)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4948 (class 2606 OID 16690)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4949 (class 1259 OID 25941)
-- Name: idx_refresh_tokens_token_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_refresh_tokens_token_hash ON public.refresh_tokens USING btree (token_hash);


--
-- TOC entry 4950 (class 1259 OID 25940)
-- Name: idx_refresh_tokens_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_refresh_tokens_user_id ON public.refresh_tokens USING btree (user_id);


--
-- TOC entry 4942 (class 1259 OID 16696)
-- Name: ix_rooms_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_rooms_id ON public.rooms USING btree (id);


--
-- TOC entry 4965 (class 2606 OID 16697)
-- Name: rooms fk_field; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_field FOREIGN KEY (field_id) REFERENCES public.fields(id);


--
-- TOC entry 4966 (class 2606 OID 16702)
-- Name: rooms fk_rooms_location; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_rooms_location FOREIGN KEY (location_id) REFERENCES public.locations(id) ON DELETE SET NULL;


--
-- TOC entry 4967 (class 2606 OID 16707)
-- Name: rooms fk_rooms_path; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_rooms_path FOREIGN KEY (path_id) REFERENCES public.paths(id) ON DELETE SET NULL;


--
-- TOC entry 4970 (class 2606 OID 25935)
-- Name: refresh_tokens refresh_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4971 (class 2606 OID 26027)
-- Name: request_before request_before_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE CASCADE;


--
-- TOC entry 4972 (class 2606 OID 26032)
-- Name: request_before request_before_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(id) ON DELETE SET NULL;


--
-- TOC entry 4973 (class 2606 OID 26022)
-- Name: request_before request_before_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4974 (class 2606 OID 26069)
-- Name: requests requests_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id) ON DELETE CASCADE;


--
-- TOC entry 4975 (class 2606 OID 26079)
-- Name: requests requests_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE CASCADE;


--
-- TOC entry 4976 (class 2606 OID 26089)
-- Name: requests requests_resident_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_resident_id_fkey FOREIGN KEY (resident_id) REFERENCES public.residents(id) ON DELETE SET NULL;


--
-- TOC entry 4977 (class 2606 OID 26084)
-- Name: requests requests_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(id) ON DELETE SET NULL;


--
-- TOC entry 4978 (class 2606 OID 26074)
-- Name: requests requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4968 (class 2606 OID 16742)
-- Name: users users_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id);


--
-- TOC entry 4969 (class 2606 OID 16747)
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- TOC entry 5156 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2026-06-28 00:14:17

--
-- PostgreSQL database dump complete
--

\unrestrict oHSTRIiKeULM5Ts2ItJzFa3lZ3PVwjNhpIHIAqtdYyJOAwQfWqXalRDlAA1J0kZ

