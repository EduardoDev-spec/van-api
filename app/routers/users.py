from fastapi import APIRouter, HTTPException, status
from app.database.database import db_dependency
from app.database.models.user import User
from app.database.models.attendance import Attendance
from app.schemas.users import UserCreate, UserResponse, UserMeResponse, AttendanceCreate, UserRole
from app.core.security import get_password_hash
from app.routers.auth import user_dependency

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: db_dependency):
    
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    db_user_cpf = db.query(User).filter(User.cpf == user.cpf).first()
    if db_user_cpf:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    hashed_password = get_password_hash(user.password)
    
    user_data = user.model_dump(exclude={"password"})
    new_user = User(**user_data, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/me', response_model=UserMeResponse)
async def read_current_user(db: db_dependency, current_user: user_dependency):

    if user['role'] != UserRole.STUDENT.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    user = db.query(User).filter(User.id == current_user['id']).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import date
from typing import Literal, Optional

class AttendanceCreate(BaseModel):
    data: date
    shift: Literal["morning", "night"]
    is_confirmed: bool = True
    transport_mode: Optional[Literal["ida_e_volta", "so_ida", "so_volta"]] = None


@router.post('/attendances')
async def confirm_attendance(user: user_dependency, db: db_dependency, attendance_data: AttendanceCreate):
    
    if user.get('role') != UserRole.STUDENT.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    user_id = user.get('id')

    
    existing_attendance = db.query(Attendance).filter(
        Attendance.user_id == user_id, 
        Attendance.date == attendance_data.data, 
        Attendance.shift == attendance_data.shift
    ).first()

    if existing_attendance:
        existing_attendance.is_confirmed = attendance_data.is_confirmed
        existing_attendance.transport_mode = attendance_data.transport_mode
        db.commit()
        db.refresh(existing_attendance)
        return existing_attendance

    
    new_attendance = Attendance(
        user_id = user_id,
        date = attendance_data.data,  
        shift = attendance_data.shift,
        is_confirmed = attendance_data.is_confirmed,
        transport_mode = attendance_data.transport_mode
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance