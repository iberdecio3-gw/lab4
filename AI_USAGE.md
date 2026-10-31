# ChatGPT Question: why isn't my python code connecting the database? {attached python code}
## Response: Your Python code might not be connecting to cohort.db because Jupyter Notebook is looking for the database in the wrong folder.

Step 1: Check where Jupyter is looking
Run this in your notebook:

import os

print(os.getcwd())
print(os.listdir())

This shows your current folder and its files. Look for cohort.db.
Step 2: Check that the database exists

import os

print(os.path.exists("cohort.db"))

- True: Jupyter can find the database.
- False: Jupyter is looking in the wrong folder.
Step 3: Connect and check the tables
If the result was True, run:
import sqlite3, pandas as pd

con = sqlite3.connect("cohort.db")

def q(sql):
    return pd.read_sql(sql, con)

q("SELECT name FROM sqlite_master WHERE type='table'")


## Step 2 was FALSE my database was in the incorrect path. Identified and fixed. 
