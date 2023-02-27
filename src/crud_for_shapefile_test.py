import crud_for_shapefile

# crud_for_shapefile.create_shapefile_table_in_db('test1', '../dataset/shapefile_data/357/357_polygons.shp', 'testing1')

# res = crud_for_shapefile.read_shapefile_table('test1', 'testing1')
# for r in res:
#     print(r)
# print(res)

crud_for_shapefile.delete_shapefile_table('test1', 'testing1')

