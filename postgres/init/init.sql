--
-- PostgreSQL database dump
--

\restrict qYemS5imix88Tw02LuIKMExVfsrT1BK9w5NgA5NF2UZaym5WMhegK1Qf6NLx87q

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-07-10 02:58:57

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
-- TOC entry 5 (class 2615 OID 2200)
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
-- TOC entry 219 (class 1259 OID 26122)
-- Name: contract_counters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contract_counters (
    id integer NOT NULL,
    prefix character varying NOT NULL,
    last_number integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.contract_counters OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 26131)
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
-- Dependencies: 220
-- Name: contract_counters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contract_counters_id_seq OWNED BY public.contract_counters.id;


--
-- TOC entry 221 (class 1259 OID 26132)
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 26137)
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
-- Dependencies: 222
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- TOC entry 223 (class 1259 OID 26138)
-- Name: fields; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fields (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.fields OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 26143)
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
-- Dependencies: 224
-- Name: fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fields_id_seq OWNED BY public.fields.id;


--
-- TOC entry 225 (class 1259 OID 26144)
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 26151)
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
-- Dependencies: 226
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- TOC entry 227 (class 1259 OID 26152)
-- Name: paths; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paths (
    id integer NOT NULL,
    description character varying NOT NULL
);


ALTER TABLE public.paths OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 26159)
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
-- Dependencies: 228
-- Name: paths_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.paths_id_seq OWNED BY public.paths.id;


--
-- TOC entry 229 (class 1259 OID 26160)
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
-- TOC entry 230 (class 1259 OID 26170)
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
-- Dependencies: 230
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.refresh_tokens_id_seq OWNED BY public.refresh_tokens.id;


--
-- TOC entry 231 (class 1259 OID 26171)
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
-- TOC entry 232 (class 1259 OID 26186)
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
-- Dependencies: 232
-- Name: request_before_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.request_before_id_seq OWNED BY public.request_before.id;


--
-- TOC entry 233 (class 1259 OID 26187)
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
-- TOC entry 234 (class 1259 OID 26202)
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
-- Dependencies: 234
-- Name: requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.requests_id_seq OWNED BY public.requests.id;


--
-- TOC entry 235 (class 1259 OID 26203)
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
-- TOC entry 236 (class 1259 OID 26210)
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
-- Dependencies: 236
-- Name: residents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.residents_id_seq OWNED BY public.residents.id;


--
-- TOC entry 237 (class 1259 OID 26211)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 26216)
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
-- Dependencies: 238
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 239 (class 1259 OID 26217)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    id integer NOT NULL,
    room_number character varying,
    field_id integer,
    capacity integer DEFAULT 0,
    location_id integer,
    path_id integer,
    room_unique_id character varying,
    status integer
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 26224)
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
-- Dependencies: 240
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_id_seq OWNED BY public.rooms.id;


--
-- TOC entry 241 (class 1259 OID 26225)
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
-- TOC entry 242 (class 1259 OID 26231)
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
-- Dependencies: 242
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4911 (class 2604 OID 26232)
-- Name: contract_counters id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contract_counters ALTER COLUMN id SET DEFAULT nextval('public.contract_counters_id_seq'::regclass);


--
-- TOC entry 4913 (class 2604 OID 26233)
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- TOC entry 4914 (class 2604 OID 26234)
-- Name: fields id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fields ALTER COLUMN id SET DEFAULT nextval('public.fields_id_seq'::regclass);


--
-- TOC entry 4915 (class 2604 OID 26235)
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- TOC entry 4916 (class 2604 OID 26236)
-- Name: paths id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paths ALTER COLUMN id SET DEFAULT nextval('public.paths_id_seq'::regclass);


