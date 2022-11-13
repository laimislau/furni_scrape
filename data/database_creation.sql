create table Shops (
	shop_id int NOT NULL auto_increment,
    shop_name varchar (255),    
    primary key (shop_id)
);

create table Furnitures (
	furniture_id int NOT NULL auto_increment,
    shop_id int NOT NULL,
    furniture_name varchar (255),
    furniture_description text,
    furniture_price int,
    furniture_image_link text,
    furniture_key_features text,
    furniture_size text,
    
    primary key (furniture_id),
    foreign key (shop_id) references Shops(shop_id)
);

create table Search (
	search_id int NOT NULL auto_increment,
    furniture_id int NOT NULL,
    log_id int NOT NULL,
    search_results_count int,
    search_keyword varchar (255),
    
    primary key (search_id),
    foreign key (furniture_id) references Furnitures(furniture_id)
);

create table Logs (
	log_id int NOT NULL auto_increment,
    shop_id int NOT NULL,
    furniture_id int NOT NULL,
    search_id int NOT NULL,
    log_date date,
    log_data text,
    
    primary key (log_id),
    foreign key (shop_id) references Shops(shop_id),
    foreign key (furniture_id) references Furnitures(furniture_id),
    foreign key (search_id) references Search(search_id)
    
);

alter table Search add foreign key (log_id) references Logs(log_id)