from traceback import print_exc

from pydantic import BaseModel, EmailStr, SecretStr, Field
from pydantic_core import ValidationError
from data import Profile


class DataValidate(BaseModel):
    name: str = Field(min_length=2, max_length=24)
    lastname: str = Field(min_length=2, max_length=36)
    email: EmailStr = Field(...)
    password: SecretStr = Field(min_length=8)
    

def pyform(register):
    try:
        DataValidate.model_validate(obj=register).model_dump()
    except ValidationError:
        print_exc()
        return 'Форма заполнена неправильно, попробуйте заново'
    else:
        user_data = DataValidate.model_validate(obj=register).model_dump()
        name = user_data['name']
        lastname = user_data['lastname']
        email = user_data['email']
        password = user_data['password'].get_secret_value()
        new_user = Profile(name, lastname, email, password).new_user()
        return new_user