--
-- TOC entry 4917 (class 2604 OID 26237)
-- Name: refresh_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('public.refresh_tokens_id_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 26238)
-- Name: request_before id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before ALTER COLUMN id SET DEFAULT nextval('public.request_before_id_seq'::regclass);


--
-- TOC entry 4922 (class 2604 OID 26239)
-- Name: requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests ALTER COLUMN id SET DEFAULT nextval('public.requests_id_seq'::regclass);


--
-- TOC entry 4925 (class 2604 OID 26240)
-- Name: residents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.residents ALTER COLUMN id SET DEFAULT nextval('public.residents_id_seq'::regclass);


--
-- TOC entry 4926 (class 2604 OID 26241)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 4927 (class 2604 OID 26242)
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN id SET DEFAULT nextval('public.rooms_id_seq'::regclass);


--
-- TOC entry 4929 (class 2604 OID 26243)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5126 (class 0 OID 26122)
-- Dependencies: 219
-- Data for Name: contract_counters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contract_counters (id, prefix, last_number) FROM stdin;
\.


--
-- TOC entry 5128 (class 0 OID 26132)
-- Dependencies: 221
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (id, name) FROM stdin;
1	АВТОДЕЛЮКС
2	АНО ДПО "Двипраз"
3	АНО ДПО "ЮУЦ"
4	АО "НПИИЭК"
5	АО Нефтемаш
6	Буртехнология
7	Газпром Газобезопасность
8	ГПН Газобезопасность
9	ГПН-Автоматизация
10	ГПН-Восток
11	ГПН-ИТО
12	ГПН-Снабжение
13	ГПН-СТ
14	ГПН-Энергосистемы
15	ГПН-ЭС
16	ГПН-ЯМАЛ
17	ГПНВ
18	ГПНВ ИТО
19	ГПНЭС ООО "ЯСЦ"
20	ИП Кураков
21	ИП Кураков (ТК СПП)
22	ИПКУРАКОВ
23	ИЦ Энергосервис
24	ИнТех
25	ИТЦ Томский
26	МСБ
27	Навигатор
28	Нефтеспас
29	НЕФТЕМОДУЛЬСТРОЙ
30	Ойл Сервис Гарант
31	ООО " Газпромгазобезопасность"
32	ООО " Газпромнефть сервисные технологии"
33	ООО " Нефтемодульстрой"
34	ООО " Нефтеспас"
35	ООО " НПО Мир"
36	ООО " Русэнерго"
37	ООО " Уралтрубопроводстройпроект"
38	ООО "Автоделюкс"
39	ООО "ГАЦ ЗСР НАКС"
40	ООО "Газпромнефть Бизнес сервис"
41	ООО "Газпромнефть сервисные технологии"
42	ООО "Газпромнефть Ямал"
43	ООО "Инженерный центр Энергосервис"
44	ООО "НИЦ"
45	ООО "НПО ИНТЕРСКАН"
46	ООО "НПФ Пакер"
47	ООО "НьютехВелл Сервис"
48	ООО "Сервис центр ЭПУ"
49	ООО "ТрансСервис"
50	ООО "ЭТ-НТ"
51	ООО ЧОП "Отечество-С"
52	ООО"Комплекс"
53	ООО"ЭТ-НТ"
54	ООО НПФ "Пакер"
55	ООО ТеплоЭнергоПром
56	ОТЕЧЕСТВО-С
57	ПАО "Газпром нефть"
58	ПАО "Гипротюменнефтегаз"
59	Партнеры Томск
60	Правозащита
61	РК "Нефтесервис"
62	Русэнерго
63	Сервис центр ЭПУ
64	СибМедЦентр
65	Сибирское управление Росехнадзора
66	СК Навигатор
67	Техресурс
68	ТИТЦ
69	Транснефть
70	ТрансСервис
71	Уралтехсистемы
72	УТПСП
73	УТСП
74	УТТ Югра
75	УТТ-Югра
76	ФБУ Омский ЦСМ
77	ФБУ Томский ЦСМ
78	ФБУОмскийЦСМ
79	ФГБУ "ЦЛАТИ по СФО"
80	ФГБУ ЦЛАТИ
81	ЮГОРСКИЙ УЧЕБНЫЙ ЦЕНТР
82	Югорский учебный центр
\.


--
-- TOC entry 5130 (class 0 OID 26138)
-- Dependencies: 223
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
-- TOC entry 5132 (class 0 OID 26144)
-- Dependencies: 225
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations (id, name) FROM stdin;
1	АБЖК
2	НОВОЕ ОБЩЕЖИТИЕ
3	ВАГОН
4	ОБЩЕЖИТИЕ УПН
7	общежитие
8	вагон
\.


--
-- TOC entry 5134 (class 0 OID 26152)
-- Dependencies: 227
-- Data for Name: paths; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paths (id, description) FROM stdin;
1	Без пути
7	1 этаж левое крыло
8	1 этаж правое крыло (по)
9	2 этаж левое крыло
10	2 этаж, правое крыло
11	1 этаж, левое крыло
\.


--
-- TOC entry 5136 (class 0 OID 26160)
-- Dependencies: 229
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refresh_tokens (id, user_id, token_hash, expires_at, revoked) FROM stdin;
3	9	258fcbf89d4b2752153e42ed438b531475901ba8a192e371db378fc2c97ccb6e	2026-06-11 02:34:10	t
5	9	f87830b2235f31f1445768170e5e792b5be0af01344575fe34d12d7a9193d5fd	2026-06-11 03:35:28	t
7	9	8ee72d95048789b7128ecbef10104bc6b96f198b730d2a55e2179417fd8d1141	2026-06-11 03:43:10	t
11	9	73c05eb1b42f084005a9b7a471b9aa428cce646b18d298e1c227e8d9c3277eaf	2026-06-19 06:00:25	t
14	9	c2ef262e6f7885b34c7f75e17fc6162865f21db3c1bf7171e2184cf68425c043	2026-06-21 06:50:54	t
17	9	3c9c26bb31672cefacf93e1af1cde921988fdba3cb22cbc55db8209e1113fade	2026-06-21 11:10:27	f
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
12	1	fa1fc3dab6aaf4fd1918f3571a2d8548dd9e0893595abb3a865bde8e51a3b923	2026-06-19 06:02:00	t
13	1	240ebbcc09349c0f1b6460e664d7a90f7de2b8270fd179984e7b63288e5c3650	2026-06-19 06:53:17	t
21	1	b58279718cb3bcb08bd46f14d09b0264fcce72630fac2253f04d8481cc610938	2026-07-05 00:05:08	t
15	1	45eecb4b241165f2c57a9326a25061ba470a77512d7529d2571819020bfaba01	2026-06-21 06:51:54	t
18	1	32d7f4e046a5c7b67f69470f5913de318a046893e679fe3521d4ed995b515c90	2026-06-21 11:12:39	t
22	1	3965a9a8653d0a83a9ceb41b26587bc5075c1caacbc161e0665071c9df92dc20	2026-07-05 23:51:40	t
23	1	8a3eb171c1c23487aced563d1e66e08222a2e623ea67d6c5355e8167512b413d	2026-07-06 01:43:55	t
24	1	81a5c30d126025ecd5b80757d1c0024a9a103e0faefb066ba3588abaf443374e	2026-07-16 23:08:20	f
\.


--
-- TOC entry 5138 (class 0 OID 26171)
-- Dependencies: 231
-- Data for Name: request_before; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.request_before (id, customer, contract_num, contract_date, eol_fio, user_id, "position", gender, full_name, field_id, check_in, check_out, days, room_id, comment, status, admin_comment, created_at) FROM stdin;
\.


--
-- TOC entry 5140 (class 0 OID 26187)
-- Dependencies: 233
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requests (id, customer_id, contract_num, contract_date, eol_fio, user_id, "position", field_id, check_in, check_out, days, room_id, comment, status, admin_comment, created_at, resident_id) FROM stdin;
\.


--
-- TOC entry 5142 (class 0 OID 26203)
-- Dependencies: 235
-- Data for Name: residents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.residents (id, full_name, "position", gender, birthday, first_name, last_name, middle_name) FROM stdin;
\.


--
-- TOC entry 5144 (class 0 OID 26211)
-- Dependencies: 237
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name) FROM stdin;
1	admin
2	user
3	field_admin
\.


