from server.config import DBPATH
from server.app import App


if __name__ == '__main__':
    app = App(DBPATH)
    app.run()
