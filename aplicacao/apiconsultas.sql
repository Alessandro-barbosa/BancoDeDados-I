#API REST

#Desenvolver Rotas para API

#1 Listar todos os tweets de um usuário

select id
from tweet
where owner in (
	select id
    from user    
    where id = 2 #Passagem
);

#2 Listar todos os tweets de pessoas que um usuário segue

select id 
from tweet 
where owner in (
	select id
    from user as u
    where id in (
		select user_follows_id
        from user_follows
        where user_followed = u.id
    )
);

#3 Listar todos usários que um usário segue

select nickname
from user as u
where id in (
	select user_followed_id
    from user_follows
    where user_follows_id = u.id
);

#4 Listar por quem esse usuário é seguido

select nickname
from user as u 
where id in (
	select user_follows_id
    from user_follows
    where user_followed_id = u.id
);

#5 Listar todas as repostas de um determinado tweet

select id
from tweet as t
where id in (
	select parent
    from tweet
);

#6 Buscar no texto do tweet
#Valor a ser procurado dentro do tweet
#Fazer

#7 Registar um usuário

insert into user values
