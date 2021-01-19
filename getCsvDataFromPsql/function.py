import json
import psycopg2
import traceback
from Common import LambdaBase

class GetCsvDataFromPsql(LambdaBase):
    def handle(self, event, context):
        db_conn = psycopg2.connect("dbname={} user={} host={} password={}".format(event['db_name'], event['db_user_ro'], event['db_host'], event['db_pass']))
        db_cursor = db_conn.cursor()
        db_cursor.execute(event['sql_query'])
        result = db_cursor.fetchall()
        db_conn.close()
        csv = ""
        for record in result:
            for field in record:
                csv += "\"" + str(field) + "\","
            csv = csv[:-1] + "\n"
        return {
            "statusCode": 200,
            "csv": csv
        }

index = GetCsvDataFromPsql.get_handler()