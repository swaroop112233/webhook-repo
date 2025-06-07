from pymongo import MongoClient

def connect_mongo():
    client = MongoClient("mongodb+srv://webuser:web1234@cluster0.sv0nyyl.mongodb.net/webhookDB?retryWrites=true&w=majority")
    db = client["webhookDB"]
    return db
