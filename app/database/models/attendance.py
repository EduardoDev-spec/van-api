from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Attendance(Base):
    __tablename__ = 'attendances'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    shift = Column(String, nullable=False)
    is_confirmed = Column(Boolean, nullable=False)

    transport_mode = Column(String, nullable=True)

    student = relationship('User', back_populates='attendances')