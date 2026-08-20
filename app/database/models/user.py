import enum
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy import func
from app.database.database import Base
<<<<<<< HEAD
from sqlalchemy.orm import relationship
=======
>>>>>>> a248c5bcbe75973cf774005ddd712eb06ebcc5d8

class UserRole(str, enum.Enum):
    STUDENT  = "student"
    ADMIN = "admin"


class UserStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    BLOCKED = "blocked"

class User(Base):
    __tablename__ = 'users' 

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, index=True ,nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    phone = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)

    address = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)

    status = Column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    

    created_at = Column(DateTime(timezone=True), server_default=func.now())
<<<<<<< HEAD
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    attendances = relationship("Attendance", back_populates="student")
=======
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
>>>>>>> a248c5bcbe75973cf774005ddd712eb06ebcc5d8