--
-- TOC entry 5146 (class 0 OID 26217)
-- Dependencies: 239
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (id, room_number, field_id, capacity, location_id, path_id, room_unique_id, status) FROM stdin;
181	101	1	2	\N	7	101a	0
1	222	3	1	1	1	222a	0
2	221	3	1	1	1	221a	0
3	220	3	1	1	1	220a	0
4	219	3	1	1	1	219a	0
5	218	3	2	1	1	218a	0
6	217	3	2	1	1	217a	0
7	216	3	2	1	1	216a	0
8	215	3	2	1	1	215a	0
9	215	3	2	1	1	215b	0
10	214	3	2	1	1	214a	0
11	214	3	2	1	1	214b	0
12	213	3	2	1	1	213a	0
13	213	3	2	1	1	213b	0
14	212	3	2	1	1	212a	0
15	212	3	2	1	1	212b	0
16	211	3	2	1	1	211a	0
17	211	3	3	1	1	211b	0
18	210	3	2	1	1	210a	0
19	210	3	2	1	1	210b	0
20	209	3	2	1	1	209a	0
21	209	3	2	1	1	209b	0
22	208	3	5	1	1	208a	0
23	206	3	3	1	1	206a	0
24	206	3	2	1	1	206b	0
25	205	3	2	1	1	205a	0
26	205	3	2	1	1	205b	0
27	204	3	2	1	1	204a	0
28	204	3	2	1	1	204b	0
29	203	3	2	1	1	203a	0
30	203	3	2	1	1	203b	0
31	202	3	2	1	1	202a	0
32	202	3	2	1	1	202b	0
33	201	3	2	1	1	201a	0
34	201	3	2	1	1	201b	0
35	108	3	3	1	1	108a	0
36	108	3	3	1	1	108b	0
37	106	3	2	1	1	106a	0
38	106	3	2	1	1	106b	0
39	105	3	2	1	1	105a	0
40	105	3	2	1	1	105b	0
42	1	3	2	2	1	1a	0
43	1	3	2	2	1	1b	0
44	2	3	2	2	1	2a	0
45	2	3	2	2	1	2b	0
47	3	3	2	2	1	3b	0
48	4	3	2	2	1	4a	0
49	4	3	2	2	1	4b	0
50	5	3	2	2	1	5a	0
51	5	3	2	2	1	5b	0
52	6	3	2	2	1	6a	0
53	6	3	2	2	1	6b	0
54	7	3	1	2	1	7a	0
55	8	3	1	2	1	8a	0
56	9	3	2	2	1	9a	0
57	9	3	2	2	1	9b	0
58	10	3	2	2	1	10a	0
59	10	3	2	2	1	10b	0
60	11	3	2	2	1	11a	0
61	11	3	2	2	1	11b	0
62	12	3	2	2	1	12a	0
63	12	3	2	2	1	12b	0
64	14	3	2	2	1	14a	0
65	14	3	2	2	1	14b	0
66	15	3	1	2	1	15a	0
67	16	3	1	2	1	16a	0
69	вагон №8 ГПН-Снабжение	3	1	3	1	вагон №8 ГПН-Снабжениеa	0
70	вагон №9 ГПН-Снабжение	3	2	3	1	вагон №9 ГПН-Снабжениеa	0
71	вагон №10	3	2	3	1	вагон №10a	0
72	Вагон №14 (ВИП) ГПНВ	3	2	3	1	Вагон №14 (ВИП) ГПНВa	0
73	Вагон №15 (ВИП) ГПНВ	3	2	3	1	Вагон №15 (ВИП) ГПНВa	0
74	вагон №16 ГПН-Снабжение	3	2	3	1	вагон №16 ГПН-Снабжениеa	0
76	вагон №2	3	5	4	1	вагон №2a	0
77	вагон №3	3	8	4	1	вагон №3a	0
182	101	1	2	\N	7	101b	0
183	102	1	2	\N	7	102a	0
184	102	1	2	\N	7	102b	0
185	103	1	2	\N	7	103a	0
186	104	1	2	\N	7	104a	0
187	105	1	1	\N	7	105a	0
188	106	1	2	\N	7	106a	0
189	107	1	2	\N	7	107a	0
190	108	1	2	\N	7	108a	0
191	108	1	2	\N	7	108b	0
192	109	1	2	\N	7	109a	0
193	109	1	2	\N	7	109b	0
194	110	1	2	\N	7	110a	0
195	110	1	2	\N	7	110b	0
196	111	1	2	\N	7	111a	0
197	112	1	2	\N	7	112a	0
198	112	1	2	\N	7	112b	0
199	113	1	2	\N	7	113a	0
200	113	1	2	\N	7	113b	0
201	114	1	2	\N	7	114a	0
202	115	1	2	\N	\N	115a	0
203	115	1	2	\N	\N	115b	0
204	116	1	2	\N	\N	116a	0
205	116	1	2	\N	\N	116b	0
206	117	1	2	\N	\N	117a	0
207	118	1	2	\N	\N	118a	0
208	118	1	2	\N	\N	118b	0
209	119	1	2	\N	\N	119a	0
210	119	1	2	\N	\N	119b	0
211	120	1	2	\N	\N	120a	0
212	120	1	2	\N	\N	120b	0
213	121	1	2	\N	\N	121a	0
214	122	1	2	\N	\N	122a	0
215	123	1	2	\N	\N	123a	0
216	124	1	2	\N	\N	124a	0
217	125	1	2	\N	\N	125a	0
218	125	1	2	\N	\N	125b	0
219	126	1	2	\N	\N	126a	0
220	126	1	2	\N	\N	126b	0
221	127	1	1	\N	\N	127a	0
222	201	1	2	\N	9	201a	0
223	201	1	2	\N	9	201b	0
224	202	1	2	\N	9	202a	0
225	202	1	2	\N	9	202b	0
226	203 (гостевой)	1	1	\N	9	203 (гостевой)a	0
227	204	1	1	\N	9	204a	0
228	205	1	2	\N	9	205a	0
229	205	1	2	\N	9	205b	0
230	206	1	2	\N	9	206a	0
231	206	1	2	\N	9	206b	0
232	207	1	2	\N	9	207a	0
233	207	1	2	\N	9	207b	0
234	208	1	2	\N	9	208a	0
235	208	1	2	\N	9	208b	0
236	209	1	2	\N	9	209a	0
237	210	1	2	\N	9	210a	0
238	210	1	2	\N	9	210b	0
239	211	1	2	\N	9	211a	0
240	211	1	2	\N	9	211b	0
241	212	1	2	\N	9	212a	0
242	213	1	2	\N	10	213a	0
243	213	1	2	\N	10	213b	0
244	214	1	2	\N	10	214a	0
245	214	1	2	\N	10	214b	0
246	215	1	2	\N	10	215a	0
247	215	1	2	\N	10	215b	0
248	216 (гостевой)	1	2	\N	10	216 (гостевой)a	0
249	217	1	1	\N	10	217a	0
250	218	1	2	\N	10	218a	0
251	218	1	2	\N	10	218b	0
252	219	1	1	\N	10	219a	0
253	220 (гостевой)	1	2	\N	10	220 (гостевой)a	0
254	221	1	2	\N	10	221a	0
255	221	1	2	\N	10	221b	0
256	222	1	2	\N	10	222a	0
257	222	1	2	\N	10	222b	0
258	223	1	2	\N	10	223a	0
259	223	1	2	\N	10	223b	0
260	224	1	2	\N	10	224a	0
262	Кедр"К.04.2.1.\n(12а)	1	2	\N	11	кедр"к.04.2.1.\n(12а)a	0
263	Кедр"К.04.2.1.\n(12а)	1	2	\N	11	кедр"к.04.2.1.\n(12а)b	0
264	Ермак (46)	1	2	\N	11	ермак (46)a	0
265	Ермак (46)	1	2	\N	11	ермак (46)b	0
266	Ермак (53)	1	2	\N	11	ермак (53)a	0
267	Ермак (53)	1	2	\N	11	ермак (53)b	0
268	Ермак (55)	1	2	\N	11	ермак (55)a	0
269	Ермак (55)	1	1	\N	11	ермак (55)b	0
270	Ермак (48)	1	2	\N	11	ермак (48)a	0
271	Ермак (48)	1	1	\N	11	ермак (48)b	0
272	К-10 (21)	1	2	\N	11	к-10 (21)a	0
273	Медведь-02 (41)	1	2	\N	11	медведь-02 (41)a	0
274	Ермак (б/н)	1	2	\N	11	ермак (б/н)a	0
275	Ермак (б/н)	1	2	\N	11	ермак (б/н)b	0
276	К-4К (не благ. 39)	1	2	\N	11	к-4к (не благ. 39)a	0
277	К-4 (12)	1	4	\N	11	к-4 (12)a	0
278	К-4 (12)	1	4	\N	11	к-4 (12)b	0
279	к-4 (38)	1	4	\N	11	к-4 (38)a	0
280	к-4 (38)	1	4	\N	11	к-4 (38)b	0
281	к-4 (38)	1	4	\N	11	к-4 (38)c	0
282	К-4К                         (не благ. б/н)	1	4	\N	11	к-4к                         (не благ. б/н)a	0
283	К-4К                         (не благ. б/н)	1	4	\N	11	к-4к                         (не благ. б/н)b	0
284	Кедр-10	1	4	\N	11	кедр-10a	0
285	Ермак (23)	1	2	\N	11	ермак (23)a	0
286	новый (б/№)	1	2	\N	11	новый (б/№)a	0
287	новый (б/№)	1	2	\N	11	новый (б/№)b	0
\.


