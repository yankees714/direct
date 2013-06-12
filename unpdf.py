#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileReader
import re
import pprint
import sqlite3

# set up the stuff from imported libraries
connection = sqlite3.connect('oracleapp/default.db')
db = connection.cursor()
pp = pprint.PrettyPrinter(indent=4)
pdf = PdfFileReader(file("./data.pdf", "rb"))

# purge the old and create the new database
db.execute('''DROP TABLE search_person''')
connection.commit()
db.execute('''CREATE TABLE search_person (id int, fname text, mname text, lname text, suffix text, year int, su text, email text, phone text, apt text)''')
connection.commit()

content = ""  # data types in python are super weird
for page in pdf.pages:
    content += page.extractText()

#content += pdf.getPage(0).extractText()

#remove the singlequote from the class year
years = re.findall(u"\xd5"+r"[0-9][0-9]", content)
for year in years:
    content = content.replace(year, "20"+''.join(year[1:]))

#remove the letter category headings HELL YEAH THIS ACTUALLY WORKS
doubles = re.findall("[A-Z]{2}", content)
for double in doubles:
    if double != "II":
        content = content.replace(double, double[0])

#remove this bullshit
content = content.replace("Student Directory, Fall 2012This directory is solely for the use of members of the Bowdoin College community. Names, addresses, phone numbers, and e-mail addresses are not to be used, lent, sold, or distributed for solicitation or for political purposes, either through U.S. mail, campus mail, e-mail, social media, or fax. Use of campus mail for political purposes or for charitable solicitations is prohibited by Federal Law. Information is current as of September 14, 2012.", "")

#translate weird unicode characters
unicodez = {
          ord(u'ß'): u'fl',
          ord(u'Þ'): u'fi',
          ord(u'Õ'): u'\'',
          ord(u'Œ'): u'ñ',
        }
content = content.translate(unicodez)

#split on the last four characters of every line (thank god they put that on there)
content = content.split("S.U.")

id = 1

for line in content:
    line = line.strip()

    # yes. this is ineffecient, terrible fucking code. but w/e, it's just to build a database with.

    if len(line) != 0:
        name = line.split("20")[0]

        lname = name.split(", ")[0].strip()
        given = name.split(", ")[1].strip()

        if len(name.split(", ")) == 3:
            suffix = name.split(", ")[2]
        else:
            suffix = ""

        fname = given.split(" ")[0].strip()
        mname = ' '.join(given.split(" ")[1:])

        year = "20"+''.join(line.split("20")[1:]).split(" ")[0]

        su = line.split(" ")[-1]

        email = line.split(" ")[-3]

        phone = line.split(" ")[-5]
        if not re.match("[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", phone):
            phone = "Unknown"

        # the dorms are super hard because they're not a constant number of words and occasionally don't exist
        apt = line
        everythingbutdorm = {fname: '', mname.strip('.'): '', lname: '', year: '', email: '', phone: '', suffix.strip('.'): '', su: ''}
        for i, j in everythingbutdorm.iteritems():
            apt = re.sub(r'\b'+re.escape(i)+r'\b', j, apt)
        apt = apt.replace(",", "").strip(' .')
        apt = apt.replace("Jr. ", "")
        if apt == "":
            apt = "Off-Campus or Unknown"

        db.execute("INSERT INTO search_person VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, fname, mname, lname, suffix, year, su, email, phone, apt))
        connection.commit()

        id+=1

db.close()
