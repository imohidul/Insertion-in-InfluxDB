from influxdb import InfluxDBClient
from datetime import datetime


def insert_data_influx_db(self):
    query = []
    database_exist = False
    database = 'smsalert'
    host = 'localhost'
    port = 8086

    # initialize connection
    client = InfluxDBClient(host=host, port=port)
    databases = client.get_list_database()

    # checking existing of database
    for db in databases:
        if db['name'] == database:
            database_exist = True

    # create database if not exist
    if not database_exist:
        client.create_database(database)

    # inserting data
    for container in self.CONTAINERS:
        if container['Status'] == 'Active':
            value = 1
        else:
            value = 0

        query.append('monitoring,server_name=' + container['Name'] + ' value=' + str(value) + " " +
                     str(int((datetime.today() - datetime(1970, 1, 1)).total_seconds())))

    client.write(query, {'db': database}, 204, 'line')

