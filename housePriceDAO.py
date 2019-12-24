import mysql.connector
import dbconfig as cfg # import db connection details

class HousePriceDAO:
    db=""

    # Connect to the database
    # Set pool_size to 5
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

    # Get a connection from the pool
    def getConnection(self):
        db = mysql.connector.connect(
            pool_name="my_connection_pool",
        )
        return db

    
    def __init__(self):
        db = self.initConnectToDB()
        db.close()

    # Check login details against db
    def checkLogin(self, uname, upass):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "select * from users where uname = %s and upass=%s"
        # Get values from function arguments
        values = (uname, upass)
        # Execute the SQL query with these values
        cursor.execute(sql, values)
        # Take the result of the SQL query
        result = cursor.fetchone()

        if not result:
            db.close()
            print("No match found")
            return "No match found!"

        print("Match found")
        # Set column names for converting to dictionary
        colnames=['id', 'uname', 'upass', 'level']
        # Return the result as a dict
        retResult = self.convertToDictionary(result, colnames)
        # Close the connection
        db.close()
        print(retResult)
        return retResult

    # Create a new house
    def create(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql="insert into houses (descr, beds, baths, area, price) values (%s, %s, %s, %s, %s)"
        cursor.execute(sql, values)
        # Commit to the database
        db.commit()
        lastRowId = cursor.lastrowid
        # Close the connection
        db.close()
        return lastRowId

    # Return all houses from db
    def getAllHouses(self):
        db = self.getConnection()
        cursor = db.cursor()
        # SQL query with a left join
        sql="select h.id, h.descr, h.beds, h.baths, a.name, h.price from houses h left join areas a on h.area = a.id"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        # Set column names for converting to dictionary
        colnames=['id','descr','beds', 'baths', 'area', 'price']

        for result in results:
            print(result)
            # Return the result as a dict
            returnArray.append(self.convertToDictionary(result, colnames))

        # Close the connection
        db.close()
        return returnArray

    # Return all houses from db
    def getAllAreas(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select id, name, latitude, longitude from areas"
        cursor.execute(sql)
        # Fetch all matching results
        results = cursor.fetchall()
        returnArray = []
        # Set column names for converting to dictionary
        colnames=['id','name','latitude', 'longitude']

        for result in results:
            print(result)
            # Return the result as a dict
            returnArray.append(self.convertToDictionary(result, colnames))

        # Close the connection
        db.close()
        return returnArray

    # Find a house in db by its id
    def findByID(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select h.id, h.descr, h.beds, h.baths, a.name, h.price from houses h left join areas a on h.area = a.id where h.id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        # Set column names for converting to dictionary
        colnames=['id','descr','beds', 'baths', 'area', 'price']
        # Return the result as a dict
        house = self.convertToDictionary(result, colnames)

        # Close the connection
        db.close()
        return house

    # Update a house in db
    def update(self, values):
        db = self.getConnection()
        cursor = db.cursor()
        sql="update houses set descr= %s, beds=%s, baths=%s, area=%s, price=%s where id = %s"
        cursor.execute(sql, values)
        # Commit to the database
        db.commit()
        # Close the connection
        db.close()

    # Delete a house in db
    def delete(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql="delete from houses where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        print(self)
        # Commit to the database
        db.commit()
        # Close the connection
        db.close()

    # Convert results to dict
    def convertToDictionary(self, result, colnames):
        # Create empty dict
        item = {}
        
        if result:
            # Build dict from results
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
    
housePriceDAO = HousePriceDAO()