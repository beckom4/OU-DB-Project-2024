import psycopg2


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


class DB_handler:
    def __init__(self):
        # Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
        self.connection = psycopg2.connect(dbname="db_project", user="omri", password="omri",
                                           options="-c search_path=text_handle")
        self.cursor = self.connection.cursor()

    def create_schemas(self):
        self.cursor.execute(" CREATE SCHEMA IF NOT EXISTS art_info; ")
        self.connection.commit()
        self.cursor.execute(" CREATE SCHEMA IF NOT EXISTS text_handle; ")
        self.connection.commit()

    def create_types(self):
        self.cursor.execute("""
            CREATE TYPE position_type AS (paragraph_number INTEGER, line_number INTEGER, position_in_line INTEGER, 
                                        finishing_chars varchar(10));
            CREATE TYPE occurrence_type AS (
                article_id INTEGER,
                positions position_type[]
            );
        """)
        self.connection.commit()

        # Function to create all the required tables:

    # Magazines, Volumes, Articles, Reporters,
    # As part of the creation of the articles table, a new type is created to store the article's pages
    def create_tables(self):
        self.cursor.execute(" CREATE TABLE art_info.Newspapers(np_id UUID PRIMARY KEY, np_name TEXT) ")
        self.connection.commit()
        self.cursor.execute("""
                            CREATE TABLE art_info.Articles( article_id SERIAL PRIMARY KEY, article_title TEXT, 
                            date DATE ,reporter_id INT, np_id UUID,
                            CONSTRAINT articles_fk FOREIGN KEY (np_id)
                            REFERENCES art_info.Newspapers (np_id));
                            """)
        self.connection.commit()
        self.cursor.execute(
            " CREATE TABLE art_info.reporters(reporter_id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT) ")
        self.connection.commit()
        self.cursor.execute(""" CREATE TABLE text_handle.words ( word_id SERIAL PRIMARY KEY, 
                                word TEXT, occurrences occurrence_type[]); """)
        self.connection.commit()
        self.cursor.execute(""" CREATE TABLE text_handle.word_groups(group_id SERIAL PRIMARY KEY, 
                             group_description TEXT, word_ids INTEGER[]); """)
        self.connection.commit()
        # self.cursor.execute(" CREATE TABLE text_handle.phrases(phrase_id SERIAL PRIMARY KEY, phrase TEXT )")
        # self.connection.commit()

    # def create_triggers(self):
    # Create a trigger that will automatically increment the volume_id when a new volume is added.
    # self.cursor.execute(" CREATE OR REPLACE FUNCTION art_info.generate_volume_id() "
    #                     " RETURNS TRIGGER AS $$ "
    #                     " DECLARE "
    #                     " v_count INTEGER; "
    #                     " BEGIN "
    #                     " SELECT COUNT(*) INTO v_count FROM art_info.Volumes "
    #                     " WHERE magazine_id = NEW.magazine_id; "
    #                     " NEW.volume_id := v_count + 1; "
    #                     " RETURN NEW; "
    #                     " END; "
    #                     " $$ LANGUAGE plpgsql; "
    #                     " CREATE TRIGGER trigger_generate_volume_id "
    #                     " BEFORE INSERT ON art_info.Volumes "
    #                     " FOR EACH ROW "
    #                     " EXECUTE FUNCTION art_info.generate_volume_id();")
    # self.connection.commit()
    # Create a trigger that will automatically increment the article_id when a new article is added.
    # self.cursor.execute(" CREATE OR REPLACE FUNCTION art_info.generate_article_id() "
    #                     " RETURNS TRIGGER AS $$ "
    #                     " DECLARE "
    #                     " a_count INTEGER;"
    #                     " BEGIN "
    #                     " SELECT COUNT(*) INTO a_count "
    #                     " FROM art_info.Articles "
    #                     " WHERE magazine_id = NEW.magazine_id AND volume_id = NEW.volume_id; "
    #                     " NEW.article_id := a_count + 1; "
    #                     " RETURN NEW; "
    #                     " END; "
    #                     " $$ LANGUAGE plpgsql; "
    #                     " CREATE TRIGGER trigger_generate_article_id "
    #                     " BEFORE INSERT ON art_info.Articles "
    #                     " FOR EACH ROW "
    #                     " EXECUTE FUNCTION art_info.generate_article_id();")
    # self.connection.commit()

    # Getters:

    # Get reporter_id from reporter's name:
    def get_reporter_id_from_name(self, reporter_full_name):
        first_name, last_name = parse_name(reporter_full_name)
        self.cursor.execute(" SELECT reporter_id "
                            " FROM art_info.reporters "
                            " WHERE LOWER(first_name)=LOWER(%s) AND LOWER(last_name) = lower(%s) ",
                            (first_name, last_name))
        return self.cursor.fetchall()

    # Get np_id from np_name
    # The assumption is that there are no 2 newspapers with the same name.
    def get_np_id_from_name(self, np_name):
        self.cursor.execute(" SELECT np_id "
                            " FROM art_info.Newspapers "
                            " WHERE np_name = %s ",
                            (np_name,))
        return self.cursor.fetchall()

    def get_word_id_from_word(self, word):
        self.cursor.execute(" SELECT word_id "
                            " FROM text_handle.words "
                            " WHERE word = %s ",
                            (word,))
        return self.cursor.fetchall()

    def get_article_id_from_title(self, article_title):
        self.cursor.execute(" SELECT article_id "
                            " FROM art_info.articles "
                            " WHERE article_title = %s ",
                            (article_title,))
        return self.cursor.fetchall()


