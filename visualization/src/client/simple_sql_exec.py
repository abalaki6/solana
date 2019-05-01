import pymysql
import pprint

if __name__ == "__main__":
    connection = pymysql.connect(
        host='localhost', user="UIUC", password="UIUC_492")

    with connection.cursor() as cursor:
        sql_req = "show databases;"
        cursor.execute(sql_req)
        pprint.pprint(cursor.fetchall())

    connection.close()