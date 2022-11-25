#Consultas SQL
#1 Listar todos os tweets de um usuario

select id, content
from tweet
where owner in (
	select id
    from user
);

#2 Listar todos os tweets de pessoas que um usuário segue

select id, content
from tweet
where owner in(
	select id
    from user
    where id in (
		select user_follows_id
        from user_follows        
    )
);
#Refazer

#3 Listar todos usuários que um usuário segue

select nickname
from user
where id in (
	select user_follows_id
    from user_follows
    where user_followed_id = id
);

#4 Listar por quem esse usário é seguido

select nickname
from user
where id in (
	select user_follows_id
    from user_follows
    where user_followed_id = id
);

#5 listar todos os tweets que tem "COPA DO MUNDO" no texto

select id
from tweet
where content like "copa do mundo";

#6 Listar todas as repostas de um determinado tweet (utilize o parent)

select retweet
from tweet as t
where t.id in (
	select parent
    from tweet
    where id = t.id 
);


