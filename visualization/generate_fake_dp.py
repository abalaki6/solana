import os
import numpy as np

def main():
    f = open("database_fake.sql", "w")

    f.write("""
drop database if exists SOLANA;
create database SOLANA;
use SOLANA;
create table NODES_TEST(
ip_addr INT (4) unsigned not null default 0,
longtitude float(32) not null default -1,
latitude float(32) not null default -1,
city varchar(64) not null default 'N/A',
region varchar(64) not null default 'N/A',
country varchar(64) not null default 'N/A',
ping_time INT(16) unsigned not null default 0,
slot_height INT(16) unsigned not null default 0,
transaction_count INT(64) unsigned not null default 0,
stake_weight FLOAT(32) not null default 0,
public_key varchar(256) not null default '',
socket_status INT(4) unsigned not null default 255);\n""")

    for i in range(1000):
        long, lat = ((np.random.random(2) - 0.5) * 90)

        f.write( f"INSERT INTO NODES_TEST (longtitude, latitude) VALUES ({long:.3}, {lat:.3}); \n" )


    f.close()

if __name__ == "__main__":
    main()