--
-- TOC entry 5148 (class 0 OID 26225)
-- Dependencies: 241
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
-- Dependencies: 220
-- Name: contract_counters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contract_counters_id_seq', 1, true);


--
-- TOC entry 5170 (class 0 OID 0)
-- Dependencies: 222
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_id_seq', 82, true);


--
-- TOC entry 5171 (class 0 OID 0)
-- Dependencies: 224
-- Name: fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fields_id_seq', 16, true);


--
-- TOC entry 5172 (class 0 OID 0)
-- Dependencies: 226
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_id_seq', 8, true);


--
-- TOC entry 5173 (class 0 OID 0)
-- Dependencies: 228
-- Name: paths_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.paths_id_seq', 11, true);


--
-- TOC entry 5174 (class 0 OID 0)
-- Dependencies: 230
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.refresh_tokens_id_seq', 24, true);


--
-- TOC entry 5175 (class 0 OID 0)
-- Dependencies: 232
-- Name: request_before_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.request_before_id_seq', 1, false);


--
-- TOC entry 5176 (class 0 OID 0)
-- Dependencies: 234
-- Name: requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requests_id_seq', 1, false);


--
-- TOC entry 5177 (class 0 OID 0)
-- Dependencies: 236
-- Name: residents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.residents_id_seq', 5, true);


