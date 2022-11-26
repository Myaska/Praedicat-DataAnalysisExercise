import pandas as pd
import xml.etree.ElementTree as et
import numpy as np
import re
import psycopg2
from sqlalchemy import create_engine

"""  These functions read data from diverse sources  """
def read_mesh_file(path_mesh):
    
    tree = et.parse(path_mesh)
    root = tree.getroot()
    
    keys_values = {}
    mesh = pd.DataFrame()

    depth = len(root[0])+ len(root[1])
    for tag in tree.iter():
        if not len(tag):
            keys_values[tag.tag] = tag.text  
            if len(keys_values) == depth:
                mesh = mesh.append(keys_values, ignore_index=True)

    return mesh

def read_chemid(path_chemid):
    
    tree = et.parse(path_chemid)
    root = tree.getroot()
    
    keys_values = {}
    chemid = pd.DataFrame()
    for elem in root:
        for tag in elem.iter():
            keys_values[tag.tag] = tag.text 
            chemid = chemid.append(keys_values, ignore_index=True)
    
    return  chemid


def read_ecxel(path_excel):
    
    excel = pd.read_excel(path_excel, skiprows=1)
    
    return excel 


def read_ppis(path_ppis):
    
    ppis_chemname = pd.read_csv(path_ppis,
                                 sep = '\s{4,}',
                                 header=None,
                                 encoding= 'unicode_escape',
                                 error_bad_lines=False)
     
    return ppis_chemname


"""  These functions clean extracted data  """    
def clean_mesh_file(mesh):

    mesh.rename(columns={"RelatedRegistryNumber": "CAS_No"}, inplace = True)
    mesh.rename(columns={"String": "Agent"}, inplace = True)   
    mesh['CAS_No'] = mesh['CAS_No'].str.replace(r'\D+', '', regex=True)
    ready_mesh = mesh.groupby(['CAS_No'], as_index=False).agg(lambda x: set(x))
    
    return ready_mesh   
 

def clean_chemid_file(chemid):
    
    chemid.rename(columns={"CASRegistryNumber": "CAS_No", 'SystematicName' : 'Agent'}, inplace = True)
    chemid = chemid.apply(lambda x: x.str.strip()).replace('', np.nan)
    chemid.dropna(how = 'all', axis = 1, inplace = True)
    chemid.rename(columns={"displayName": "Agent"}, inplace = True)
    ready_chemid = chemid.groupby(['CAS_No'], as_index=False).agg(lambda x: set(x))
    
    return ready_chemid

def clean_excel_file(excel):    

    excel.rename(columns={"Additional information" : "Note", "Group" : "GroupNo", "CAS No." : "CAS_No"}, inplace = True)
    excel['CAS_No'] = excel['CAS_No'].str.replace(r'\D+', '', regex=True)
    ready_excel = excel[excel['CAS_No'].notna()] 
    
    return ready_excel 


def clean_ppis(ppis_chemname):
    
    ppis = ppis_chemname.rename(columns={0: "id", 1 : "Agent"})
    ppis['id'] = ppis['id'].str[:6]
    ppis.dropna(inplace = True)
    ppis[['Agent', 'CAS_No']] = ppis['Agent'].str.rsplit('CAS Reg. No.', n=1, expand=True)    
    ppis['Agent'] = ppis[['id','Agent','CAS_No']].groupby(['id'])['Agent'].transform(lambda x: '|'.join(x))
    ppis = ppis.replace('',np.nan).groupby(['id','Agent'], as_index=False).agg(
                                                            {'CAS_No':lambda x: x.dropna()})   
    ppis['CAS_No'] = ppis['CAS_No'].str.replace(r'\D+', '', regex=True)
    ready_ppis = ppis[ppis['CAS_No'].notna()]
    
    return ready_ppis 

"""  These functions customize data  """  
def create_data_source(data, name):
    
    data['DataSource'] = name
    
    return data

def cas_uniform(data):
    
    data["CAS_No"].replace(to_replace='-', value='', regex=True, inplace=True)
    
    return data


"""  This function join all data  """  
def join_data(ready_mesh, ready_chemid, ready_excel, ready_ppis, path, save_to):

    merge = pd.concat([ready_mesh, ready_chemid, ready_excel, ready_ppis], ignore_index = True).astype(object)
    merge_clean = merge.fillna('')    
    merge_clean = merge_clean.applymap(str)
    merge_clean = merge_clean.replace(r"\}|\{|\'", '', regex=True)
    merge_gr = merge_clean.groupby(['CAS_No'], as_index=False).agg(lambda x: [x for x in list(x) if x] if [x for x in list(x) if x] else None)
    merge_gr = merge_gr.applymap(str)
    merge_gr = merge_gr.replace(r"\]|\[|\'", '', regex=True)
    merge_gr = merge_gr.replace('None', None, regex=True)
    merge_gr.to_csv(path + save_to, index=True)
    
    columns = merge_gr.columns
    
    return columns, merge_gr


"""  These functions opearate in PostgresSQL  """  
def postgres_connection(dbname, user, password):
    conn = psycopg2.connect("dbname={0} user={1} password={2}".format(dbname, user, password))
    cursor = conn.cursor()
    
    return conn, cursor
 
def create_table(postgres_table_name, conn, cursor, columns):
    
    sql = str([i + ' CHAR(45)' for i in columns])
    sql = re.sub(r"\]|\[|\'",'', sql) 
    cursor.execute("CREATE TABLE IF NOT EXISTS %s(%s)"%(postgres_table_name, sql))
    conn.commit()

def put_data_to_db(dbname, user, password, merge_gr, postgres_table_name):
    
    engine = create_engine('postgresql://{0}:{1}@localhost:5432/{2}'.format(user, password, dbname))
    merge_gr.to_sql(postgres_table_name, engine, if_exists='replace')



   