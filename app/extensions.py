from pymongo import MongoClient

# Function to connect to MongoDB Atlas
def connect_mongo():
    # Replace this URI with your actual connection string
    client = MongoClient("mongodb+srv://webuser:web1234@cluster0.sv0nyyl.mongodb.net/webhookDB?retryWrites=true&w=majority")
    
    # Connect to the 'webhookDB' database
    db = client["webhookDB"]
    return db
