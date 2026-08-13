from pydantic import BaseModel, ConfigDict
from app.database.models.user import UserStatus, UserRole
from datetime import datetime


class UpdateStatusRequest(BaseModel):
    status: UserStatus

# Schema para o Admin visualizar os alunos sem expor dados excessivos
class UserAdminResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: UserRole
    status: UserStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)