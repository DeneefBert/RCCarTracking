from .Database import Database
from datetime import datetime


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def write_device(time, data, id, comment="NULL"):
        sql = "INSERT INTO history(date, value, comments, deviceid, actionid) VALUES(%s, %s, %s, %s, %s)"
        params = [time, data, comment, id, 1]
        return Database.execute_sql(sql, params)

    @staticmethod
    def write_light(colour, comment="NULL"):
        sql = "INSERT INTO history(value, comments, deviceid, actionid) VALUES(%s, %s, 4, 4)"
        params = [colour, comment]
        return Database.execute_sql(sql, params)

    @staticmethod
    def write_speaker(toneid, comment="NULL"):
        sql = "INSERT INTO history(value, comments, deviceid, actionid) VALUES(%s, %s, 5, 4)"
        params = [toneid, comment]
        return Database.execute_sql(sql, params)

    @staticmethod
    def request_data(deviceid, amount, enddate, startdate):
        if enddate == "":
            enddate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if startdate == "":
            sql = "select date, value from history where deviceid = %s and date < %s order by date desc limit %s" 
            params = [deviceid, enddate, amount]
            return Database.get_rows(sql, params)
        else:
            sql = "select date, value from history where deviceid = %s and date between %s and %s order by date desc limit %s"
            params = [deviceid, startdate, enddate, amount]
            return Database.get_rows(sql, params)

    @staticmethod
    def light_status():
        sql = "select value from history where deviceid = 4 order by date desc limit 1"
        return Database.get_one_row(sql)

    @staticmethod
    def light_default(intensity, method, comment="NULL"):
        sql = "insert into history(value, comments, deviceid, actionid) VALUES(%s, %s, 4, %s)"
        params = [intensity, comment, method]
        return Database.execute_sql(sql, params)

    @staticmethod
    def speaker_default(alarm, comment="NULL"):
        sql = "insert into history(value, comments, deviceid, actionid) VALUES(%s, %s, 5, 5)"
        params = [alarm, comment]
        return Database.execute_sql(sql, params)