
CREATE TABLE facttrips
(
    tripid integer NOT NULL primary key,
    dateid integer NOT NULL,
    stationid integer NOT NULL,
    truckid integer NOT NULL,
    wastecollected float NOT NULL
);

CREATE TABLE dimdate
(
    dateid integer NOT NULL primary key,
    fulldate date NOT NULL,
    year integer NOT NULL,
    quarter integer NOT NULL,
    quarterName varchar(40) NOT NULL,
    month integer NOT NULL,
    monthname varchar(40) NOT NULL,
    day integer NOT NULL,
    weekday integer NOT NULL,
    weekdayName varchar(40) NOT NULL
);

CREATE TABLE dimstation
(
    stationid integer NOT NULL primary key,
    city varchar(40) NOT NULL
);

CREATE TABLE dimtruck
(
    truckid integer NOT NULL primary key,
    trucktype varchar(40) NOT NULL
);


ALTER TABLE facttrips ADD FOREIGN KEY (dateid) REFERENCES dimdate (dateid);

ALTER TABLE facttrips ADD FOREIGN KEY (stationid) REFERENCES dimstation (stationid);

ALTER TABLE facttrips ADD FOREIGN KEY (truckid) REFERENCES dimtruck (truckid);