--
-- TOC entry 5178 (class 0 OID 0)
-- Dependencies: 238
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, true);


--
-- TOC entry 5179 (class 0 OID 0)
-- Dependencies: 240
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_id_seq', 287, true);


--
-- TOC entry 5180 (class 0 OID 0)
-- Dependencies: 242
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 9, true);


--
-- TOC entry 4931 (class 2606 OID 26245)
-- Name: contract_counters contract_counters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contract_counters
    ADD CONSTRAINT contract_counters_pkey PRIMARY KEY (id);


--
-- TOC entry 4933 (class 2606 OID 26247)
-- Name: contract_counters contract_counters_prefix_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contract_counters
    ADD CONSTRAINT contract_counters_prefix_key UNIQUE (prefix);


--
-- TOC entry 4935 (class 2606 OID 26249)
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- TOC entry 4937 (class 2606 OID 26251)
-- Name: fields fields_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_pkey PRIMARY KEY (id);


--
-- TOC entry 4939 (class 2606 OID 26253)
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- TOC entry 4941 (class 2606 OID 26255)
-- Name: paths paths_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paths
    ADD CONSTRAINT paths_pkey PRIMARY KEY (id);


--
-- TOC entry 4945 (class 2606 OID 26257)
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 4947 (class 2606 OID 26259)
-- Name: refresh_tokens refresh_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_hash_key UNIQUE (token_hash);


