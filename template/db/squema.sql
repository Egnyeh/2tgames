create table users (
       id int primary key auto_increment,
       name varchar(20) not null,
       username varchar(20) not null,
       password varchar(512) not null
) engine=innodb;

create table films (
       id int primary key auto_increment,
       title varchar(256) not null,
       synopsis text
) engine=innodb;

create table user_starred_films (
       id int primary key auto_increment,
       user int not null,
       film int not null,
       stars int not null,
       comment text,
       foreign key (user) references users(id),
       foreign key (film) references films(id),
       unique key (user, film)
) engine=innodb;
