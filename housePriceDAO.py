import mysql.connector
import dbconfig as cfg

class HousePriceDAO:
    db=""
    def initConnectToDB(self):
        db = mysql.connector.connect(
            host=       cfg.mysql["host"],
            user=       cfg.mysql["user"],
            password=   cfg.mysql["password"],
            database=   cfg.mysql["database"],
            pool_name="my_connection_pool",
            pool_size=5
        )
        return db

    def getConnection(self):
        db = mysql.connector.connect(
            pool_name="my_connection_pool",
        )
        return db

    def __init__(self):
        db = self.initConnectToDB()
        db.close()

    def checkLogin(self, uname, upass):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "select * from users where uname = %s and upass=%s"
        values = (uname, upass)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if not result:
            db.close()
            print("No match found")
            return "No match found!"

        print("Match found")
        colnames=['id', 'uname', 'upass', 'level']
        retResult = self.convertToDictionary(result, colnames)

        db.close()
        print(retResult)
        return retResult

    def create(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql="insert into houses (descr, beds, baths, area, price) values (%s, %s, %s, %s, %s)"
        cursor.execute(sql, values)
        db.commit()
        lastRowId = cursor.lastrowid
        db.close()
        return lastRowId

    def getAllHouses(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select h.id, h.descr, h.beds, h.baths, a.name, h.price from houses h left join areas a on h.area = a.id"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        colnames=['id','descr','beds', 'baths', 'area', 'price']

        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result, colnames))

        db.close()
        return returnArray

    def getAllAreas(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select id, name, latitude, longitude from areas"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        colnames=['id','name','latitude', 'longitude']

        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result, colnames))

        db.close()
        return returnArray



    def findByID(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select h.id, h.descr, h.beds, h.baths, a.name, h.price from houses h left join areas a on h.area = a.id where h.id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        colnames=['id','descr','beds', 'baths', 'area', 'price']
        house = self.convertToDictionary(result, colnames)
        db.close()
        return house

    def update(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql="update houses set descr= %s, beds=%s, baths=%s, area=%s, price=%s where id = %s"
        cursor.execute(sql, values)
        db.commit()
        db.close()

    def delete(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="delete from houses where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        print(self)

        db.commit()
        db.close()

    def convertToDictionary(self, result, colnames):
        #colnames=['id','descr','beds', 'baths', 'area', 'price']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
   


        
housePriceDAO = HousePriceDAO()