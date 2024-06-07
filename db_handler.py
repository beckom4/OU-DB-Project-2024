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
        self.cursor.execute(" CREATE TYPE text_handle.position_type as ( line_number INTEGER, "
                            "position_in_line INTEGER); ")
        self.connection.commit()
        self.cursor.execute(" CREATE TYPE text_handle.occurrence_type AS ( magazine_id UUID, volume_id INTEGER, "
                            " article_id INTEGER, positions_array position_type[]); ")
        self.connection.commit()



    # Function to create all the required tables:
    # Magazines, Volumes, Articles, Authors,
    # As part of the creation of the articles table, a new type is created to store the article's pages
    def create_tables(self):
        self.cursor.execute(" CREATE TABLE art_info.Magazines(magazine_id UUID PRIMARY KEY, "
                            " magazine_name TEXT, e_date DATE, location TEXT); ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE art_info.Volumes(magazine_id UUID, volume_id INT, issue_date DATE, "
                            " CONSTRAINT pk_volumes PRIMARY KEY (magazine_id, volume_id), "
                            " CONSTRAINT magazine_id_fk FOREIGN KEY (magazine_id) "
                            " REFERENCES art_info.Magazines (magazine_id)) ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE art_info.Articles( magazine_id UUID, volume_id INT, article_id INT, "
                            " article_title TEXT, page_range INT[] ,author_id INT, "
                            " CONSTRAINT articles_pk PRIMARY KEY (magazine_id, volume_id, article_id), "
                            " CONSTRAINT articles_fk FOREIGN KEY (magazine_id, volume_id) "
                            " REFERENCES art_info.Volumes (magazine_id, volume_id)) ")
        self.connection.commit()
        self.cursor.execute(
            " CREATE TABLE art_info.authors(author_id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT, "
            " date_of_birth DATE, country TEXT) ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE text_handle.words ( word_id SERIAL PRIMARY KEY, "
                            " word TEXT, occurrence occurrence_type[]); ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE text_handle.special_words(group_id SERIAL PRIMARY KEY, "
                            " group_description TEXT, words TEXT[])")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE text_handle.phrases(phrase_id SERIAL PRIMARY KEY, phrase TEXT )")
        self.connection.commit()

    def create_triggers(self):
        # Create a trigger that will automatically increment the volume_id when a new volume is added.
        self.cursor.execute(" CREATE OR REPLACE FUNCTION art_info.generate_volume_id() "
                            " RETURNS TRIGGER AS $$ "
                            " DECLARE "
                            " v_count INTEGER; "
                            " BEGIN "
                            " SELECT COUNT(*) INTO v_count FROM art_info.Volumes "
                            " WHERE magazine_id = NEW.magazine_id; "
                            " NEW.volume_id := v_count + 1; "
                            " RETURN NEW; "
                            " END; "
                            " $$ LANGUAGE plpgsql; "
                            " CREATE TRIGGER trigger_generate_volume_id "
                            " BEFORE INSERT ON art_info.Volumes "
                            " FOR EACH ROW "
                            " EXECUTE FUNCTION art_info.generate_volume_id();")
        self.connection.commit()
        # Create a trigger that will automatically increment the article_id when a new article is added.
        self.cursor.execute(" CREATE OR REPLACE FUNCTION art_info.generate_article_id() "
                            " RETURNS TRIGGER AS $$ "
                            " DECLARE "
                            " a_count INTEGER;"
                            " BEGIN "
                            " SELECT COUNT(*) INTO a_count "
                            " FROM art_info.Articles "
                            " WHERE magazine_id = NEW.magazine_id AND volume_id = NEW.volume_id; "
                            " NEW.article_id := a_count + 1; "
                            " RETURN NEW; "
                            " END; "
                            " $$ LANGUAGE plpgsql; "
                            " CREATE TRIGGER trigger_generate_article_id "
                            " BEFORE INSERT ON art_info.Articles "
                            " FOR EACH ROW "
                            " EXECUTE FUNCTION art_info.generate_article_id();")
        self.connection.commit()

    # Getters:

    # Get author_id from author's name:
    def get_author_id_from_name(self, author_full_name):
        first_name, last_name = parse_name(author_full_name)
        print("first name: ", first_name)
        print("last name: ", last_name)
        self.cursor.execute(" SELECT author_id "
                            " FROM art_info.authors "
                            " WHERE first_name = %s AND last_name = %s ",
                            (first_name,last_name))
        return self.cursor.fetchall()

    # Get magazine_id from magazine_name
    # The assumption is that there are no 2 magazines with the same name.
    def get_magazine_id_from_name(self, magazine_name):
        self.cursor.execute(" SELECT magazine_id "
                            " FROM art_info.magazines "
                            " WHERE magazine_name = %s ",
                            (magazine_name,))
        return self.cursor.fetchall()[0]
