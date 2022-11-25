import utilities as util
import yaml

with open('params.yml') as f:
    params = yaml.safe_load(f)
 
"""  Parameters from .yaml file  """
path = params['files']['path']
path_to_mesh = params['test']['path_test_mesh']
path_to_chemid = params['test']['path_test_chemid']
save_to = params['csv_directory']['save_to']

postgres_table_name = params['postgres']['postgres_table_name']
dbname = params['postgres']['dbname']
user = params['postgres']['user']
password = params['postgres']['password']

"""  Reading and cleaning .xml file with MeSH Data  """
mesh_file = params['test']['mesh_file']
path_mesh = path_to_mesh + mesh_file
mesh = util.read_mesh_file(path_mesh)
ready_mesh = util.clean_mesh_file(mesh)
ready_mesh = util.cas_uniform(ready_mesh)
ready_mesh = util.create_data_source(ready_mesh, mesh_file)

"""  Reading and cleaning .xml file with ChemIDplus Data  """
chemid_file = params['test']['chemid_file']
path_chemid = path_to_chemid + chemid_file 
chemid = util.read_chemid(path_chemid)
ready_chemid = util.clean_chemid_file(chemid)
ready_chemid = util.cas_uniform(ready_chemid)
ready_chemid = util.create_data_source(ready_chemid, chemid_file)

"""  Reading and cleaning .xls file  """
excel_file = params['files']['excel_file']
path_excel = path + excel_file
excel = util.read_ecxel(path_excel)
ready_excel = util.clean_excel_file(excel)
ready_excel = util.cas_uniform(ready_excel)
ready_excel = util.create_data_source(ready_excel, excel_file)

"""  Reading and cleaning chemname file from PPIS  """
ppis_file = params['files']['ppis_file']
path_ppis = path + ppis_file
ppis_chemname = util.read_ppis(path_ppis)
ready_ppis = util.clean_ppis(ppis_chemname)
ready_ppis = util.cas_uniform(ready_ppis)
ready_ppis = util.create_data_source(ready_ppis, ppis_file)

"""  Data aggregation  """
columns = util.join_data(ready_mesh, ready_chemid, ready_excel, ready_ppis, path, save_to)

"""  Loading data to PostgresSQL DataBase  """
conn, cursor = util.postgres_connection(dbname, user, password)
util.create_table(postgres_table_name, conn, cursor, columns)
util.put_data_to_db(conn, cursor, save_to)
