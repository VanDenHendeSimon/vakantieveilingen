from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            data = request.form.to_dict()

        return data

    @staticmethod
    def get_auctions():
        sql = "SELECT * FROM auction;"
        return Database.get_rows(sql)

    @staticmethod
    def get_auction(url):
        sql = """
        SELECT *
        FROM auction
        WHERE id = %s
        """
        params = [url]

        return Database.get_one_row(sql, params)

    @staticmethod
    def create_category(name, description, blacklisted):
        sql = """
        INSERT INTO category
        VALUES (%s, %s, %s)
        """
        params = [name, description, blacklisted]

        return Database.execute_sql(sql, params)
