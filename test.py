from datetime import datetime

import psycopg2

from DB_handler import DB_handler

from SearchWizard import SearchWizard

from TextLoader import TextLoader

from TextBuilder import TextBuilder

dict_array = [
    {'When': [(1, 1, 1, ' ')]},
    {'he': [(1, 1, 2, ' ')]},
    {'was': [(1, 1, 3, ' ')]},
    {'a': [(1, 1, 4, ' '), (1, 1, 11, ' '), (2, 1, 17, ' ')]},
    {'boy': [(1, 1, 5, ' ')]},
    {'growing': [(1, 1, 6, ' ')]},
    {'up': [(1, 1, 7, ' ')]},
    {'in': [(1, 1, 8, ' '), (1, 1, 13, ' '), (1, 1, 30, ' '), (2, 1, 65, ' ')]},
    {'Wadi': [(1, 1, 9, ' ')]},
    {'Musa': [(1, 1, 10, ' ')]},
    {'town': [(1, 1, 12, ' ')]},
    {'southern': [(1, 1, 14, ' ')]},
    {'Jordan': [(1, 1, 15, ' '), (2, 1, 83, ' ')]},
    {'Mohamad': [(1, 1, 16, ' ')]},
    {'Alfarajat': [(1, 1, 17, ' '), (2, 1, 5, ', '), (2, 1, 312, ' ')]},
    {'says': [(1, 1, 18, ' '), (2, 1, 318, ' '), (2, 2, 6, ' ')]},
    {'his': [(1, 1, 19, ' '), (2, 1, 90, ' '), (2, 1, 200, ' ')]},
    {'father': [(1, 1, 20, ' '), (2, 1, 204, ' ')]},
    {'told': [(1, 1, 21, ' ')]},
    {'him': [(1, 1, 22, ' '), (2, 1, 234, ' ')]},
    {'stories': [(1, 1, 23, ' ')]},
    {'of': [(1, 1, 24, ' '), (2, 1, 102, ' ')]},
    {'green': [(1, 1, 25, ' ')]},
    {'terraces': [(1, 1, 26, ' ')]},
    {'planted': [(1, 1, 27, ' ')]},
    {'with': [(1, 1, 28, ' '), (1, 1, 36, ' ')]},
    {'wheat': [(1, 1, 29, ' '), (1, 1, 150, ' ')]},
    {'the': [(1, 1, 31, ' '), (1, 1, 45, ' '), (1, 2, 16, ' '), (1, 2, 48, ' '), (2, 1, 180, ' '),
             (2, 1, 284, ' '), (2, 1, 298, ' '), (2, 2, 44, ' '), (2, 2, 56, ' '), (2, 2, 70, ' '), (2, 1, 324, ' ')]},
    {'region’s': [(1, 1, 32, ' ')]},
    {'desert': [(1, 1, 33, ' ')]},
    {'canyons': [(1, 1, 34, ' '), (1, 1, 181, ', ')]},
    {'along': [(1, 1, 35, ' ')]},
    {'thriving': [(1, 1, 37, ' ')]},
    {'apricot': [(1, 1, 38, ' ')]},
    {'orchards': [(1, 1, 39, ' ')]},
    {'and': [(1, 1, 40, ' '), (1, 2, 1, ' '), (2, 1, 126, ' '), (2, 2, 1, ' '), (2, 1, 211, ' ')]},
    {'fig': [(1, 1, 41, ' ')]},
    {'trees': [(1, 1, 42, ' ')]},
    {'that': [(1, 1, 43, ' '), (2, 1, 108, ' '), (2, 1, 191, ' ')]},
    {'fed': [(1, 1, 44, ' '), (2, 1, 196, ' ')]},
    {'local': [(1, 1, 46, ' ')]},
    {'community': [(1, 1, 47, ' '), (2, 1, 16, ' '), (2, 1, 328, ' '), (2, 2, 14, ' ')]},
    {'now': [(2, 1, 13, ' ')]},
    {'geologist': [(2, 1, 19, ' ')]},
    {'at': [(2, 1, 29, ' ')]},
    {'Al-Hussein': [(2, 1, 32, ' ')]},
    {'Bin': [(2, 1, 43, ' ')]},
    {'Talal': [(2, 1, 47, ' ')]},
    {'University': [(2, 1, 53, ' ')]},
    {'nearby': [(2, 1, 68, ' ')]},
    {'Ma’an': [(2, 1, 76, ', ')]},
    {'little': [(2, 1, 95, ' ')]},
    {'bounty': [(2, 1, 112, ' ')]},
    {'remains': [(2, 1, 116, ' ')]},
    {'Longer': [(2, 1, 120, ' ')]},
    {'longer': [(2, 1, 129, ' ')]},
    {'dry': [(2, 1, 136, ' ')]},
    {'spells': [(2, 1, 140, ' ')]},
    {'have': [(2, 1, 147, ' ')]},
    {'made': [(2, 1, 152, ' ')]},
    {'it': [(2, 1, 157, ' ')]},
    {'harder': [(2, 1, 160, ' ')]},
    {'to': [(2, 1, 167, ' '), (2, 1, 343, ' '), (2, 1, 304, ' ')]},
    {'maintain': [(2, 1, 170, ' ')]},
    {'fields': [(2, 1, 184, ' ')]},
    {'generations': [(2, 1, 215, ' ')]},
    {'before': [(2, 1, 227, ' ')]},
    {'Since': [(2, 1, 238, ' ')]},
    {'climate': [(2, 1, 244, ' ')]},
    {'change': [(2, 1, 252, ' '), (2, 2, 18, ' ')]},
    {'started': [(2, 1, 260, ' ')]},
    {'40': [(2, 1, 269, ' ')]},
    {'years': [(2, 1, 273, ' '), (2, 2, 28, ' ')]},
    {'ago': [(2, 1, 279, ', ')]},
    {'fertile': [(2, 1, 288, ' ')]},
    {'areas': [(2, 1, 296, ' '), (2, 2, 53, ' ')]},
    {'contract': [(2, 1, 307, ' ')]},
    {'used': [(2, 1, 339, ' ')]},
    {'grow': [(2, 1, 347, ' ')]},
    {'its': [(2, 1, 353, '')]}
]


