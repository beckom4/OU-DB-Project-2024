from DB_handler import DB_handler
import re
import ast

def parse_string_to_tuple_ind(input_string):
    res = []
    tuple_strings = (input_string
                                    .replace(r'"', '') \
                                    .replace("\\",''))
    tup_arr = ast.literal_eval(tuple_strings.replace('{{', '[').replace('}}', ']'))
    return tup_arr


def parse_string_to_tuple_con(word, input_string):
    res = []
    tuple_strings = (input_string
                                    .replace(r'"', '') \
                                    .replace(r'\\"" \\""', "' '")\
                                    .replace('\n', '@@@') \
                                    .replace("\\", "'"))
    parsed_tuple = ast.literal_eval(tuple_strings.replace('{', '[').replace('}', ']'))
    array_of_tuples = list(parsed_tuple)
    for tup in array_of_tuples:
        temp_str = tup[3].replace(r'@@@@@@', '\n\n')\
                         .replace(r'@@@', '\n')\
                         .replace(r'&&&', '"')
        final_word = word + temp_str
        new_tup = tup[:3] + (final_word,)
        res.append(new_tup)
    return res
def parse_string_to_tuple(word, input_string):
    res = []
    tuple_strings = (input_string
                                    .replace(r'"', '') \
                                    .replace(r'\\"" \\""', "' '")\
                                    .replace(r'\\', "'")\
                                    .replace('\n', '@@@') \
                                    .replace(r'\\, \\', ','))
    parsed_tuple = ast.literal_eval(tuple_strings.strip('{}'))
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

    def build_entire_text(self, article_title):
        text_arr = []
        article_id = self.db_handler.get_article_id_from_title(article_title)[0][0]
        self.db_handler.cursor.execute("""SELECT a.article_title, a.date, r.first_name, r.last_name 
                                          FROM art_info.articles a JOIN art_info.reporters r 
                                          ON a.reporter_id = r.reporter_id 
                                          WHERE a.article_id = %s """,
                                         (article_id, ))
        self.db_handler.connection.commit()
        article_title, date_of_issue, rep_f_name, rep_last_name = self.db_handler.cursor.fetchall()[0]
        self.db_handler.cursor.execute( " SELECT word_id, word, unnest(occurrences) "
                                        " FROM text_handle.words, "
                                        " LATERAL unnest(occurrences) AS outer_tuple "
                                        " WHERE (outer_tuple).article_id = %s ",
                                        (article_id, ))
        self.db_handler.connection.commit()
        for row in self.db_handler.cursor:
            tup_arr = parse_string_to_tuple(row[1],row[2])
            text_arr.extend(tup_arr)
        sorted_text_arr = sorted(text_arr, key=lambda x: (x[0], x[1], x[2]))
        final_text = ""
        for tup in sorted_text_arr:
            final_text += f"{tup[3]}"

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

    def build_context(self, article_title, word):
        res =[]
        lines_arr = []
        article_id = self.db_handler.get_article_id_from_title(article_title)[0][0]
        word_id = self.db_handler.get_word_id_from_word(word)[0][0]
        self.db_handler.cursor.execute(" SELECT word, unnest(occurrences) "
                                       " FROM text_handle.words, "
                                       " LATERAL unnest(occurrences) AS outer_tuple "
                                       " WHERE (outer_tuple).article_id = %s and word_id = %s",
                                       (article_id,word_id))
        self.db_handler.connection.commit()

        # Build the text array with tuples
        for row in self.db_handler.cursor:
            tup_arr = parse_string_to_tuple(row[0], row[1])
        for tup in tup_arr:
            line = (tup[0], tup[1])
            lines_arr.append(line)
        for line in lines_arr:
            query = """
                SELECT word_id, word, 
                       ARRAY(
                           SELECT pos
                           FROM unnest((outer_tuple).positions) AS pos
                           WHERE pos.paragraph_number = %s
                           AND pos.line_number IN (%s, %s, %s)
                       ) AS filtered_positions
                FROM text_handle.words,
                     LATERAL unnest(occurrences) AS outer_tuple
                WHERE (outer_tuple).article_id = %s
                  AND EXISTS (
                      SELECT 1
                      FROM unnest((outer_tuple).positions) AS pos
                      WHERE pos.paragraph_number = %s
                      AND pos.line_number IN (%s, %s, %s)
                  )
            """
            self.db_handler.cursor.execute(query, (line[0],line[1]-1,line[1],line[1]+1,
                                                   article_id,line[0],line[1]-1,line[1],line[1]+1))
            self.db_handler.connection.commit()
            result = self.db_handler.cursor.fetchall()
            text_arr = []
            for tup in result:
                tup_arr = parse_string_to_tuple_con(tup[1], tup[2])
                text_arr.extend(tup_arr)
            sorted_text_arr = sorted(text_arr, key=lambda x: (x[0], x[1], x[2]))
            final_context = ""
            for tup in sorted_text_arr:
                final_context += f"{tup[3]}"
            res.append(final_context)
        return res


    # Search for all the articles that contain a specific word.
    # An index is defined as the position of the word in the article.
    # The position consists of the paragraph number, the line number and the position in the line.
    def build_words_index(self, word, article_title):
        word_id = self.db_handler.get_word_id_from_word(word)[0][0]
        article_id = self.db_handler.get_article_id_from_title(article_title)[0][0]
        query = """
            WITH position_aggregation AS (
                SELECT word,
                       occ.article_id,
                       ARRAY_AGG((pos.paragraph_number, pos.line_number, pos.position_in_line)) AS positions
                FROM words,
                     LATERAL unnest(occurrences) AS occ(article_id, positions),
                     LATERAL unnest(occ.positions) AS pos(paragraph_number, line_number, position_in_line, finishing_chars)
                GROUP BY word, occ.article_id
            )
            SELECT word,
                   ARRAY_AGG( positions) AS filtered_occurrences
            FROM position_aggregation
            GROUP BY word;
        """
        self.db_handler.cursor.execute(query)
        self.db_handler.connection.commit()
        res = []
        for row in self.db_handler.cursor:
            index_arr = parse_string_to_tuple_ind(row[1])
            res.append((row[0], index_arr))
        return res















