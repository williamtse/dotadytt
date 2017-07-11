#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from conf.config import *

engine = create_engine('mysql+mysqlconnector://'+DB_TEST_USER+':'+DB_TEST_PASSWORD+'@'+DB_TEST_HOST+':'+str(DB_TEST_PORT)
                       +'/'+DB_TEST_DBNAME,
                       pool_size=50, max_overflow=0)

db_session=scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
conn = engine.connect()
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import db.Orms
    Base.metadata.create_all(bind=engine)


