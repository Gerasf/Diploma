--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

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
-- Name: parking_areas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parking_areas (
    area_id integer NOT NULL,
    top json,
    "right" json,
    bottom json,
    "left" json
);


ALTER TABLE public.parking_areas OWNER TO postgres;

--
-- Name: parking_areas_area_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parking_areas_area_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parking_areas_area_id_seq OWNER TO postgres;

--
-- Name: parking_areas_area_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parking_areas_area_id_seq OWNED BY public.parking_areas.area_id;


--
-- Name: parking_positions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.parking_positions (
    id integer NOT NULL,
    area_id integer,
    left_up json,
    right_up json,
    right_down json,
    left_down json
);


ALTER TABLE public.parking_positions OWNER TO postgres;

--
-- Name: parking_positions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parking_positions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parking_positions_id_seq OWNER TO postgres;

--
-- Name: parking_positions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parking_positions_id_seq OWNED BY public.parking_positions.id;


--
-- Name: parking_areas area_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parking_areas ALTER COLUMN area_id SET DEFAULT nextval('public.parking_areas_area_id_seq'::regclass);


--
-- Name: parking_positions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parking_positions ALTER COLUMN id SET DEFAULT nextval('public.parking_positions_id_seq'::regclass);


--
-- Data for Name: parking_areas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parking_areas (area_id, top, "right", bottom, "left") FROM stdin;
1	[7, 519]	[1267, 429]	[1278, 527]	[7, 650]
2	[11, 421]	[1275, 325]	[1278, 390]	[8, 485]
3	[14, 294]	[6, 340]	[1276, 271]	[1227, 239]
4	[13, 356]	[7, 399]	[1274, 316]	[1245, 294]
\.


--
-- Data for Name: parking_positions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parking_positions (id, area_id, left_up, right_up, right_down, left_down) FROM stdin;
1	1	1006	457	166	66
2	1	1007	471	191	62
3	1	167	510	51	91
4	1	167	520	51	80
5	1	368	394	60	48
6	1	369	396	60	46
7	1	166	516	52	85
8	1	167	513	52	88
9	1	917	459	103	76
10	1	917	459	96	75
11	1	491	496	113	91
12	1	497	496	106	92
13	1	921	463	83	72
14	1	921	456	95	84
15	1	918	456	102	88
16	1	916	457	104	89
17	1	72	431	146	36
18	1	73	431	145	38
19	1	51	441	151	29
20	1	37	441	157	29
21	1	1117	457	94	76
22	1	323	402	58	55
23	1	325	401	57	53
24	1	325	401	58	53
25	1	813	463	76	85
26	1	930	467	99	76
27	1	938	453	111	77
28	1	10	551	74	90
29	1	10	551	66	90
30	1	1121	443	93	71
31	1	1120	446	93	61
32	1	527	504	97	83
33	1	514	505	78	88
34	1	618	476	83	104
35	1	608	478	85	105
36	1	910	460	129	78
37	1	909	462	131	79
\.


--
-- Name: parking_areas_area_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parking_areas_area_id_seq', 4, true);


--
-- Name: parking_positions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parking_positions_id_seq', 37, true);


--
-- Name: parking_areas parking_areas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parking_areas
    ADD CONSTRAINT parking_areas_pkey PRIMARY KEY (area_id);


--
-- Name: parking_positions parking_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parking_positions
    ADD CONSTRAINT parking_positions_pkey PRIMARY KEY (id);


--
-- Name: parking_positions parking_positions_area_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parking_positions
    ADD CONSTRAINT parking_positions_area_id_fkey FOREIGN KEY (area_id) REFERENCES public.parking_areas(area_id);


--
-- PostgreSQL database dump complete
--

