#This file is where we place the schemas for a collection, this is not enforced by Mongo, pydantic allows us to define a set structure
#for data being insterted in to a collection, all schemas are classess that extend pydantics BaseModel

from typing import Optional
from pydantic import BaseModel, EmailStr, Field

#Field pattern key name: type = Field(...) <The dots indicate that this is required it could be replaced with None or a default value
#Email string is an extension of pydantic allowing for email verification, it is treated as a type
class UserSchema(BaseModel):
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    # year: int = Field(..., gt=0, lt=9) <<< Examples of using validators in field definition (greater than 0 and less than 9)
    # gpa: float = Field(..., le=4.0)

    #Config is a child class of UserSchema, can be used to set some parameters and give an example valid input
    class Config:
        scheme_extra = {
            'full_name' : 'John Doe',
            'email' : 'jdoe@gmail.com'
        }

#When making post requests this is the format, typing and rule set for the JSON data sent across
class UpdateUserModel(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        scheme_extra = {
            'example': {
                'full_name' : 'Jamie Doe',
                'email' : 'northcoders@nc.com'
            }
        }

#A function defined to organise response data from requests to the users colleciton
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

#A function to organise response data when there is an error with a request to the users collection
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}