--
-- TOC entry 4949 (class 2606 OID 26261)
-- Name: request_before request_before_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_pkey PRIMARY KEY (id);


--
-- TOC entry 4951 (class 2606 OID 26263)
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


--
-- TOC entry 4953 (class 2606 OID 26265)
-- Name: residents residents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.residents
    ADD CONSTRAINT residents_pkey PRIMARY KEY (id);


--
-- TOC entry 4955 (class 2606 OID 26267)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 4957 (class 2606 OID 26269)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 4960 (class 2606 OID 26271)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- TOC entry 4962 (class 2606 OID 26273)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4964 (class 2606 OID 26275)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4942 (class 1259 OID 26276)
-- Name: idx_refresh_tokens_token_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_refresh_tokens_token_hash ON public.refresh_tokens USING btree (token_hash);


--
-- TOC entry 4943 (class 1259 OID 26277)
-- Name: idx_refresh_tokens_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_refresh_tokens_user_id ON public.refresh_tokens USING btree (user_id);


--
-- TOC entry 4958 (class 1259 OID 26278)
-- Name: ix_rooms_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_rooms_id ON public.rooms USING btree (id);


--
-- TOC entry 4974 (class 2606 OID 26279)
-- Name: rooms fk_field; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_field FOREIGN KEY (field_id) REFERENCES public.fields(id);


