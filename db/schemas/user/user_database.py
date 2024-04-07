from db.schemas.user.user import UserSchema


class UserDatabaseSchema(UserSchema):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True
