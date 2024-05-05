import psycopg2


class DB_handler:
    def __init__(self):
        # Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
        self.connection = psycopg2.connect(dbname="db_project", user="omri", password="omri",
                                           options="-c search_path=m_text")
        self.cursor = self.connection.cursor()

    #

    def create_types(self):
        self.cursor.execute(" create type position_type as ( line_number INTEGER, position_in_line INTEGER); ")
        self.connection.commit()
        self.cursor.execute(" CREATE TYPE occurence_type AS ( magazine_id UUID, volume_id INTEGER, "
                                                            " article_id INTEGER, positions_array position_type[]); ")
        self.connection.commit()

    # Function to create all the required tables:
    # Magazines, Volumes, Articles, Authors,
    # As part of the creation of the articles table, a new type is created to store the article's pages
    def create_tables(self):
        self.cursor.execute(" CREATE TABLE m_text.Magazines(magazine_id UUID PRIMARY KEY, "
                            " magazine_name TEXT, e_date DATE, location TEXT); ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE m_text.Volumes(magazine_id UUID, volume_id INT, issue_date DATE, "
					        " CONSTRAINT pk_volumes PRIMARY KEY (magazine_id, volume_id), "
					        " CONSTRAINT magazine_id_fk FOREIGN KEY (magazine_id) "
                            " REFERENCES m_text.Magazines (magazine_id)) ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE m_text.Articles( magazine_id UUID, volume_id INT, article_id INT, "
                            " article_title TEXT, page_range INT[] ,author_id INT, "
                            " CONSTRAINT articles_pk PRIMARY KEY (magazine_id, volume_id, article_id), "
                            " CONSTRAINT articles_fk FOREIGN KEY (magazine_id, volume_id) "
                            " REFERENCES m_text.Volumes (magazine_id, volume_id)) ")
        self.connection.commit()
        # Create a sequence to automatically generate a serial author_id
        self.cursor.execute(" CREATE TABLE m_text.authors(author_id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT, "
                            " date_of_birth DATE, country TEXT) ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE m_text.words ( word_id SERIAL PRIMARY KEY, "
                                                        " word TEXT, occurence occurence_type); ")
        self.connection.commit()
        self.cursor.execute(" CREATE TABLE user_input.special_words(group_id SERIAL PRIMARY KEY, "
                            " group_description TEXT, words TEXT[])")
        self.connection.commit()

    def create_triggers(self):
        # Create a trigger that will automatically increment the volume_id when a new volume is added.
        self.cursor.execute(" CREATE OR REPLACE FUNCTION m_text.generate_volume_id() "
                            " RETURNS TRIGGER AS $$ "
                            " DECLARE "
                                " v_count INTEGER; "
                            " BEGIN "
                                " SELECT COUNT(*) INTO v_count FROM Volumes WHERE magazine_id = NEW.magazine_id; "
                                " NEW.volume_id := v_count + 1; "
                                " RETURN NEW; "
                            " END; "
                            " $$ LANGUAGE plpgsql; "
                            " CREATE TRIGGER trigger_generate_volume_id "
                            " BEFORE INSERT ON m_text.Volumes "
                            " FOR EACH ROW "
                            " EXECUTE FUNCTION generate_volume_id();")
        self.connection.commit()
        # Create a trigger that will automatically increment the article_id when a new article is added.
        self.cursor.execute(" CREATE OR REPLACE FUNCTION m_text.generate_article_id() "
                            " RETURNS TRIGGER AS $$ "
                            " DECLARE "
                                " a_count INTEGER;" 
                            " BEGIN "
                                " SELECT COUNT(*) INTO a_count " 
                                " FROM Articles " 
                                " WHERE magazine_id = NEW.magazine_id AND volume_id = NEW.volume_id; "
                                " NEW.article_id := a_count + 1; "
                                " RETURN NEW; "
                            " END; "
                            " $$ LANGUAGE plpgsql; "
                            " CREATE TRIGGER trigger_generate_article_id "
                            " BEFORE INSERT ON m_text.Articles "
                            " FOR EACH ROW "
                            " EXECUTE FUNCTION generate_article_id();")
        self.connection.commit()

