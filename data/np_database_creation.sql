use nordpool;
create table Months (
	mon_id int NOT NULL,
    mon_name varchar(255),
    
    primary key (mon_id)
);

insert into Months(mon_id, mon_name)
values
(1,"JANUARY"),
(2, "FEBRUARY"),
(3, "MARCH"),
(4, "APRIL"),
(5, "MAY"),
(6, "JUNE"),
(7, "JULY"),
(8, "AUGUST"),
(9, "SEPTEMBER"),
(10, "OCTOBER"),
(11, "NOVEMBER"),
(12, "DECEMBER");

create table Years (
	year_id int NOT NULL auto_increment,
    year int,
    
    primary key (year_id)
);

insert into Years(year) values
(2022),
(2023),
(2024),
(2025),
(2026),
(2027),
(2028),
(2029),
(2030);

create table HourlyPricesLT (
	day_id int NOT NULL auto_increment,
    mon_id int NOT NULL,
    year_id int NOT NULL,
    price_date date,
    time_00_01 float,
    time_01_02 float,
    time_02_03 float,
    time_03_04 float,
    time_04_05 float,
    time_05_06 float,
    time_06_07 float,
    time_07_08 float,
    time_08_09 float,
    time_09_10 float,
    time_10_11 float,
    time_11_12 float,
    time_12_13 float,
    time_13_14 float,
    time_14_15 float,
    time_15_16 float,
    time_16_17 float,
    time_17_18 float,
    time_18_19 float,
    time_20_21 float,
    time_21_22 float,
    time_22_23 float,
    time_23_24 float,    
    
    primary key (day_id),
    foreign key (mon_id) references Months(mon_id),
    foreign key (year_id) references Years(year_id)
    );







