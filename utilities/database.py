from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    discord_id = Column('discord_id', String, primary_key=True)
    discord_name = Column('discord_name', String)
    minecraft_name = Column('minecraft_name', String)
    
    
def create_db() -> None:
    engine = create_engine(os.getenv('DB_URI'))
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.close()
    
    
class DataBaseUtils():
    def __init__(self) -> None:
        engine = create_engine(os.getenv('DB_URI'))
        self.Session = sessionmaker(bind=engine)
        self.User = User
        
    def fetch_user(self, *, discord_id: int) -> User | bool | int:
        """query database for user

        Args:
            discord_id (int): the discord_id of the user to query for

        Returns:
            User | bool | int: return user if user, else returns false. Returns -1 on error.
        """
        from . import logger
        with self.Session() as session:
            try:
                user: User = session.query(User).filter(User.discord_id == discord_id).first()
                if not user:
                    return False
                return user
            except Exception as error:
                logger.error(f'An error has occured: {error}')
                return -1
    
    def insert_user(self, *, discord_id, discord_name, minecraft_name) -> bool:
        from . import logger
        with self.Session() as session:
            try:
                user = User(discord_id=discord_id, discord_name=discord_name, minecraft_name=minecraft_name)
                session.add(user); session.commit()
                return True
            except Exception as error:
                logger.error(f'An error has occured: {error}')
                return False