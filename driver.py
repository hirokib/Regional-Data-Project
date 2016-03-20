import os
import sqlite3


DATABASE = 'main.db'
Debug = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'password'

def connect_db():
    return sqlite3.connect('main.db')

def create_table(db, schema_file_name):
    con = sqlite3.connect(db)
    cur = con.cursor()
    with open(schema_file_name, 'r') as f:
        cont = f.read()
        cur.executescript(cont)
    con.commit()
    cur.close()

class fipCode():
    def __init__(self,zipcode, updatekey,addon, state,countyno,countyname):
        self.zipcode = zipcode
        self.updatekey = updatekey
        self.addon = addon
        self.state = state
        self.countyno = countyno
        self.countyname = countyname

    def __str__(self):
        return ("zipcode: " + self.zipcode + " updatekey: " + self.updatekey + " add: " + self.addon
                + " state: " + self.state + " countyno: " + self.countyno + " countyname: " + self.countyname)


def fipToZip(string):
    zipcode = string[0:5]
    updatekey  = string[5:15]
    addon = string[15:23]
    state = string[23:25]
    countyno = string[25:28]
    countyname = string[28:]
    return  fipCode(zipcode, updatekey, addon, state, countyno, countyname)

def readFromFiles(files):
    fipCodeList = []
    for file in files:
        with open(file) as f:
            zList = []
            for line in f:
                zList.append(fipToZip(line))
            fipCodeList.extend(zList[1:])
    return fipCodeList

def insertFipToDB(fip):
    con = connect_db()
    curs = con.cursor()

    query = "INSERT INTO zipCodes VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\
            \"{}\")".format(fip.zipcode, fip.updatekey,fip.addon, fip.state,
             fip.countyno, fip.countyname)
    # print(query)
    curs.execute(query)
    # print('executed')
    con.commit()
    curs.close()

def dbInserts(fip_list):
    i = 0
    for fip in fip_list:
        print(i)
        insertFipToDB(fip)
        i+=1

def insertFipsToDBFast(files):
    con = connect_db()
    curs = con.cursor()
    i = 0
    for file in files:
        with open(file) as f:
            for line in f:
                query = "INSERT INTO zipCodes VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\
                        \"{}\")".format(line[0:5],line[5:15],line[15:23],line[23:25],line[25:28],line[28:],)
                # print(query)
                print(i)
                i+=1
                curs.execute(query)
    con.commit()
    curs.close()

if __name__ == "__main__":
    filelist = ['zipdata/zipcty'+str(x) for x in range(1,11)]
    insertFipsToDBFast(filelist)
