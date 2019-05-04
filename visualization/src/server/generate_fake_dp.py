import os
import numpy as np
import json
from pandas.io.json import json_normalize


def main():
    f = open("database_fake.sql", "w")

    f.write("""
drop database if exists SOLANA;
create database SOLANA;
use SOLANA;
create table NODES_TEST(
ip_addr INT (4) unsigned not null default 0,
longitude float(32) not null default -1,
latitude float(32) not null default -1,
city varchar(64) not null default 'N/A',
region varchar(64) not null default 'N/A',
country varchar(64) not null default 'N/A',
ping_time INT(16) unsigned not null default 0,
slot_height INT(16) unsigned not null default 0,
transaction_count INT(64) unsigned not null default 0,
stake_weight FLOAT(32) not null default 0,
public_key varchar(256) not null default '',
socket_status INT(4) unsigned not null default 255,
map_depth INT(4) unsigned not null default 0,
node_size INT(16) unsigned not null default 1);
INSERT INTO NODES_TEST
(longitude, latitude, map_depth)
VALUES
""")

    # temporal location of test set
    with open("../client/public/d.json", 'r') as source:
        # select only feature attributes
        data = json.load(source)['levels'][0]['features']

    df = json_normalize(data)
    # normalize to 2d numpy array of coordinates
    locs = np.array([np.array([*df.loc[:, ['geometry.coordinates']].values[i]]) for i in range(len(df))]).reshape(-1, 2)

    # number of points to put
    N = 1000
    # select random locations
    # add reproductivity
    np.random.seed(17121997)
    locs = locs[np.random.randint(locs.shape[0], size=N), :]
    # maximum offset in 1d from root point
    MAXOFF = 10

    for i,loc in enumerate(locs):
        long, lat = (np.random.random(2) - 0.5) * (2 * MAXOFF) + loc
        level = 1

        f.write(f"({long:.3f}, {lat:.3f}, {level})")
        if i != N - 1:
            f.write(",\n")
        else:
            f.write(";\n")


    f.close()

if __name__ == "__main__":
    main()
