# thnkng

## Purpose
This repository provides a simple Python interface to the MySQL database for the users on the VSC **ThinKing** cluster (hence the repository name). With this, it is possible to query for the users information across multiple tables, and easily merge the results.

The `thnkng_db` class can provide instances for two databases:
+ `hpc_thnkng_stats`
+ `hpc_thnkng_reps`

## Contents
+ `db_lib.py`: The basic module to import. The `thnkng_db` class lives here.

## Requirements
+ Python 2.7
+ `mysql.connector` package (https://www.mysql.com/products/connector)

## Example
```python
from import thnkng import db_lib as dl

with dl.thnkng_db('hpc_thnkng_stats') as db:
  conn  = db.get_connection()
	curs  = db.get_cursor()
	query = 'select * from users'
	curs.execute(query)
	users = curs.fetchall()
```
