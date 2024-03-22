import motor.motor_asyncio
from bson.objectid import ObjectId
from environs import Env

#This file is closer to the models file we used in the express project

env = Env()
env.read_env()

#Use env to get the URL from the .env file for the DB
MONGODB_URL = env('MONGODB_URL')

#Initialise the MONGO DB server connection
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

#Get the database by name, if the db does not exist it is created when a collection is added and a document is added to that collection
db = client['leap_test']

#Select the collection from the db, akin to a table in SQL
users_col = db['users']

#helpers
def user_helper(user) -> dict: #-> dict has something to do with annotating the type of the argument
    return {
        'id' : str(user['_id']),
        'full_name' : user['full_name'],
        'email' : user['email']
    }

#Retrieve all users from the database
async def retrieve_users():
    users = []
    async for user in users_col.find():
        users.append(user_helper(user))
    return users

#Add a new user to the database
async def add_user(user_data : dict) -> dict:
    user = await users_col.insert_one(user_data)
    new_user = await users_col.find_one({'_id' : user.inserted_id})
    return user_helper(new_user)

#Return a user with a matching ID
async def retrieve_user(id : str) -> dict:
    user = await users_col.find_one({"_id" : ObjectId(id)})
    if user:
        return user_helper(user)
    #need some error handling here for invalid ID
    
#Update a user with matching ID
async def update_user(id : str, data: dict):
    #Return false if an empty request body is sent
    if len(data) < 1:
        return False
    user = await users_col.find_one({'_id': ObjectId(id)})
    if user:
        updated_user = await users_col.update_one({'_id' : ObjectId(id)}, {'$set' : data})
        if updated_user:
            return True
        return False
    
#Delete a user from the database
async def delete_user(id : str):
    user = await users_col.find_one({'_id' : ObjectId(id)})
    if user:
        await users_col.delete_one({'_id' : ObjectId(id)})
        return True
