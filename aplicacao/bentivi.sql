create table bentivi;
use bentivi;
create table tweet(
	id int primary key not null,
    content Text not null,        
    retweet tinyint(1),
    owner int not null,
    parent int 
);

alter table tweet add constraint retweetForeign foreign key (owner)  references user(id);
alter table tweet add constraint retweetTweet foreign key (parent)  references tweet(id);

create table user_likes(
	user_id int not null,
    tweet_id int not null
);
alter table user_likes add constraint user_tweet foreign key (user_id) references user(id);
alter table user_likes add constraint user_tweet_id foreign key (tweet_id) references tweet(id);

create table user(
	id int primary key not null,
    nickname varchar(64) not null,
    email varchar(64) not null,
    password varchar(64) not null
);

create table user_follows(
	user_follows_id int not null,
    user_followed_id int not null    
);

alter table user_follows add constraint user_follows_id foreign key (user_follows_id) references user(id);
alter table user_follows add constraint user_followed_id foreign key (user_followed_id) references user(id);
