# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:11:33 2019

@author: luigi de lisi
"""
import sqlite3 as sq


class Db:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sq.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def add_to_table(self, table_name, columns, values):
        query = (f'INSERT OR REPLACE INTO {table_name} {columns} \
        VALUES{values}')
        self.conn.execute(query)
        self.conn.commit()

    def new_table(self, table_name, table_headers):
        query = (f'CREATE TABLE IF NOT EXISTS {table_name} \
                 {table_headers}')
        self.conn.execute(query)
        self.conn.commit()

    def get_column(self, table_name, column):
        query = (f'SELECT {column} FROM {table_name}')
        x = self.cursor.execute(query).fetchall()
        return x[0][0]

    def delete_row(self, table_name, column, value):
        query = (f'DELETE FROM {table_name} WHERE {column} = {value}')
        self.conn.execute(query)
        self.conn.commit()

    def delete_column(self):
        pass

    def delete_table(self):
        pass
