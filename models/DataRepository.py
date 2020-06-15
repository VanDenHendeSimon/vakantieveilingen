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
    def get_wishlist():
        sql = "SELECT * FROM wishlist WHERE Bought = 0;"
        return Database.get_rows(sql)

    @staticmethod
    def create_category(name, description, blacklisted):
        sql = """
        INSERT INTO category
        VALUES (%s, %s, %s)
        """
        params = [name, description, blacklisted]

        return Database.execute_sql(sql, params)

    @staticmethod
    def create_auction(url, extra_costs, retail_price, category, supplier_link):
        sql = """
        INSERT INTO auction
        VALUES (%s, %s, %s, %s, %s)
        """

        params = [url, extra_costs, retail_price, category, supplier_link]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_auction(url, extra_costs, retail_price, category, supplier_link):
        sql = """
        UPDATE auction
        SET 
            ExtraCost = %s,
            RetailPrice = %s,
            Category = %s,
            SupplierLink = %s
        WHERE URL = %s
        """

        params = [extra_costs, retail_price, category, supplier_link, url]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_history(url, current_price, bid, won):
        sql = """
        INSERT INTO history (AuctionURL, CurrentPrice, Bid, Won)
        VALUES (%s, %s, %s, %s)
        """
        params = [url, current_price, bid, won]

        return Database.execute_sql(sql, params)

    @staticmethod
    def create_wishlist(url, max_price):
        sql = """
        INSERT INTO wishlist (AuctionURL, MaxPrice)
        VALUES (%s, %s)
        """
        params = [url, max_price]

        return Database.execute_sql(sql, params)

    @staticmethod
    def update_wishlist(url, max_price):
        sql = """
        UPDATE wishlist
        SET MaxPrice = %s
        WHERE AuctionURL= %s
        """
        params = [max_price, url]

        return Database.execute_sql(sql, params)

    @staticmethod
    def bought_item_on_wishlist(url, price):
        sql = """
        UPDATE wishlist
        SET Bought = 1, Bid = %s
        WHERE AuctionURL= %s
        """
        params = [url, price]

        return Database.execute_sql(sql, params)
