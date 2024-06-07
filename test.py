
from datetime import datetime

import psycopg2

from DB_handler import DB_handler

from SearchWizard import SearchWizard

# Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
connection = psycopg2.connect(dbname="db_project", user="omri", password="omri", options="-c search_path=text_handle")
cursor = connection.cursor()

db_test = DB_handler()

db_test.create_schemas()

db_test.create_types()

db_test.create_tables()

db_test.create_triggers()

sw = SearchWizard()

## Tests on Magazines table
##
# cursor.execute("CREATE TABLE Magazines(magazine_id VARCHAR2(36) DEFAULT RAWTOHEX(SYS_GUID()) PRIMARY KEY,"
#                            "magazine_name VARCHAR(50),e_date DATE, location VARCHAR(50))")
cursor.execute(" INSERT INTO art_info.Magazines (magazine_id, magazine_name, e_date, location) VALUES (gen_random_uuid (), "
               " 'National Geographic', '1923-05-30', 'New York')")
cursor.execute(" INSERT INTO art_info.Magazines (magazine_id, magazine_name, e_date, location) VALUES (gen_random_uuid (), "
               " 'TIME', '1987-05-30', 'Chicago') ")
print("Magazines table: ")
cursor.execute("SELECT * FROM art_info.magazines")
for row in cursor:
    print(row)

cursor.execute("SELECT magazine_id FROM art_info.magazines WHERE magazine_name = 'National Geographic'")
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
cursor.execute("INSERT INTO art_info.Volumes (magazine_id, issue_date) VALUES (%s, %s)",
               (magazine_id, datetime(1987, 5, 30).date()))
connection.commit()
print("Volumes table: ")
cursor.execute("SELECT * FROM art_info.Volumes")
for row in cursor:
    print(row)
cursor.execute("SELECT volume_id FROM art_info.volumes ")
volume_id = cursor.fetchall()[0][0]

# cursor.execute("INSERT INTO Volumes (magazine_id, issue_date) VALUES ('8CD3041608714218BD3850949D53F5E5', "
#              "DATE '1963-05-30')")

cursor.close()

##
## End of tests on Volumes table

## Tests on Articles table
##
cursor = connection.cursor()

cursor.execute("INSERT INTO art_info.Articles (magazine_id, volume_id, article_title, page_range, author_id) " 
                " VALUES (%s, %s, 'The Big Bang Theory', ARRAY[4,5], 1) ",
               (magazine_id, volume_id))
connection.commit()
cursor.execute("SELECT * FROM art_info.Articles ORDER BY magazine_id, volume_id, article_id ")

cursor.execute("SELECT volume_id FROM art_info.articles ")
article_id = cursor.fetchall()[0][0]

print("Articles table: ")

for row in cursor:
    print(row)

cursor.close()

# Print all attributes and their values

## Tests on words table
##
cursor = connection.cursor()

cursor.execute(" INSERT INTO text_handle.words (word, occurrence) VALUES "
               " ( 'Dog', ARRAY[(%s, %s, %s, ARRAY[(1,2),(2,3),(3,4)]::position_type[])]::occurrence_type[]); ",
               (magazine_id, volume_id, article_id))
connection.commit()
cursor.execute("SELECT * FROM text_handle.words ")

print("Words table: ")

for row in cursor:
    print(row)

cursor.close()

# Print all attributes and their values



##
## End of tests on Articles table

## Tests on Authors table
##
cursor = connection.cursor()

cursor.execute("INSERT INTO art_info.authors(first_name, last_name, date_of_birth, country) " 
                " VALUES ( 'Yuval', 'Levy', DATE '1987-05-30', 'Panama') ")
connection.commit()
cursor.execute(" SELECT * FROM art_info.authors ")
for row in cursor:
    print(row)


## Tests on SearchWizard
article_id_test = sw.search_author_articles('Yuval Levy')
print("article id of Yuval Levy is: ")
print(article_id_test)

article_id_test = sw.search_magazine_articles('National Geographic')
print("article id of National Geographic is: ")
print(article_id_test)

article_id_test = sw.search_magazine_volume_articles('National Geographic', 1)
print("article ids of National Geographic volume 1 is: ")
print(article_id_test)

article_id_test = sw.search_magazine_volume_page_articles('National Geographic', 1, [4, 5])
print("article ids of National Geographic volume 1 pages 4-5 is: ")
print(article_id_test)

article_id_test = sw.search_articles_date(datetime(1987, 5, 30).date())
print("article ids of 1987-05-30 is: ")
print(article_id_test)
## End of tests on SearchWizard



cursor.close()
##
## End of tests on Authors table
cursor = connection.cursor()

cursor.execute(" DROP TABLE art_info.Articles")
connection.commit()
cursor.execute(" TRUNCATE TABLE art_info.volumes")
cursor.execute(" DROP TABLE art_info.volumes")
connection.commit()
cursor.execute(" TRUNCATE TABLE art_info.magazines")
cursor.execute(" DROP TABLE art_info.magazines")
connection.commit()
cursor.execute(" TRUNCATE TABLE art_info.authors")
cursor.execute(" DROP TABLE art_info.authors")
connection.commit()
cursor.execute(" TRUNCATE TABLE text_handle.special_words")
cursor.execute(" DROP TABLE text_handle.special_words")
connection.commit()
cursor.execute(" DROP TABLE text_handle.words")
connection.commit()
cursor.execute(" DROP TABLE text_handle.phrases")
connection.commit()
cursor.execute(" DROP TYPE text_handle.occurrence_type")
cursor.execute(" DROP TYPE text_handle.position_type")
connection.commit()

cursor.close()
