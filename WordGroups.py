from DB_handler import *


class WordGroup:
    def __init__(self):
        self.db_handler = DB_handler()

    def get_group_id(self, group_description):
        self.db_handler.cursor.execute("SELECT group_id FROM text_handle.word_groups WHERE group_description = %s",
                                       (group_description,))
        self.db_handler.connection.commit()
        group_id = self.db_handler.cursor.fetchall()
        if len(group_id) == 0:
            return None
        else:
            return group_id[0][0]

    def create_group(self, group_description):
        self.db_handler.cursor.execute(" INSERT INTO text_handle.word_groups (group_description) "
                                       " VALUES (%s) ", (group_description,))
        self.db_handler.connection.commit()

    def add_word_to_group(self, group_id, word_id):
        self.db_handler.cursor.execute("UPDATE text_handle.word_groups SET word_ids = array_append(word_ids, %s) "
                                       " WHERE group_id = %s", (word_id, group_id))
        self.db_handler.connection.commit()

    def get_group(self, group_description):
        self.db_handler.cursor.execute("SELECT word_ids FROM text_handle.word_groups WHERE group_description = %s",
                                       (group_description,))
        self.db_handler.connection.commit()
        word_ids = self.db_handler.cursor.fetchall()
        words = []
        for word_id in word_ids[0][0]:
            self.db_handler.cursor.execute("SELECT word FROM text_handle.words WHERE word_id = %s", (word_id,))
            self.db_handler.connection.commit()
            word = self.db_handler.cursor.fetchall()
            words.append(word[0][0])
        return words

    def get_all_groups(self):
        self.db_handler.cursor.execute("SELECT group_description FROM text_handle.word_groups")
        self.db_handler.connection.commit()
        groups = self.db_handler.cursor.fetchall()
        return groups

    def is_word_in_group(self, group_id, word_id):
        query = """
        SELECT *
        FROM text_handle.word_groups
        WHERE group_id = %s AND %s = ANY(word_ids);
        """
        self.db_handler.cursor.execute(query, (group_id, word_id))
        self.db_handler.connection.commit()
        if self.db_handler.cursor.fetchall():
            return True
        else:
            return False
