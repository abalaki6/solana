import pymysql
import numpy as np
import sklearn
import sklearn.cluster
from sklearn.cluster import KMeans


def KMeans_clustering(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, algorithm='elkan').fit(data)
    labels, centers =  kmeans.labels_, kmeans.cluster_centers_

    counts = np.unique(labels, return_counts=True)[1]
    # add some additional metric collections

    return np.hstack([centers, counts.reshape(-1, 1)])

def run_clustering(data, n_clusters):
    return KMeans_clustering(data, n_clusters)


if __name__ == "__main__":
    connection = pymysql.connect(
        host='localhost', user="UIUC", password="UIUC_492")


    with connection.cursor() as cursor:
        # use SOLANA
        sql_req = "use SOLANA;"
        cursor.execute(sql_req)
        responce = cursor.fetchall()
        # collect data from table
        sql_req =  "select latitude, longtitude from NODES_TEST;"
        cursor.execute(sql_req)
        responce = cursor.fetchall()
        # define clusters sizes
        data = np.array(responce)
        # n_clusters = [10, 20, 30, 50, 100]
        n_clusters = [15, 20, 50, 100]

        # create scheme
        sql_req = "drop table if exists NODES_TEST_CLUSTER;"
        cursor.execute(sql_req)
        responce = cursor.fetchall()
        sql_req = "create table NODES_TEST_CLUSTER like NODES_TEST;"
        cursor.execute(sql_req)
        responce = cursor.fetchall()

        sql_req = "insert into NODES_TEST_CLUSTER (longtitude, latitude, node_size, map_depth) VALUES\n"

        steps = []
        for i,n in enumerate(n_clusters):
            clusters = run_clustering(data, n)
            steps.append("".join([f"({a[0]:.3f}, {a[1]:.3f}, {a[2]}, {i}),\n" for a in clusters]))
            if i == len(n_clusters) -1:
                istep = list(steps[-1])
                istep[-2:] = [';', '\n']
                steps[-1] = "".join(istep)
        sql_req = "".join([sql_req, *steps])
        cursor.execute(sql_req)
        connection.commit()

    connection.close()