import oracledb


class DB_handler:
    def __init__(self):
        # Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
        self.connection = oracledb.connect(user="system", password="oracle", dsn="192.168.1.112:1521/XEPDB1")
        self.cursor = self.connection.cursor()

    # Function to create all the required tables:
    # Magazines, Volumes, Articles, Authors,
    # As part of the creation of the articles table, a new type is created to store the article's pages
    def create_tables(self):
        self.cursor.execute(" CREATE TABLE Magazines(magazine_id VARCHAR2(36) DEFAULT RAWTOHEX(SYS_GUID()) PRIMARY KEY,"
                            " magazine_name VARCHAR(50),e_date DATE, location VARCHAR(50))")
        self.cursor.execute(" CREATE TABLE Volumes(magazine_id VARCHAR2(36), volume_id INTEGER, issue_date DATE,"
                            " CONSTRAINT pk_volumes PRIMARY KEY (magazine_id, volume_id),"
                            " CONSTRAINT magazine_id_fk FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id))")
        self.cursor.execute(" CREATE OR REPLACE TYPE page_range_type AS TABLE OF INTEGER")
        self.cursor.execute(" CREATE TABLE Articles( magazine_id VARCHAR(36), volume_id NUMBER, article_id NUMBER," 
                            " article_title VARCHAR(100), page_range page_range_type,author_id NUMBER, "
					        " CONSTRAINT articles_pk PRIMARY KEY (magazine_id, volume_id, article_id), "
					        " CONSTRAINT articles_fk FOREIGN KEY (magazine_id, volume_id) "
                            " REFERENCES Volumes (magazine_id, volume_id) "
					        " )NESTED TABLE page_range STORE AS article_page_ranges")
        # Create a sequence to automatically generate a serial author_id
        self.cursor.execute(" CREATE SEQUENCE author_id_seq START WITH 1 INCREMENT BY 1 NOMAXVALUE ")
        self.cursor.execute(" CREATE TABLE authors(author_id INTEGER, first_name VARCHAR2(30), last_name VARCHAR(30), "
                            " date_of_birth DATE, country VARCHAR2(30), "
					        " CONSTRAINT authors_pk PRIMARY KEY (author_id)) ")
    def create_triggers(self):
        # Create a trigger that will automatically increment the volume_id when a new volume is added.
        self.cursor.execute(" CREATE OR REPLACE TRIGGER generate_volume_id" 
                            " BEFORE INSERT ON Volumes"  
                            " FOR EACH ROW"
                            " DECLARE"
                            " v_count INTEGER;"
                            " BEGIN"
                                " SELECT COUNT(*) INTO v_count FROM Volumes WHERE magazine_id = :NEW.magazine_id;"
                                " :NEW.volume_id := v_count + 1;"
                            " END;")
        # Create a trigger that will automatically increment the article_id when a new article is added.
        self.cursor.execute(" CREATE OR REPLACE TRIGGER generate_article_id "
                            " BEFORE INSERT ON Articles "
                            " FOR EACH ROW "
                            " DECLARE "
                                " a_count INTEGER; "
                            " BEGIN "
	                            " SELECT COUNT(*) INTO a_count " 
                                " FROM Articles " 
                                " WHERE magazine_id = :NEW.magazine_id AND volume_id = :NEW.volume_id; "
                                " :NEW.article_id := a_count + 1; "
                            " END;")
        # create a trigger that will automatically generate a new serial author_id
        self.cursor.execute(" CREATE OR REPLACE TRIGGER generate_author_id "
                            " BEFORE INSERT ON authors "
                            " FOR EACH ROW "
                            " BEGIN "
                                " SELECT author_id_seq.NEXTVAL INTO :NEW.author_id FROM dual; "
                            " END;")
