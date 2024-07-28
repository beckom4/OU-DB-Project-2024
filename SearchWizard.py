############################################################################################################
#              This module is responsible for searches in the database according                           #
#              to key elements provided by the user                                                        #
#              The functions in this class implement the 3rd requirement of the assignment        #
############################################################################################################

from DB_handler import DB_handler
import uuid
import ast
import re


def parse_nested_article_id(s):
    s = s.strip('()')
    main_parts = s.split(',', 3)
    uuid_str = main_parts[0]
    first_int = int(main_parts[1])
    second_int = int(main_parts[2])
    array_of_tuples_str = main_parts[3].strip('"{}')
    tuple_pattern = r'\(\d+,\d+,\d+\)'
    tuples = re.findall(tuple_pattern, array_of_tuples_str)
    parsed_tuples = [ast.literal_eval(t) for t in tuples]
    return (uuid_str, first_int, second_int, parsed_tuples)



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
        reporter_ids = self.db_handler.get_reporter_id_from_name(reporter_full_name)
        for reporter_id_tuple in reporter_ids:
            reporter_id = reporter_id_tuple[0]
            self.db_handler.cursor.execute(" SELECT a.article_title, n.np_name "
                                           " FROM art_info.articles a JOIN art_info.newspapers n "
                                            " ON a.np_id = n.np_id "
                                           " WHERE a.reporter_id = %s ", (reporter_id,))
            self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    # Search for all the articles in a specific newspaper.
    # The assumption is that there are no 2 magazines with the same name.
    def search_np_articles(self, np_name):
        np_id = self.db_handler.get_np_id_from_name(np_name)[0][0]
        self.db_handler.cursor.execute(" SELECT article_title "
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
        word_id = self.db_handler.get_word_id_from_word(word)[0][0]
        self.db_handler.cursor.execute( " SELECT a.article_title, n.np_name "
                                        " FROM art_info.articles a JOIN art_info.newspapers n "
                                        " ON a.np_id = n.np_id "
                                        " WHERE a.article_id IN"
                                            " (SELECT (unnest(occurrences)).article_id AS article_id "
                                            " FROM text_handle.words "
                                            " WHERE word_id = %s)", (word_id,))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    def search_article_title(self, title):
        self.db_handler.cursor.execute(" SELECT magazine_id, volume_id, article_id "
                                       " FROM art_info.articles "
                                       " WHERE article_title = %s ", (title,))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    ## End of the cluster of functions for requirement number 3

    ## The following cluster of functions is supposed to take care of requirement number 4
    #  in the project's requirements. The cluster ends in the next ##
    # def
    ## End of the cluster of functions for requirement number 4