--
-- TOC entry 4975 (class 2606 OID 26284)
-- Name: rooms fk_rooms_location; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_rooms_location FOREIGN KEY (location_id) REFERENCES public.locations(id) ON DELETE SET NULL;


--
-- TOC entry 4976 (class 2606 OID 26289)
-- Name: rooms fk_rooms_path; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_rooms_path FOREIGN KEY (path_id) REFERENCES public.paths(id) ON DELETE SET NULL;


--
-- TOC entry 4965 (class 2606 OID 26294)
-- Name: refresh_tokens refresh_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4966 (class 2606 OID 26299)
-- Name: request_before request_before_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE CASCADE;


--
-- TOC entry 4967 (class 2606 OID 26304)
-- Name: request_before request_before_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(id) ON DELETE SET NULL;


--
-- TOC entry 4968 (class 2606 OID 26309)
-- Name: request_before request_before_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request_before
    ADD CONSTRAINT request_before_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4969 (class 2606 OID 26314)
-- Name: requests requests_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id) ON DELETE CASCADE;


--
-- TOC entry 4970 (class 2606 OID 26319)
-- Name: requests requests_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE CASCADE;


--
-- TOC entry 4971 (class 2606 OID 26324)
-- Name: requests requests_resident_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_resident_id_fkey FOREIGN KEY (resident_id) REFERENCES public.residents(id) ON DELETE SET NULL;


--
-- TOC entry 4972 (class 2606 OID 26329)
-- Name: requests requests_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(id) ON DELETE SET NULL;


--
-- TOC entry 4973 (class 2606 OID 26334)
-- Name: requests requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4977 (class 2606 OID 26339)
-- Name: users users_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id);


--
-- TOC entry 4978 (class 2606 OID 26344)
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


-- Completed on 2026-07-10 02:58:57

--
-- PostgreSQL database dump complete
--

\unrestrict qYemS5imix88Tw02LuIKMExVfsrT1BK9w5NgA5NF2UZaym5WMhegK1Qf6NLx87q

