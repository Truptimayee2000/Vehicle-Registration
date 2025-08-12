from app import app
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from dbconfig import db


class VehicleCategoryMonthly(db.Model):
    __tablename__ = 'vehicle_category'
    id = Column(Integer, primary_key=True)
    vehicle_category = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    jan = Column(Integer, default=0)
    feb = Column(Integer, default=0)
    mar = Column(Integer, default=0)
    apr = Column(Integer, default=0)
    may = Column(Integer, default=0)
    jun = Column(Integer, default=0)
    jul = Column(Integer, default=0)
    aug = Column(Integer, default=0)
    sep = Column(Integer, default=0)
    oct = Column(Integer, default=0)
    nov = Column(Integer, default=0)
    dec = Column(Integer, default=0)
    total = Column(Integer, default=0)
    created_on = Column(TIMESTAMP(timezone=False))
    created_by = Column(String(50))
    updated_on = Column(TIMESTAMP(timezone=False))
    updated_by = Column(String(50))
    is_active = Column(Boolean, default=True)


class ManufacturerMonthly(db.Model):
    __tablename__ = 'manufacture'
    id = Column(Integer, primary_key=True)
    manufacturer = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    jan = Column(Integer, default=0)
    feb = Column(Integer, default=0)
    mar = Column(Integer, default=0)
    apr = Column(Integer, default=0)
    may = Column(Integer, default=0)
    jun = Column(Integer, default=0)
    jul = Column(Integer, default=0)
    aug = Column(Integer, default=0)
    sep = Column(Integer, default=0)
    oct = Column(Integer, default=0)
    nov = Column(Integer, default=0)
    dec = Column(Integer, default=0)
    total = Column(Integer, default=0)
    created_on = Column(TIMESTAMP(timezone=False))
    created_by = Column(String(50))
    updated_on = Column(TIMESTAMP(timezone=False))
    updated_by = Column(String(50))
    is_active = Column(Boolean, default=True)


