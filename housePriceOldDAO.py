import mysql.connector
import dbconfig as cfg

class HousePriceDAO:
    db=""
    def connectToDB(self):
        self.db = mysql.connector.connect(
        host=       cfg.mysql["host"],
        user=       cfg.mysql["user"],
        password=   cfg.mysql["password"],
        database=   cfg.mysql["database"]
        )

    def __init__(self):
        self.connectToDB()

    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDB()
        return self.db.cursor()

    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into houses (descr, beds, baths, area, price) values (%s, %s, %s, %s, %s)"
        cursor.execute(sql, values)

        self.db.commit()
        lastRowId=cursor.lastrowid
        cursor.close()
        return cursor.lastrowid

    def getAllHouses(self):
        cursor = self.db.cursor()
        sql="select h.id, h.descr, h.beds, h.baths, a.name, h.price from houses h left join areas a on h.area = a.id"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []

        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))

        cursor.close()
        return returnArray


    def findByID(self, id):
        cursor = self.db.cursor()
        sql="select h.id, h.descr, h.beds, h.baths, a.name, h.price from houses h left join areas a on h.area = a.id where h.id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        house = self.convertToDictionary(result)
        cursor.close()
        return house

    def update(self, values):
        cursor = self.db.cursor()
        sql="update houses set descr= %s, beds=%s, baths=%s, area=%s, price=%s where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

    def delete(self, id):
        cursor = self.db.cursor()
        sql="delete from houses where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")
        cursor.close()

    def convertToDictionary(self, result):
        colnames=['id','descr','beds', 'baths', 'area', 'price']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item


        
housePriceDAO = HousePriceDAO()