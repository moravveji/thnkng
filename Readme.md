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
