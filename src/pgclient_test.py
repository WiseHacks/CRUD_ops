import pgclient
from sqlalchemy import Table, MetaData

# pgclient.create_database('test1')
# pgclient.delete_database('test1')

# print(pgclient.check_if_database_exists('test1'))

# test_table = Table('test_table', MetaData())
# pgclient.create_table('test1', test_table)
# pgclient.delete_table('test1', test_table)

pgclient.run_query_on_database('test1', 'create table test_table2(id int)')