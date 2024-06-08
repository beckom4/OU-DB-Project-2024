############################################################################################################
#              This module is responsible for searches in the database according                           #
#              to key elements provided by the user                                                        #
#              The functions in this class implement the 3rd requirement of the assignment                 #
############################################################################################################

from DB_handler import DB_handler


class SearchWizard:
    def __init__(self):
        self.db_handler = DB_handler()

    ## The first 2 requirements are taken care of by the class db_handler

    ## The following cluster of functions is supposed to take care of requirement number 3
    #  in the project's requirements. The cluster ends in the next ##

    # Search for all the articles written by an author whose name was provided by the user.
    # The loop takes care of the case where there can be multiple authors with the same name.
    # In that case, we fetch the articles that were written by all of them.
    def search_author_articles(self, author_full_name):
        author_ids = self.db_handler.get_author_id_from_name(author_full_name)
        for author_id_tuple in author_ids:
            author_id = author_id_tuple[0]
            self.db_handler.cursor.execute("SELECT magazine_id, volume_id, article_id "
                                           " FROM art_info.articles"
                                           " WHERE author_id = %s ", (author_id,))
            self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    # Search for all the articles in a specific magazine.
    # The assumption is that there are no 2 magazines with the same name.
    def search_magazine_articles(self, magazine_name):
        magazine_id = self.db_handler.get_magazine_id_from_name(magazine_name)[0][0]
        self.db_handler.cursor.execute(" SELECT magazine_id, volume_id, article_id "
                                       " FROM art_info.articles WHERE magazine_id = %s", (magazine_id,))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    # Search for all the articles in a specific magazine and volume.
    def search_magazine_volume_articles(self, magazine_name, volume_id):
        magazine_id = self.db_handler.get_magazine_id_from_name(magazine_name)[0][0]
        self.db_handler.cursor.execute("SELECT magazine_id, volume_id, article_id"
                                       " FROM art_info.articles WHERE magazine_id = %s AND volume_id = %s",
                                       (magazine_id, volume_id))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    # Search for all the articles in a specific magazine, volume and page range.
    def search_magazine_volume_page_articles(self, magazine_name, volume_id, page_range):
        magazine_id = self.db_handler.get_magazine_id_from_name(magazine_name)[0][0]
        self.db_handler.cursor.execute(" SELECT magazine_id, volume_id, article_id"
                                       " FROM art_info.articles WHERE magazine_id = %s AND volume_id = %s AND "
                                       "page_range @> ARRAY[%s]", (magazine_id, volume_id, page_range))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    # Search for all the articles that were published a specific date
    def search_articles_date(self, date):
        self.db_handler.cursor.execute("SELECT a.magazine_id, a.volume_id, a.article_id "
                                       " FROM art_info.articles a JOIN art_info.volumes v "
                                       " ON a.magazine_id = v.magazine_id AND a.volume_id = v.volume_id "
                                       " WHERE issue_date = %s", (date,))
        self.db_handler.connection.commit()
        return self.db_handler.cursor.fetchall()

    ## End of the cluster of functions for requirement number 3

    ## The following cluster of functions is supposed to take care of requirement number 4
    #  in the project's requirements. The cluster ends in the next ##
    # def
    ## End of the cluster of functions for requirement number 4