def convert_to_tuple(string_tuple, type_cast):
    # Remove the parentheses and split by commas
    items = string_tuple.strip('()').split(',')
    # Convert each item using the provided type_cast function
    return tuple(type_cast(item) for item in items)


# Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
connection = psycopg2.connect(dbname="db_project", user="omri", password="omri", options="-c search_path=text_handle")
cursor = connection.cursor()

db_test = DB_handler()

db_test.create_schemas()

db_test.create_types()

db_test.create_tables()

# db_test.create_triggers()

tl = TextLoader()

sw = SearchWizard()

tb = TextBuilder()

## Tests on Authors table
##
author_id = tl.load_author('Yuval Levy')
cursor.execute(" SELECT * FROM art_info.authors ")
print("Authors table: ")
for row in cursor:
    print(row)
##
## End of tests on Authors table

## Tests on Magazines table
##
np_id1 = tl.load_newspaper('The New York Times')
np_id2 = tl.load_newspaper('Washington Post')
cursor.execute("SELECT * FROM art_info.Newspapers")
print("Newspapers table: ")
for row in cursor:
    print(row)
cursor.close()
##
## End of tests on Magazines table
##
## Tests on Articles table
##
cursor = connection.cursor()
art_id1 = tl.load_article(np_id1, 'The Big Bang Theory', datetime(1987, 5, 30).date(), author_id)
art_id2 = tl.load_article(np_id2, 'friends', datetime(1987, 5, 30).date(), author_id)
cursor.execute("SELECT * FROM art_info.Articles ORDER BY article_id ")
print("Articles table: ")

for row in cursor:
    print(row)

cursor.close()

## Tests on words table
##

