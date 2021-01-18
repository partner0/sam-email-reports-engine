import json
import psycopg2
import traceback

def arr_to_csv(arr):
    csv = ""
    for record in arr:
        for field in record:
            csv += "\"" + field + "\","
        csv = csv[:-1] + "\n"
    return csv

def index(event, context):
    try:
        for variable in event:
            globals()[variable] = event[variable]
        db_conn = psycopg2.connect("dbname={} user={} host={} password={}".format(db_name, db_user_ro, db_host, db_pass))
        db_cursor = db_conn.cursor()
        db_cursor.execute(sql_query)
        result = db_cursor.fetchall()
        db_conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "message": traceback.format_exc(),
        }
    return {
        "statusCode": 200,
        "csv": arr_to_csv(result)
    }