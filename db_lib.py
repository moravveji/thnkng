
import sys, os
import logging
import mysql.connector as mycon

###########################################################
logger = logging.getLogger(__name__)
###########################################################
def _read(filename, dbname):
  """
  Read the private file with the database credentials
  
  @param filename: full path to the private file with the database credentials
  @type filename: str
  @param dbname: the name of the desired database to get the credentials
  @type dbname: str
  @return: dictionary with the credential as key/value pairs
  @rtype: dict
  """
  if not os.path.exists(filename):
    logger.error('_read: the file {0} does not exist'.format(filename))
    sys.exit(1)
 
  if not check_dbname(dbname):
    logger.error('_read: the specified database name is invalid')
    sys.exit(1) 

  with open(filename, 'r') as r: lines = r.readlines()

  dic = dict()

  if dbname == 'hpc_thnkng_stats':
    start = 0
    end   = 5
  else:
    start = 6
    end   = 11
  lines   = lines[start : end]

  for line in lines:
    key, val = line.split(':')
    dic[key] = val
  
  return dic

###########################################################
def get_dic_connections(dbname):
  """
  This function returns a dictionary with the login info for the two databases.
  The only two allowed database names (dbname) are:
  - hpc_thnkng_stats
  - hpc_thnkng_reps

  @param dbname: the name of the desired database to connect to
  @type dbname: str
  @return: the connection arguments
  @rtype: dict
  """
  if not check_dbname(dbname): 
    logger.error('get_dic_connections: dbname:{0} is not accepted'.format(dbname))
    sys.exit(1)

  return _read('private', dbname)

###########################################################

class thnkng_db(object):
  """
  A base class which creates the connection to any of the two ThinKing databases
  """
  def __init__(self, dbname):
    if not check_dbname(dbname):
      logger.error('__init__: The dbname={0} is invalid'.format(dbname))
      sys.exit(1)

    self.dbname = dbname

    self.dic_connection = get_dic_connections(dbname)
    self.connection = None
    self.cursor = None 

  # .........................  
  def __enter__(self):
    return self 

  # .........................  
  def __exit__(self, type, value, traceback):
    pass

  # .........................  
  def get_connection(self):
    """ Return the mysql.connector connection object """
    if self.connection is not None: return self.connection

    conn = mycon.connect(**self.dic_connection)
    self.connection = conn
    return conn

  # .........................  
  def get_cursor(self):
    """ Return the mysql.connector.connection.cursor object """
    if isinstance(self.connection, type(None)):
      logger.error('get_cursor: Not connected yet; first call: db.get_connection()')
      sys.exit(1)

    curs = self.connection.cursor()
    self.cursor = curs 

    return curs

  # .........................  
  def execute(self, cmnd, inputs=None):
    """ Execute the command, together with parsing the inputs """
    curs = self.cursor
    if curs is None:
      logger.error('execute: The cursor is not grabbed yet')
      sys.exit(1)

    curs.execute(cmnd, inputs)      
    # self.connection.commit()

  # .........................  
  def get_table_column_names(self, table):
    """ Get the list of column names of the desired table """
    curs = self.cursor
    if curs is None:
      logger.error('get_table_column_names: cursor is not grabbed yet')
      sys.exit(1)

    cmnd = 'select * from {0};'.format(table)
    self.execute(cmnd, None)

    return self.cursor.column_names

  # .........................  
  # .........................  

###########################################################
def check_dbname(dbname):
  """ Make sure the dbname is one of the two only valid dbnames"""
  return dbname in ['hpc_thnkng_stats', 'hpc_thnkng_reps']

