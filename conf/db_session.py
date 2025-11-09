import sqlalchemy as sa
from sqlalchemy.future.engine import Engine
from sqlalchemy.orm import Session,sessionmaker

from typing import Optional

from models.model_base import Model_base


__engine: Optional[Engine] = None

def create_engine():
    global __engine

    if __engine:
        return

    conn_str = "postgresql://postgres:root@localhost:5432/finacas"
    __engine = sa.create_engine(url=conn_str, echo=False)

    return __engine




def create_session() -> Session:
    global __engine

    if not __engine:
        create_engine()

    __session = sessionmaker(bind=__engine, expire_on_commit=False, class_=Session)

    session: Session = __session()

    return session



def create_table():
    global __engine

    if not __engine:
        create_engine()
    
    import models.__all_models

    Model_base.metadata.drop_all(__engine)
    Model_base.metadata.create_all(__engine)
