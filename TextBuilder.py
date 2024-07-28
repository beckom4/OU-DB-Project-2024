from DB_handler import DB_handler
from LinkedList import *
import re
import ast



def parse_string_to_tuple(word, input_string):
    res = []
    # print("input string is: ", input_string)
    tuple_strings = (input_string
                                    .replace(r'"', '') \
                                    .replace(r'\\"" \\""', "' '")\
                                    .replace(r'\\', "'")\
                                    .replace('\n', '@@@') \
                                    .replace(r'\\, \\', ','))
    parsed_tuple = ast.literal_eval(tuple_strings)
    array_of_tuples = list(parsed_tuple[1])
    for tup in array_of_tuples:
        temp_str = tup[3].replace(r'@@@@@@', '\n\n')\
                         .replace(r'@@@', '\n')\
                         .replace(r'&&&', '"')
        final_word = word + temp_str
        new_tup = tup[:3] + (final_word,)
        res.append(new_tup)
    return res

class TextBuilder:
    def __init__(self):
        self.db_handler = DB_handler()
        self.node = Node()
        self.ll = LinkedList()

    def build_entire_text(self, article_title):
        text_arr = []
        article_id = self.db_handler.get_article_id_from_title(article_title)[0][0]
        print("article_id: ", article_id)
        self.db_handler.cursor.execute("""SELECT a.article_title, a.date, r.first_name, r.last_name 
                                          FROM art_info.articles a JOIN art_info.reporters r 
                                          ON a.reporter_id = r.reporter_id 
                                          WHERE a.article_id = %s """,
                                         (article_id, ))
        self.db_handler.connection.commit()
        article_title, date_of_issue, rep_f_name, rep_last_name = self.db_handler.cursor.fetchall()[0]
        print("article_title: ", article_title)
        print("date_of_issue: ", date_of_issue)
        print("rep_f_name: ", rep_f_name)
        print("rep_last_name: ", rep_last_name)
        self.db_handler.cursor.execute( " SELECT word_id, word, unnest(occurrences) "
                                        " FROM text_handle.words, "
                                        " LATERAL unnest(occurrences) AS outer_tuple "
                                        " WHERE (outer_tuple).article_id = %s ",
                                        (article_id, ))
        self.db_handler.connection.commit()
        print("Test Words table: ")
        for row in self.db_handler.cursor:
            # print("each row is :")
            # print(row)
            tup_arr = parse_string_to_tuple(row[1],row[2])
            text_arr.extend(tup_arr)
        sorted_text_arr = sorted(text_arr, key=lambda x: (x[0], x[1], x[2]))
        print("sorted_text_arr: ", sorted_text_arr)
        final_text = ""
        for tup in sorted_text_arr:
            final_text += f"{tup[3]}"
        print("final_text: ")
        print(final_text)

    def all_words(self):
        self.db_handler.cursor.execute(" SELECT word "
                                       " from text_handle.words")
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    def all_words_in_article(self, article_id):
        self.db_handler.cursor.execute(" SELECT word "
                                       " from text_handle.words, unnest(occurrences) AS occ "
                                       " WHERE (occ).article_id = %s", (article_id,))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()





