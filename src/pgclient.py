import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.orm import sessionmaker
import sqlalchemy_utils.functions

load_dotenv('../settings.env')

def check_if_database_exists(database_name : str):
    db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        db = database_name
    )
    # METHOD 1 - using try except
    # try:
    #     create_engine(db_string).connect()
    # except:
    #     return False
    # return True

    # METHOD 2 - using sqlalchemy_utils
    return sqlalchemy_utils.functions.database_exists(db_string)

def create_database(database_name : str):

    if(check_if_database_exists(database_name=database_name) == True):
        raise ValueError('Database Already Exists')

    db_string = 'postgresql://{user}:{password}@{host}:{port}/postgres'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT')
    )
    engine = create_engine(db_string)

    # METHOD 1 - using connection
    conn = engine.connect()
    # This conn is still in transaction, to make it active, commit it
    commit = text('commit')
    conn.execute(commit)
    query = text('CREATE DATABASE {database_name}'.format(database_name = database_name))
    conn.execute(query)
    conn.close()

    # METHOD 2 - using session
    # session = sessionmaker(engine)()
    # # We can either make a commit using this - session.connection() is escentially engine.connect()
    # session.connection().execute(text('commit'))
    # # OR we can use this - isolation level = 0 means, autocommit
    # # session.connection().connection.set_isolation_level(0)
    # query = text('CREATE DATABASE {database_name}'.format(database_name = database_name))
    # session.execute(query)
    # # session.connection().connection.set_isolation_level(1)
    # session.close()

    # METHOD 3 - using sqlalchemyutils
    # db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
    #     user = os.getenv('POSTGRES_USERNAME'),
    #     password = os.getenv('POSTGRES_PASSWORD'),
    #     host = os.getenv('POSTGRES_HOST'),
    #     port = os.getenv('POSTGRES_PORT'),
    #     db = database_name
    # )
    # sqlalchemy_utils.functions.create_database(db_string)

def delete_database(database_name : str):
    if(check_if_database_exists(database_name=database_name) == False):
        raise ValueError('Database Does Not Exist')

    db_string = 'postgresql://{user}:{password}@{host}:{port}/postgres'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT')
    )
    engine = create_engine(db_string)
    # METHOD 1 - using connection
    conn = engine.connect()
    # This conn is still in transaction, to make it active, commit it
    commit = text('commit')
    conn.execute(commit)
    query = text('DROP DATABASE {database_name}'.format(database_name = database_name))
    conn.execute(query)
    conn.close()

    # METHOD 2 - using session
    # session = sessionmaker(engine)()
    # # We can either make a commit using this - session.connection() is escentially engine.connect()
    # session.connection().execute(text('commit'))
    # # OR we can use this - isolation level = 0 means, autocommit
    # # session.connection().connection.set_isolation_level(0)
    # query = text('DROP DATABASE {database_name}'.format(database_name = database_name))
    # session.execute(query)
    # # session.connection().connection.set_isolation_level(1)
    # session.close()

    # METHOD 3 - using sqlalchemyutils
    # db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
    #     user = os.getenv('POSTGRES_USERNAME'),
    #     password = os.getenv('POSTGRES_PASSWORD'),
    #     host = os.getenv('POSTGRES_HOST'),
    #     port = os.getenv('POSTGRES_PORT'),
    #     db = database_name
    # )
    # sqlalchemy_utils.functions.drop_database(db_string)

def create_table(database_name : str, table : Table):
    if(check_if_database_exists(database_name=database_name) == False):
        raise ValueError('Database Does Not Exist')
    db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        db = database_name
    )
    engine = create_engine(db_string)
    if(engine.dialect.has_table(engine.connect(), table.name) == True):
        raise ValueError('Table Already Exist')

    # METHOD 1 
    table.create(engine)
    # METHOD 2
    # table.metadata.create_all(engine)

def delete_table(database_name : str, table : Table):
    if(check_if_database_exists(database_name=database_name) == False):
        raise ValueError('Database Does Not Exist')
    db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        db = database_name
    )
    engine = create_engine(db_string)
    if(engine.dialect.has_table(engine.connect(), table.name) == False):
        raise ValueError('Table Does Not Exist')

    # METHOD 1
    table.drop(engine)
    # METHOD 2
    # table.metadata.drop_all(engine)

def run_query_on_database(database_name : str, query : str):
    if(check_if_database_exists(database_name=database_name) == False):
        raise ValueError('Database Does Not Exist')
    db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        db = database_name
    )
    engine = create_engine(db_string)
    # Here, sessions is used, we can use conn aswell
    session = sessionmaker(engine)()
    session.connection().execute(text('commit'))
    session.execute(text(query))
    session.commit()
    session.close()


