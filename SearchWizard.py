############################################################################################################
#              This module is responsible for searches in the database according                           #
#              to key elements provided by the user                                                        #
#              The functions in this class implement the 3rd requirement of the assignment        #
############################################################################################################
import ast

from DB_handler import DB_handler


def parse_tuples_string(string_representation):
    # Remove outer curly braces and split the string into individual tuple strings
    string_representation = string_representation.strip('{}')
    tuple_strings = string_representation.split('","')

    # Clean up each tuple string
    tuples_list = []
    for tuple_str in tuple_strings:
        cleaned_tuple_str = tuple_str.strip('"').strip('()')
        tuple_elements = cleaned_tuple_str.split(',')
        tuple_int = tuple(map(int, tuple_elements))
        tuples_list.append(tuple_int)

    return tuples_list


class SearchWizard:
    def __init__(self):
        self.db_handler = DB_handler()

    ## The first 2 requirements are taken care of by the class db_handler

    ## The following cluster of functions is supposed to take care of requirement number 3
    #  in the project's requirements. The cluster ends in the next ##

    # Search for all the articles written by an reporter whose name was provided by the user.
    # The loop takes care of the case where there can be multiple reporters with the same name.
    # In that case, we fetch the articles that were written by all of them.
    def search_reporter_articles(self, reporter_full_name):
        if len(reporter_full_name) == 0:
            return None
        else:
            reporter_ids = self.db_handler.get_reporter_id_from_name(reporter_full_name)
            for reporter_id_tuple in reporter_ids:
                reporter_id = reporter_id_tuple[0]
                self.db_handler.cursor.execute(" SELECT a.article_title, n.np_name, a.date "
                                               " FROM art_info.articles a JOIN art_info.newspapers n "
                                               " ON a.np_id = n.np_id "
                                               " WHERE a.reporter_id = %s ", (reporter_id,))
                self.db_handler.connection.commit()
            return self.db_handler.cursor.fetchall()

    # Search for all the articles in a specific newspaper.
    # The assumption is that there are no 2 magazines with the same name.
    def search_np_articles(self, np_name):
        np_id_ret = self.db_handler.get_np_id_from_name(np_name)
        if len(np_id_ret) == 0:
            return None
        else:
            np_id = np_id_ret[0][0]
            self.db_handler.cursor.execute(" SELECT article_title, date "
                                           " FROM art_info.articles WHERE np_id = %s", (np_id,))
            self.db_handler.connection.commit()
            return self.db_handler.cursor.fetchall()

    # Search for all the articles that were published a specific date
    def search_articles_date(self, date):
        self.db_handler.cursor.execute(" SELECT a.article_title, n.np_name "
                                       " FROM art_info.articles a JOIN art_info.newspapers n "
                                       " ON a.np_id = n.np_id "
                                       " WHERE a.date = %s", (date,))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    # Search for all the articles that contain a specific word.
    def search_articles_word(self, word):
        if len(word) == 0:
            return None
        else:
            word_id = self.db_handler.get_word_id_from_word(word)
            self.db_handler.cursor.execute(" SELECT a.article_title, n.np_name, a.date "
                                           " FROM art_info.articles a JOIN art_info.newspapers n "
                                           " ON a.np_id = n.np_id "
                                           " WHERE a.article_id IN"
                                           " (SELECT (unnest(occurrences)).article_id AS article_id "
                                           " FROM text_handle.words "
                                           " WHERE word_id = %s)", (word_id,))
            self.db_handler.connection.commit()
            return self.db_handler.cursor.fetchall()

    def search_word_at_position(self, article_title, paragraph_number, line_number, position_in_line):
        article_id = self.db_handler.get_article_id_from_title(article_title)[0][0]
        query = """
            SELECT word
            FROM words,
                 LATERAL unnest(occurrences) AS occ(article_id, positions),
                 LATERAL unnest(occ.positions) AS pos(paragraph_number, line_number, position_in_line, finishing_chars)
            WHERE occ.article_id = %s
              AND pos.paragraph_number = %s
              AND pos.line_number = %s
              AND pos.position_in_line = %s;
        """
        self.db_handler.cursor.execute(query, (article_id, paragraph_number, line_number, position_in_line))
        self.db_handler.connection.commit()
        res = self.db_handler.cursor.fetchone()
        if res:
            return res[0]
        else:
            return None




    ## End of the cluster of functions for requirement number 3

    ## The following cluster of functions is supposed to take care of requirement number 4
    #  in the project's requirements. The cluster ends in the next ##
    # def
    ## End of the cluster of functions for requirement number 4
