import oracledb


class db_handler:
    def __init__(self):
        # Connect to the database. PLEASE MAKE SURE TO change the  credentials to the ones on your local server.
        self.connection = oracledb.connect(user="system", password="oracle", dsn="192.168.1.112:1521/XEPDB1")
        self.cursor = self.connection.cursor()

    # Function to create all the required tables:
    # Magazines,
    def create_tables(self):
        self.cursor.execute("CREATE TABLE Magazines(magazine_id VARCHAR2(36) DEFAULT RAWTOHEX(SYS_GUID()) PRIMARY KEY,"
                            "magazine_name VARCHAR(50),e_date DATE, location VARCHAR(50))")
        self.cursor.execute("CREATE TABLE Volumes(magazine_id VARCHAR(36), volume_id NUMBER, issue_date DATE,"
                            "CONSTRAINT pk_volumes PRIMARY KEY (magazine_id, volume_id),"
                            "CONSTRAINT magazine_id_fk FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id)")
        self.cursor.execute()

    def create_triggers(self):
        # Create a trigger that will automatically increment the volume_id when a new volume is added.
        self.cursor.execute("CREATE OR REPLACE TRIGGER generate_volume_id"
                            "BEFORE INSERT ON volumes"
                            "FOR EACH ROW"
                            "DECLARE"
                                "counter NUMBER;"
                            "BEGIN"
                                "SELECT count(magazine_id)"
                                "INTO counter"
                                "FROM volumes"
                                "WHERE magazine_id = :NEW.magazine_id;"                       
                                ":NEW.volume_id := counter + 1;"
                            "END;"
                            "/")




