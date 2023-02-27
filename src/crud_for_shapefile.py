import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import geopandas
import pgclient
from pathlib import Path

# def create():pass - create shapefile in db, using geopandas
def create_shapefile_table_in_db(database_name : str, shapefile_path : str, table_name : str):
    if(pgclient.check_if_database_exists(database_name=database_name) == False):
        raise ValueError('Database Does Not Exist')
    if(Path.exists(Path(shapefile_path)) == False):
        raise ValueError('Invalid shapefile_path Given')
    gdf = geopandas.read_file(shapefile_path)

    db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        db = database_name
    )
    engine = create_engine(db_string)
    try:
        gdf.to_postgis(table_name, engine)
    except:
        raise ValueError('Table Already Exists')

# def read():pass - simply run select and print rows
def read_shapefile_table(database_name : str, table_name : str):
    if(pgclient.check_if_database_exists(database_name=database_name) == False):
        raise ValueError('Database Does Not Exist')
    db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        db = database_name
    )
    engine = create_engine(db_string)

    if(engine.dialect.has_table(engine.connect(), table_name) == False):
        raise ValueError('Table Does Not Exist')
    
    session = sessionmaker(engine)()
    query = text('SELECT * FROM {table_name}'.format(table_name = table_name))
    rows = session.execute(query)
    session.close()
    return rows

# def delete():pass - delete whole shapefile table? - simple delete
def delete_shapefile_table(database_name : str, table_name : str):
    if(pgclient.check_if_database_exists(database_name=database_name) == False):
        raise ValueError('Database Does Not Exist')
    db_string = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user = os.getenv('POSTGRES_USERNAME'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST'),
        port = os.getenv('POSTGRES_PORT'),
        db = database_name
    )
    engine = create_engine(db_string)
    if(engine.dialect.has_table(engine.connect(), table_name) == False):
        raise ValueError('Table Does Not Exist')

    session = sessionmaker(engine)()
    # commit is necessary 
    session.connection().execute(text('commit'))
    query = text('DROP TABLE {table_name}'.format(table_name = table_name))
    session.execute(query)
    session.close()
    

# def update():pass - delete old, create new 
def update_shapefile_table(database_name : str, table_name : str, new_shapefile_path : str):
    delete_shapefile_table(database_name=database_name, table_name=table_name)
    create_shapefile_table_in_db(database_name=database_name, shapefile_path=new_shapefile_path, table_name=table_name)

