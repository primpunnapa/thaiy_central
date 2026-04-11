from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .session import Base
import enum

# Enums
class PlatformEnum(str, enum.Enum):
    IQIYI = "iqiyi"
    VIU = "viu"
    NETFLIX = "netflix"
    AISPLAY = "aisplay"
    ONED = "oned"
    WETV = "wetv"


class Series(Base):
    __tablename__ = "series"
    
    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey('studios.id'), nullable=False)
    title_th = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    description = Column(Text)
    release_year = Column(Integer)
    poster_url = Column(String(500))
    status = Column(String(50), default="ongoing")
    views = Column(Integer, default=0)
    air_day = Column(String(20), nullable=True)
    air_time = Column(String(10), nullable=True)
    platforms = Column(JSON, default=list)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    studio = relationship("Studio", back_populates="series")

class Studio(Base):
    __tablename__ = "studios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    website_url = Column(String(200))
    logo_url = Column(String(200))
    # One-to-many relationship with series
    series = relationship("Series", back_populates="studio")

class UserRole(str, enum.Enum):
    NORMAL = "normal"
    EDITOR = "editor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.NORMAL)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)