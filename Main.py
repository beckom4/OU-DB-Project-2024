from Database import Database
from StreamlitUI import StreamlitUI

class Main:
    def __init__(self):
        self.database = Database()
        self.ui = StreamlitUI(self.database)

    def run(self):
        self.ui.run()



if __name__ == "__main__":
    app = Main()
    app.run()
