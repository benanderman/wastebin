from degrading_pastebin import app
import degrading_pastebin.pastebin

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()


