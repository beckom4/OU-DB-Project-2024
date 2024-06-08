
from datetime import datetime

import psycopg2

from DB_handler import DB_handler

from SearchWizard import SearchWizard

from TextLoader import TextLoader

# Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
connection = psycopg2.connect(dbname="db_project", user="omri", password="omri", options="-c search_path=text_handle")
cursor = connection.cursor()

db_test = DB_handler()

db_test.create_schemas()

db_test.create_types()

db_test.create_tables()

db_test.create_triggers()

tl = TextLoader()

sw = SearchWizard()

## Tests on Authors table
##
author_id = tl.load_author('Yuval Levy')
cursor.execute(" SELECT * FROM art_info.authors ")
for row in cursor:
    print(row)
##
## End of tests on Authors table

## Tests on Magazines table
##
magazine_id = tl.load_magazine('National Geographic')
magazine_id2 = tl.load_magazine('TIME')
cursor.execute("SELECT * FROM art_info.magazines")
for row in cursor:
    print(row)
cursor.close()
##
## End of tests on Magazines table

## Tests on Volumes table
##
cursor = connection.cursor()
# cursor.execute("INSERT INTO art_info.Volumes (magazine_id, issue_date) VALUES (%s, %s)",
#                (magazine_id, datetime(1987, 5, 30).date()))
# connection.commit()
volume_id = tl.load_volume(magazine_id, 1, datetime(1987, 5, 30).date())
volume_id2 = tl.load_volume(magazine_id, 2, datetime(1987, 6, 30).date())
cursor.execute("SELECT * FROM art_info.Volumes")
for row in cursor:
    print(row)
cursor.execute("SELECT volume_id FROM art_info.volumes ")
volume_id = cursor.fetchall()[0][0]
cursor.close()

##
## End of tests on Volumes table

## Tests on Articles table
##
cursor = connection.cursor()
tl.load_article(magazine_id, volume_id, 'The Big Bang Theory', [4, 5], author_id)
tl.load_article(magazine_id, volume_id2, 'friends', [2, 3, 4], author_id)
cursor.execute("SELECT * FROM art_info.Articles ORDER BY magazine_id, volume_id, article_id ")

print("Articles table: ")

for row in cursor:
    print(row)

cursor.execute("SELECT volume_id FROM art_info.articles ")
article_id = cursor.fetchall()[0][0]


cursor.close()

# Print all attributes and their values

## Tests on words table
##
# cursor.execute(" INSERT INTO text_handle.words (word, occurrence) VALUES "
#                " ( 'Dog', ARRAY[(%s, %s, %s, ARRAY[(1,2),(2,3),(3,4)]::position_type[])]::occurrence_type[]); ",
#                (magazine_id, volume_id, article_id))
# connection.commit()

word_list = [['Dog', [(1,2,3), (2,3,4), (3,4,5)]], ['Cat', [(1,1,1), (2,2,3), (3,3,4)]],
             ['Bird', [(1,2,1), (1,2,3), (3,5,4)]], ['Fish', [(1,1,2), (1,1,3), (1,1,4)]]]

tl.load_text([magazine_id, volume_id, article_id], word_list)

word_list2 = [['Dog', [(1,1,1), (2,2,2), (3,3,3)]], ['Bird', [(2,2,2), (3,3,3), (4,4,4)]]]

tl.load_text([magazine_id, 2, article_id], word_list2)

cursor = connection.cursor()

cursor.execute("SELECT * FROM text_handle.words ")

print("Words table: ")

for row in cursor:
    print(row)

cursor.close()

# Print all attributes and their values



##
## End of tests on Articles table

## Tests on SearchWizard
article_id_test = sw.search_author_articles('Yuval Levy')
print("article id of Yuval Levy is: ")
print(article_id_test)
#
article_id_test = sw.search_magazine_articles('National Geographic')
print("article id of National Geographic is: ")
print(article_id_test)
#
article_id_test = sw.search_magazine_volume_articles('National Geographic', 1)
print("article ids of National Geographic volume 1 is: ")
print(article_id_test)
#
article_id_test = sw.search_magazine_volume_page_articles('National Geographic', 1, [4, 5])
print("article ids of National Geographic volume 1 pages 4-5 is: ")
print(article_id_test)
#
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
