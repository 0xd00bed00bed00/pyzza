from sqlalchemy import String, Boolean, update

from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from utils import gen_id
from common import gettmpdir, checkpaths
from sqlalchemy import create_engine
from common import DEBUG

CONNECTION_TYPES_MODEL = ['tcp', 'unix']

checkpaths()

engine = None

class Base(DeclarativeBase):
    pass

def initdb():
    global engine
    if engine is None:
        engine = create_engine(f'sqlite:///{gettmpdir()}/cache.db', echo=DEBUG)
    Base.metadata.create_all(bind=engine)

class Connection(Base):
    __tablename__ = 'connections'

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: gen_id())
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    conntype: Mapped[str] = mapped_column(String)
    connpath: Mapped[str] = mapped_column(String)
    isdefault: Mapped[bool] = mapped_column(Boolean, default=False)
    old = None
    ctype = None
    action = None

    def __init__(self, id=None, name=None, type=None, path=None):
        self.id = id
        self.name = name
        self.conntype = type
        self.connpath = path
        self.old = name

    def __repr__(self):
        return f'[{self.id}:{self.name}] {self.conntype}://{self.connpath} {self.isdefault}'
    
    def setasdefault(self):
        with Session(engine) as s:
            stmt = (
                update(Connection).
                where(Connection.isdefault==True).
                where(Connection.name!=self.name).
                values(isdefault=False)
            )
            s.execute(stmt)
            conn = (
                s.query(Connection).
                filter(Connection.name==self.name).
                first()
            )
            conn.isdefault = True
            s.commit()

    def delete(self):
        with Session(engine) as s:
            s.delete(self)
            s.commit()

    def clear():
        with Session(engine) as s:
            s.query(Connection).delete()
            s.commit()

initdb()