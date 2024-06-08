############################################################################################################
#              This module is responsible for loading text from the articles into the database             #
#              The functions in this class implement the 1st and 2nd requirements of the assignment        #
############################################################################################################

from DB_handler import DB_handler


def parse_name(full_name):
    # Split the full name by spaces
    parts = full_name.split()

    # Handle cases with no spaces (single name)
    if len(parts) == 1:
        return parts[0], ''

    # Handle cases with more than one space (more than two names)
    first_name = parts[0]
    last_name = ' '.join(parts[1:])

    return first_name, last_name


class TextLoader:
    def __init__(self):
        self.db_handler = DB_handler()

    def load_author(self, author_full_name):
        author_id = self.db_handler.get_author_id_from_name(author_full_name)
        # If the author is not in the database, we add him.
        if len(author_id) == 0:
            first_name = parse_name(author_full_name)[0]
            last_name = parse_name(author_full_name)[1]
            self.db_handler.cursor.execute(" INSERT INTO art_info.authors (first_name, last_name) "
                                           " VALUES (%s, %s) RETURNING author_id", (first_name, last_name))
            self.db_handler.connection.commit()
            ret = self.db_handler.cursor.fetchall()[0][0]
        # If the author is in the database, we return the author_id.
        else:
            ret = author_id[0][0]
        return ret

    def load_magazine(self, magazine_name):
        magazine_id = self.db_handler.get_magazine_id_from_name(magazine_name)
        # If the magazine is not in the database, we add it.
        if len(magazine_id) == 0:
            self.db_handler.cursor.execute(" INSERT INTO art_info.magazines (magazine_id, magazine_name) "
                                           " VALUES (gen_random_uuid (), %s) RETURNING magazine_id", (magazine_name,))
            self.db_handler.connection.commit()
            ret = self.db_handler.cursor.fetchall()[0][0]
        else:
            ret = magazine_id[0][0]
        return ret

    def load_volume(self, magazine_id, volume_id, issue_date):
        self.db_handler.cursor.execute("SELECT magazine_id, volume_id "
                                       " FROM art_info.volumes "
                                       " WHERE magazine_id = %s AND volume_id = %s ", (magazine_id, volume_id))
        self.db_handler.connection.commit()
        volume_id_tuple = self.db_handler.cursor.fetchall()
        # If the volume is not in the database, we add it.
        if len(volume_id_tuple) == 0:
            self.db_handler.cursor.execute(" INSERT INTO art_info.volumes (magazine_id, volume_id, issue_date) "
                                           " VALUES (%s, %s, %s) RETURNING volume_id ",
                                           (magazine_id, volume_id, issue_date))
            self.db_handler.connection.commit()
            ret = self.db_handler.cursor.fetchall()[0][0]
        # If the volume is in the database, we return the volume_id.
        else:
            ret = volume_id
        return ret

    def load_article(self, magazine_id, volume_id, article_title, page_range, author_id):
        self.db_handler.cursor.execute(" INSERT INTO art_info.articles (magazine_id, volume_id, "
                                       " article_title, page_range, author_id) "
                                       " VALUES (%s, %s, %s, %s, %s) "
                                       " RETURNING article_id",
                                       (magazine_id, volume_id, article_title, page_range, author_id))
        self.db_handler.connection.commit()
        article_id_tuple = self.db_handler.cursor.fetchall()
        return article_id_tuple

    def load_text(self, article_id_tuple, word_list):
        print("word list: ", word_list)
        for word_occurrence in word_list:
            word = word_occurrence[0]
            occurrences = word_occurrence[1]
            print("word: ", word)
            print("occurrences: ", occurrences)
            self.db_handler.cursor.execute("SELECT word_id FROM text_handle.words WHERE word = %s", (word,))
            self.db_handler.connection.commit()
            word_id = self.db_handler.cursor.fetchall()
            # If the word is not in the database, we add it.
            if len(word_id) == 0:
                self.db_handler.cursor.execute("INSERT INTO text_handle.words (word, occurrences) VALUES "
                                               "  (%s, ARRAY[(%s,%s,%s,%s::position_type[])]::occurrence_type[]) ",
                                               (word, article_id_tuple[0], article_id_tuple[1],
                                                article_id_tuple[2], occurrences))
                self.db_handler.connection.commit()
            # If the word is in the database, we add the new occurrences.
            else:
                self.db_handler.cursor.execute("UPDATE text_handle.words "
                                               " SET occurrences = ARRAY_APPEND(occurrences, "
                                               "(%s,%s,%s,%s::position_type[])::occurrence_type) "
                                               " WHERE word_id = %s ",
                                               (article_id_tuple[0], article_id_tuple[1],
                                                article_id_tuple[2], occurrences, word_id[0][0]))
                self.db_handler.connection.commit()
