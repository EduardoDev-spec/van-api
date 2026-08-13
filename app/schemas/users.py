import re
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional, Literal
from datetime import datetime, date
from validate_docbr import CPF
from app.database.models.user import UserRole, UserStatus

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    cpf: str
    address: Optional[str] = None
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        cpf_validator = CPF()
        
        if not cpf_validator.validate(v):
            raise ValueError('CPF inválido ou dígitos verificadores incorretos.')
        
        return re.sub(r'[^0-9]', '', v)

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole = UserRole.STUDENT
    status: UserStatus = UserStatus.PENDING
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserMeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    status: UserStatus

    model_config = ConfigDict(from_attributes=True)


class AttendanceCreate(BaseModel):
    data: date
    shift: Literal["morning", "night"]
    is_confirmed: bool = True
    transport_mode: Optional[Literal["ida_e_volta", "so_ida", "so_volta"]] = None

