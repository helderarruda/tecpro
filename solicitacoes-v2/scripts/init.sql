create database solicitacoes;

\c solicitacoes

create table pedidos (
	id serial not null,
	data timestamp not null default CURRENT_TIMESTAMP,
	nome varchar( 100 ) not null,
	assunto varchar( 100 ) not null,
	mensagem varchar( 250 ) not null
);