cursor = connection.cursor()
#
# 2. Mohamad Alfarajat says his father told him stories of green terraces planted with wheat in the region’s desert canyons, along with thriving apricot orchards and fig trees that fed the local community.
# Alfarajat, now a geologist at Al-Hussein Bin Talal University in nearby Ma’an, Jordan, says little of that bounty remains. Longer and longer dry spells have made it harder to maintain the fields that fed his father and generations before him.
# “Since climate change started 40 years ago, the fertile areas started to contract, ”Alfarajat says. “The community used to grow its own food on its own land, and now they import nearly everything from outside.”
#
#   (2,3,13,'," ')
#   (2,3,13,',', ' ')
#
# As drought has made local agriculture precarious, climate change has also made flash flooding more frequent, threatening both the area’s ancient ruins and local communities. And more intense temperature swings have accelerated the weathering of historic sandstone facades that were carved at the height of the Roman Empire.
# “The impact of climate change at Wadi Musa is very clear,” says Alfarajat. “If you want to see climate change impacts in front of your face, come to Petra.”
# Wadi Musa has changed in other ways since Alfarajat was a boy. Since the 1980s, the nearby archaeological site of Petra has turned into a global tourism hotspot. Nearly a million visitors visit Petra each year to marvel at the tombs and temples cut into sandstone by the Nabatean civilization almost 2,000 years ago. They, too, are threatened by flash floods, and damage to the archaeological site would endanger the tourism business locals have come to rely on.
# To protect the site in decades to come, Petra’s guardians are turning to ancient solutions, including technology left behind by the people who originally built the remarkable desert outpost.
#


# word_occurrence = [
#     ('When', [(1, 1, 1, ' ')]), ('he', [(1, 1, 2, ' ')]),
#     ('a', [(1, 1, 3, ' '), (1, 1, 9, ' ')]),
#     ('growing', [(1, 1, 4, ' ')]), ('up', [(1, 1, 5, ' ')]), ('in', [(1, 1, 6, ' '), (1, 1, 12, ' ')]),
#     ('Wadi', [(1, 1, 7, ' ')]), ('Musa', [(1, 1, 8, ' ')]), ('town', [(1, 1, 10, ' ')]),
#     ('southern', [(1, 1, 13, ' ')]), ('Jordan', [(1, 1, 14, ',')])]
word_occurrence1 = []
word_occurrence3 = [{'Dog': [(1, 2, 3, ' '), (1, 3, 5, '?')]}]

tl.load_text(art_id1, dict_array)
# tl.load_text(art_id2, word_occurrence1)
# tl.load_text(art_id2, word_occurrence3)

cursor.execute(" SELECT word_id, word, unnest(occurrences) FROM text_handle.words ")

# print("Words table: ")
# for row in cursor:
#     print(row)

# cursor.execute(" SELECT word_id, word, pos"
#                " from text_handle.words, unnest(occurrences) AS occ, unnest(occ.positions) AS pos;")
#
# print("Words table per position: ")
# for row in cursor:
#     print(row)
#     word = row[0]
#     position_str = row[1]
#     # Convert the string representations to actual tuples
cursor.close()


## Tests on SearchWizard

def extract_first_elements(tup_list):
    return [t[0] for t in tup_list]


article_list_test = sw.search_author_articles('yuval levy')
print("All article written Yuval Levy are: ")
print(article_list_test)

# article_list_test = sw.search_np_articles('The New York Times')
# print("article id of The New York Times is: ")
# print(extract_first_elements(article_list_test))
#
# article_list_test = sw.search_articles_date(datetime(1987, 5, 30).date())
# print("articles written on 1987-05-30 are: ")
# print(article_list_test)
#
# articles_word_test = sw.search_articles_word('Dog')
# print("articles according to word dog are: ")
# print(articles_word_test)
#
# #
all_words = tb.all_words()
print("All words in the database are: ")
print(extract_first_elements(all_words))

all_words_in_article = tb.all_words_in_article(art_id1[0])
print("All words in article 1 are: ")
print(extract_first_elements(all_words_in_article))
## End of tests on SearchWizard


cursor.close()
##
## End of tests on Authors table
cursor = connection.cursor()

cursor.execute(" DROP TABLE art_info.Articles")
connection.commit()
connection.commit()
cursor.execute(" DROP TABLE art_info.newspapers")
connection.commit()
cursor.execute(" TRUNCATE TABLE art_info.authors")
cursor.execute(" DROP TABLE art_info.authors")
# connection.commit()
# cursor.execute(" TRUNCATE TABLE text_handle.special_words")
# cursor.execute(" DROP TABLE text_handle.special_words")
# connection.commit()
cursor.execute(" DROP TABLE text_handle.words")
connection.commit()
# cursor.execute(" DROP TABLE text_handle.phrases")
# connection.commit()
cursor.execute(" drop type text_handle.occurrence_type; ")
cursor.execute(" drop type text_handle.position_type;")
connection.commit()
cursor.close()

# When he a growing up in a in
