#Routes are essentially the same as controllers

from fastapi import APIRouter, Body

#Translate python dictionaries in to JSON data (serialiser)
from fastapi.encoders import jsonable_encoder

#Importing the DB functions we made in database.py
from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user
)

#Importing the Models we made in models/user.py
from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel
)

#Initiate the router object
router = APIRouter()

#A decorator that extends router, sets the method to POST, first arg = endpoint, second arg is there for documentation

#Add user to the database
@router.post('/', response_description='User data added into the database') 
async def add_user_data(user: UserSchema = Body(...)): #Takes arg user, expects it to be of the form we defined for UserSchema
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, 'User added successfully')

#Get all users
@router.get('/', response_description='Users recieved')
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, 'User data retrieved successfully')
    return ResponseModel(users, 'Empty list returned')

#Get user by id
@router.get('/{id}', response_description='User data retrieved')
async def get_user_by_id(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, 'User data retrieved successfully')
    return ErrorResponseModel('An error occurred.', 404, "Student doesn't exist")

#Update user by id
@router.put('/{id}')
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            'User with ID: {} updated successful'.format(id),
            'User name updated successfully'
        )
    return ErrorResponseModel(
        'An Error Occurred',
        404,
        'There was an error updating the student data',
    )

#Delete user by ID
@router.delete('/{id}')
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            'User with ID: {} removed'.format(id),
            'User deleted successfully'
        )
    return ErrorResponseModel(
        'An error occurred', 404, "Student with id {0} doesn't exist".format(id)
    )