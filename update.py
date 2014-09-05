#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sqlite3
import os
import psycopg2


# if os.getcwd() == "/app":
#     conn_string = "host='ec2-54-225-105-169.compute-1.amazonaws.com' dbname='dct2sfiea871d8' user='nldurbrhtujxzj' password='bqJaaIxKpfVhrYd-svszgiGeLE'"
#     connection = psycopg2.connect(conn_string)
# else:
connection = sqlite3.connect('oracleapp/default.db')

db = connection.cursor()

db.execute('''DROP TABLE search_person''')
db.execute('''CREATE TABLE search_person (id int, fname text, mname text, lname text, suffix text, year int, su text, email text, phone text, apt text)''')
connection.commit()


students = []
id = 1

for student in students:
    name = ""

    lname = name.split(", ")[0].strip()
    given = name.split(", ")[1].strip()

    if len(name.split(", ")) == 3:
        suffix = name.split(", ")[2]
    else:
        suffix = ""

    fname = given.split(" ")[0].strip()
    mname = ' '.join(given.split(" ")[1:])

    year = "20"+''

    su = ""

    email = ""

    phone = ""
    if not re.match("[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", phone):
        phone = "Unknown"

    # the dorms are super hard because they're not a constant number of words and occasionally don't exist
    apt = ""

    if os.getcwd() == "/app":   #postgres
        db.execute("INSERT INTO search_person VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, fname, mname, lname, suffix, year, su, email, phone, apt))
    else:   #sqlite
        db.execute("INSERT INTO search_person VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, fname, mname, lname, suffix, year, su, email, phone, apt))
    connection.commit()

    id+=1

db.close()
