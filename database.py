from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb://localhost:27017/'
ca = certifi.where()

def dbConnection(): 
    try: 
        client = MongoClient(MONGO_URI) 
        db = client['db_productos_app'] 
        return db 
    except Exception as e:
        print("Error de conexión con la base de datos:", e)