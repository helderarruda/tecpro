PGDMP     7    +                x            solicitacoes    9.6.18    9.6.18     P           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            Q           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            R           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            S           1262    16384    solicitacoes    DATABASE     |   CREATE DATABASE solicitacoes WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';
    DROP DATABASE solicitacoes;
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            T           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12393    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            U           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16387    pedidos    TABLE     �   CREATE TABLE public.pedidos (
    id integer NOT NULL,
    data timestamp without time zone DEFAULT now() NOT NULL,
    nome character varying(100) NOT NULL,
    assunto character varying(100) NOT NULL,
    mensagem character varying(250) NOT NULL
);
    DROP TABLE public.pedidos;
       public         postgres    false    3            �            1259    16385    pedidos_id_seq    SEQUENCE     w   CREATE SEQUENCE public.pedidos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.pedidos_id_seq;
       public       postgres    false    186    3            V           0    0    pedidos_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.pedidos_id_seq OWNED BY public.pedidos.id;
            public       postgres    false    185            �           2604    16390 
   pedidos id    DEFAULT     h   ALTER TABLE ONLY public.pedidos ALTER COLUMN id SET DEFAULT nextval('public.pedidos_id_seq'::regclass);
 9   ALTER TABLE public.pedidos ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    185    186    186            M          0    16387    pedidos 
   TABLE DATA               D   COPY public.pedidos (id, data, nome, assunto, mensagem) FROM stdin;
    public       postgres    false    186            W           0    0    pedidos_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.pedidos_id_seq', 1, true);
            public       postgres    false    185            M   0   x�3�4202�50�5�T0��2��2��33��06�L�L�L����� ��c     