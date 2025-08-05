from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="company")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="department")


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="position")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="location")


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="status")

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="organization")
    api_keys = relationship("OrgApiKey", back_populates="organization", cascade="all, delete")

class OrgApiKey(Base):
    __tablename__ = "org_api_keys"

    api_key = Column(String(255), primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    organization = relationship("Organization", back_populates="api_keys")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    contact = Column(String(255), nullable=True)

    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    internal_note = Column(Text)


    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    location = relationship("Location", back_populates="employees")
    status = relationship("Status", back_populates="employees")
    company = relationship("Company", back_populates="employees")
    organization = relationship("Organization", back_populates="employees")
