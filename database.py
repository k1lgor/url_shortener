import random
import string

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///urls.db', echo=True)
Session = sessionmaker(bind=engine)


class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False)

    @staticmethod
    def generate_short_code():
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(6))


Base.metadata.create_all(engine)
