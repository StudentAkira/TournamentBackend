from sqlalchemy.orm import Session
from starlette.responses import Response

from db.crud.annotation.annotation import get_annotations_db
from db.schemas.annotation.annotation_create import AnnotationCreateSchema
from db.schemas.annotation.annotation_delete import AnnotationDeleteSchema
from db.schemas.annotation.annotation_get import AnnotationGetSchema
from db.schemas.annotation.annotation_update import AnnotationUpdateSchema
from managers.annotation_manager import AnnotationManager
from managers.token import TokenManager
from managers.user import UserManager


class AnnotationService:
    def __init__(self, db: Session):
        self.__db = db

        self.__user_manager = UserManager(db)
        self.__token_manager = TokenManager(db)
        self.__annotation_manager = AnnotationManager(db)

        self.__annotation_created_message = "annotation created"
        self.__annotation_updated_message = "annotation updated"
        self.__annotation_deleted_message = "annotation deleted"

    def get_annotations(self, offset: int, limit: int) -> list[AnnotationGetSchema]:
        nominations_db = get_annotations_db(self.__db, offset, limit)
        return [AnnotationGetSchema.from_orm(nomination_db) for nomination_db in nominations_db]

    def create_annotation(self, response: Response, token: str, annotation_data: AnnotationCreateSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_is_not_admin(decoded_token.role)

        annotation_db = self.__annotation_manager.get_by_text(annotation_data.text)
        self.__annotation_manager.raise_exception_if_text_taken(annotation_db)
        self.__annotation_manager.create(decoded_token.user_id, annotation_data)
        return {"message": self.__annotation_created_message}

    def update_annotation(self, response: Response, token: str, annotation_data: AnnotationUpdateSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_is_not_admin(decoded_token.role)

        annotation_db = self.__annotation_manager.get_by_id_and_user_id(annotation_data.id, decoded_token.user_id)
        self.__annotation_manager.raise_exception_if_not_found(annotation_db)

        annotation_with_new_text_db = self.__annotation_manager.get_by_text(annotation_data.new_text)
        self.__annotation_manager.raise_exception_if_text_taken(annotation_with_new_text_db)
        self.__annotation_manager.update(annotation_db, annotation_data)
        return {"message": self.__annotation_updated_message}

    def delete_annotation(self, response: Response, token: str, annotation_data: AnnotationDeleteSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_is_not_admin(decoded_token.role)

        annotation_db = self.__annotation_manager.get_by_id_and_user_id(annotation_data.id, decoded_token.user_id)
        self.__annotation_manager.raise_exception_if_not_found(annotation_db)

        self.__annotation_manager.delete(annotation_db)
        return {"message": self.__annotation_deleted_message}
