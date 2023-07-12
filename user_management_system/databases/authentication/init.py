import pymysql

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker


pymysql.install_as_MySQLdb()

# Replace 'username', 'password', 'host', and 'db_name' with your database credentials
connection_string = "mysql://root:@localhost/authentication"
engine = create_engine(connection_string)


Base = declarative_base()



# class User(Base):
#     __tablename__ = "User"

#     id = Column(Integer, primary_key=True)
#     email = Column(String(128), nullable=False, unique=True)
#     # stored as salty hash
#     password = Column(String(128), nullable=False)
#     first_name = Column(String(64), nullable=False)
#     last_name = Column(String(64), nullable=False)
#     # type = 'A' - Store Owner, 'B'- Customer, 'C' - Courier
#     type = Column(String(1), nullable=False)




class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    # type = 'A' - Store Owner, 'B'- Customer, 'C' - Courier
    type = Column(String(1), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    forename = Column(String(256), nullable=False)
    surname = Column(String(256), nullable=False)
    # stored as salty hash
    password = Column(String(256), nullable=False)



Base.metadata.create_all(engine)


# Session = sessionmaker(bind=engine)
# session = Session()
