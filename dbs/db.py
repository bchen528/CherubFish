#!/usr/bin/python3
'''
    Define class DatabaseStorage
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from base_entry import ShortURL
from emailentry import Email 
from base_entry import Base
class DBStorage:
    '''
        Create SQLalchemy database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Create engine and link to MySQL databse (hbnb_dev, hbnb_dev_db)
        '''
        #user = getenv("USER")
        #pwd = getenv("PWD")
        #host = getenv("HOST")
        #db = getenv("DB")
        envv = getenv("HBNB_ENV", "none")
        user = 'cherubfish'
        pwd = 'cherubpassword'
        host = 'localhost'
        db = 'commando'
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=ShortURL):
        '''
            Query current database session
        '''
        db_dict = {}

        if cls:
            objs = self.__session.query(ShortURL).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            return db_dict

    def new(self, obj):
        '''
            Add object to current database session
        '''
        self.__session.add(obj)

    def save(self):
        '''
            Commit all changes of current database session
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            Delete from current database session
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
            Commit all changes of current database session
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            Remove private session attribute
        '''
        self.__session.close()

    def count(self, cls=None):
        ''' counts all the instances of a class '''
        return len(self.all(cls))
        

    def get(self, id):
        ''' 
        returns object based on class name and id. Otherwise none
        cls: string representing the class name
        id: string representing the object ID
        '''
        try:
            return [a for a in self.all(ShortURL).values() if a.urlhash == id][0]
        except (IndexError, TypeError):
            return None

    def getemail(self):
        'gets email'
        db_dict = {}

        objs = self.__session.query(Email).all()
        for obj in objs:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            db_dict[key] = obj
        return db_dict

        
