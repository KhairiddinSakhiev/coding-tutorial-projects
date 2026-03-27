from pydantic import BaseModel, model_validator, field_validator

class UserCreate(BaseModel):
    username:str
    password:str
    confirm_password:str

    # @field_validator("*", mode="before")
    # def check_empty_values(value):
    #     if not value:
    #         raise ValueError("Please fill all fields")
    
    # @model_validator(mode="before")
    # def check_passwords(value):
    #     password = value.get("password")
    #     password2 = value.get("confirm_password")

    #     if password != password2:
    #         raise ValueError("passwords do not match")
    #     return value
    
    
class UserOut(BaseModel):
    id:int
    username:str
    
    model_config = {"from_attributes":True}
    