from datetime import datetime

import oracledb

from DB_handler import DB_handler

# Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
connection = oracledb.connect(user="system", password="oracle", dsn="192.168.1.112:1521/XEPDB1")
cursor = connection.cursor()

db_test = DB_handler()

db_test.create_tables()

db_test.create_triggers()
##General tests:
##
# cursor.execute("CREATE TABLE test_table(id INTEGER PRIMARY KEY,name VARCHAR(50))")
# cursor.execute("INSERT INTO test_table (id, name) VALUES (111, 'testtest')")
# cursor.execute("SELECT * FROM test_table")
# for row in cursor:
#     print(row)
##
## END of general tests

## Tests on Magazines table
##
# cursor.execute("CREATE TABLE Magazines(magazine_id VARCHAR2(36) DEFAULT RAWTOHEX(SYS_GUID()) PRIMARY KEY,"
#                            "magazine_name VARCHAR(50),e_date DATE, location VARCHAR(50))")
cursor.execute("INSERT INTO Magazines (magazine_name, e_date, location) VALUES ('National Geographic', "
               "DATE '1923-05-30', 'New York')")
print("Magazines table: \n")
cursor.execute("SELECT * FROM magazines")
for row in cursor:
    print(row)

cursor.execute("SELECT magazine_id FROM magazines WHERE magazine_name = 'National Geographic'")
magazine_id = cursor.fetchall()[0][0]

# cursor.execute("TRUNCATE TABLE magazines")
# cursor.execute("DROP TABLE magazines")
##
## End of tests on Magazines table

## Tests on Volumes table
##
# cursor.execute("CREATE TABLE Volumes(magazine_id VARCHAR(36), volume_id NUMBER, issue_date DATE,"
#                     "CONSTRAINT pk_volumes PRIMARY KEY (magazine_id, volume_id),"
#                     "CONSTRAINT magazine_id_fk FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id)")
cursor.close()
cursor = connection.cursor()
cursor.execute("INSERT INTO Volumes (magazine_id, issue_date) VALUES (:1, :2)",
               (magazine_id, datetime(1987, 5, 30).date()))
connection.commit()
print("Volumes table: ")
cursor.execute("SELECT * FROM Volumes")
for row in cursor:
    print(row)
cursor.execute("SELECT volume_id FROM volumes ")
article_id_id = cursor.fetchall()[0][0]

# cursor.execute("INSERT INTO Volumes (magazine_id, issue_date) VALUES ('8CD3041608714218BD3850949D53F5E5', "
#              "DATE '1963-05-30')")

cursor.close()

##
## End of tests on Volumes table

## Tests on Articles table
##
cursor = connection.cursor()

cursor.execute("INSERT INTO Articles (magazine_id, volume_id, article_title, page_range, author_id) " 
                " VALUES (:1, :2, :3, page_range_type(:4, :5), :6) ",
               (magazine_id, article_id_id, 'The Big Bang Theory', 1, 10, 1))
connection.commit()
cursor.execute("SELECT * FROM Articles ORDER BY magazine_id, volume_id, article_id ")
page_range_table = cursor.fetchall()[0][4].aslist()

print("Articles table: ")

for row in cursor:
    print(row)
print("page range is:")
for value in page_range_table:
    print(value)
# Print all attributes and their values



##
## End of tests on Articles table

## Tests on Authors table
##
cursor.execute("INSERT INTO authors(first_name, last_name, date_of_birth, country) " 
                " VALUES ( 'Yuval', 'Levy', DATE '1987-05-30', 'Panama') ")
cursor.execute(" SELECT * FROM authors ")
for row in cursor:
    print(row)
##
## End of tests on Authors table

cursor.execute(" TRUNCATE TABLE articles ")
cursor.execute(" DROP TABLE articles")
cursor.execute(" TRUNCATE TABLE volumes")
cursor.execute(" DROP TABLE volumes")
cursor.execute(" TRUNCATE TABLE magazines")
cursor.execute(" DROP TABLE magazines")
cursor.execute(" TRUNCATE TABLE authors")
cursor.execute(" DROP TABLE authors")
