from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            data = request.form.to_dict()

        return data

    # ########  Treinen  #########
    @staticmethod
    def read_treinen():
        sql = "SELECT * FROM trein.treinen;"
        return Database.get_rows(sql)

    @staticmethod
    def read_trein(treinID):
        sql = """
        SELECT *
        FROM treinen
        WHERE idtrein = %s
        """
        params = [treinID]

        return Database.get_one_row(sql, params)

    @staticmethod
    def read_treinen_met_bestemming(bestemmingID):
        sql = """
        SELECT *
        FROM treinen as t
            INNER JOIN bestemmingen as b on t.bestemmingID = b.idbestemming
        WHERE b.idbestemming = %s
        """
        params = [bestemmingID]

        return Database.get_rows(sql, params)

    @staticmethod
    def create_trein(vertrek, bestemmingID, spoor, vertraging, afgeschaft):
        sql = """
        INSERT INTO treinen
        VALUES (null, %s, %s, %s, %s, %s)
        """
        params = [vertrek, bestemmingID, spoor, vertraging, afgeschaft]

        return Database.execute_sql(sql, params)

    @staticmethod
    def update_trein(treinID, vertrek, bestemmingID, spoor, vertraging, afgeschaft):
        sql = """
        UPDATE treinen
        SET
            vertrek = %s,
            bestemmingID = %s,
            spoor = %s,
            vertraging = %s,
            afgeschaft = %s

        WHERE idtrein = %s
        """
        params = [vertrek, bestemmingID, spoor, vertraging, afgeschaft, treinID]

        return Database.execute_sql(sql, params)

    @staticmethod
    def update_trein_vertraging(treinID, vertraging):
        sql = """
        UPDATE treinen
        SET
            vertraging = %s

        WHERE idtrein = %s
        """
        params = [vertraging, treinID]

        return Database.execute_sql(sql, params)

    @staticmethod
    def delete_trein(treinID):
        sql = """
        DELETE FROM treinen
        WHERE idtrein = %s
        """
        params = [treinID]

        return Database.execute_sql(sql, params)

    # ########  Bestemmingen  #########
    @staticmethod
    def read_bestemmingen():
        sql = "SELECT * FROM trein.bestemmingen;"
        return Database.get_rows(sql)
