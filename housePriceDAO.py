import mysql.connector
import dbconfig as cfg

class HousePriceDAO:
    db=""
    def __init__(self):
        self.db = mysql.connector.connect(
        host=       cfg.mysql["host"],
        user=       cfg.mysql["user"],
        password=   cfg.mysql["password"],
        database=   cfg.mysql["database"]
        )

    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into houses (descr, beds, baths, area, price) values (%s, %s, %s, %s, %s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    def getAllHouses(self):
        cursor = self.db.cursor()
        sql="select * from houses"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionaryHouses(result))

        return returnArray

    def getAllAreas(self):
        cursor = self.db.cursor()
        sql="select * from areas"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionaryAreas(result))

        return returnArray

    def findByID(self, id):
        cursor = self.db.cursor()
        sql="select * from houses where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def update(self, values):
        cursor = self.db.cursor()
        sql="update houses set descr= %s, beds=%s, baths=%s, area=%s, price=%s, where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
    def delete(self, id):
        cursor = self.db.cursor()
        sql="delete from houses where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")

    def convertToDictionaryHouses(self, result):
        colnames=['id','descr','beds', 'baths', 'area', 'price']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

    def convertToDictionaryAreas(self, result):
        colnames=['id','name']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
housePriceDAO = HousePriceDAO()