create database picpay;
use picpay;

create table usuario(
	id int primary key not null,
    email varchar(100) unique not null,    
    senha varchar(100) not null,
    cpf int not null,
    valor float 
);

create table transacao(
	id int primary key,
    id_usuario_envio int not null,
    id_usuario_recebe int not null,
    valor float,
    data date
);

alter table transacao add foreign key (id_usuario_envio) references usuario(id);
alter table transacao add foreign key (id_usuario_recebe) references usuario(id);

create table item(
	id int primary key not null,
    nome varchar(100) not null,
    quantidade int 
);

create table compra(
	id_trans int not null,
    id_item int not null,
    quantidade int
);
alter table compra add primary key(id_trans, id_item);
alter table compra add foreign key (id_trans) references item(id);
alter table compra add foreign key (id_item) references transacao(id);


