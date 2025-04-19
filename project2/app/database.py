import pymongo


def get_db():
    # MongoDB connection URL (adjust host/port if different)
    url = "mongodb://localhost:27017/"

    # Create a MongoClient to connect to MongoDB
    client = pymongo.MongoClient(url)

    # Access (or create) the 'user_details' database
    db = client["user_details"]

    # Return the full database object so you can access collections like:
    # get_db()["users"], get_db()["calculations"], etc.
    return db
