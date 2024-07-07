from DB_handler import DB_handler
from LinkedList import *
import re


def parse_string_to_tuple(input_string):
    tuple_strings = re.findall(r'\(([^()]*)\)', input_string.strip("'"))
    art_id_elements = tuple_strings[0].split(',')
    a_first_element = art_id_elements[0]
    a_second_element = int(art_id_elements[1])
    a_third_element = int(art_id_elements[2])
    art_id_tup = (a_first_element, a_second_element, a_third_element)
    position_elements = tuple_strings[1].split(',')
    p_first_element = int(position_elements[0])
    p_second_element = int(position_elements[1])
    p_third_element = int(position_elements[2])
    position_tup = (p_first_element, p_second_element, p_third_element)
    tup_str = tuple_strings[2].replace(r'"" ""', "' '").replace(r'"",""', ',')
    final_version = tup_str.split(',')
    ext_char_tup = tuple(final_version)
    res = (art_id_tup, position_tup, ext_char_tup)
    return res

class TextBuilder:
    def __init__(self):
        self.db_handler = DB_handler()
        self.node = Node()
        self.ll = LinkedList()

    # def build_text(self, article_id_tuple):
    #     self.db_handler.cursor.execute("SELECT a.article_title, a.page_range, v.issue_date, "
    #                                    " aut.first_name, aut.last_name "
    #                                    " FROM art_info.articles a JOIN art_info.volumes v "
    #                                    " ON a.magazine_id = v.magazine_id AND  a.volume_id = v.volume_id JOIN art_info.authors aut"
    #                                    " ON a.author_id = aut.author_id "
    #                                    " WHERE a.magazine_id = %s AND a.volume_id = %s AND a.article_id = %s ",
    #                                    (article_id_tuple[0], article_id_tuple[1], article_id_tuple[2]))
    #     self.db_handler.connection.commit()
    #     article_title, page_range, date_of_issue, aut_f_name, aut_last_name = self.db_handler.cursor.fetchall()[0]
    #     # print("page_range: ", page_range)
    #     # print("article_title: ", article_title)
    #     # print("date_of_issue: ", date_of_issue)
    #     # print("aut_f_name: ", aut_f_name)
    #     # print("aut_last_name: ", aut_last_name)
    #     self.db_handler.cursor.execute( " SELECT word_id, word, unnest(occurrences) "
    #                                     " FROM text_handle.words, "
    #                                     " LATERAL unnest(occurrences) AS outer_tuple "
    #                                     " WHERE (outer_tuple).article_id = ROW(%s,%s,%s)::article_id_type; ",
    #                                     (article_id_tuple[0], article_id_tuple[1], article_id_tuple[2]))
    #     self.db_handler.connection.commit()
    #
    #
    #     word_occurrences = []
    #     print("Test Words table: ")
    #
    #     for row in self.db_handler.cursor:
    #         print(row)
    #         ext_tup = parse_string_to_tuple(row[2])
    #         print("word is: ", row[1])
    #         word_occurrences.append(ext_tup)
    #         print(ext_tup[0])
    #         print(ext_tup[1])
    #         print(ext_tup[2])
    #
    #     print("words: ", word_occurrences)

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





