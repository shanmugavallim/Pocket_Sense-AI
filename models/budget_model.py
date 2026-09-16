from sqlalchemy import Column, Integer, Float, String
from database.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    amount = Column(Float, nullable=False)