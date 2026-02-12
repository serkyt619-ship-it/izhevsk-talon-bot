# src/db/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String)


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey("regions.id"))
    name = Column(String, nullable=False)


class Clinic(Base):
    __tablename__ = "clinics"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    name = Column(String, nullable=False)
    address = Column(String)
    aliases = Column(String)
    url = Column(String)


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    full_name = Column(String, nullable=False)
    specialty = Column(String)
    is_active = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_user_id = Column(Integer, unique=True, nullable=False)
    tg_chat_id = Column(Integer)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)


class MonitoringTask(Base):
    __tablename__ = "monitoring_tasks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tg_chat_id = Column(Integer)
    region_id = Column(Integer, ForeignKey("regions.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    mode = Column(String, default="auto")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
