# from fastapi import HTTPException
# from starlette.status import HTTP_404_NOT_FOUND
#
# from src.models import CompanyModel
# from src.schemas.company import CompanyWithUsers, CompanyRequest
# from src.schemas.user import UserDB
# from src.utils.service import BaseService
# from src.utils.unit_of_work import transaction_mode
#
#
# class PositionService(BaseService):
#     base_repository: str = "structure"
#
#     @transaction_mode
#     async def create_position(self, company_id):
#         self.uow.
#
