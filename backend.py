import os
import sqlite3
import wsgiref.simple_server

from werkzeug.wrappers import Request, Response

port = 8000

class LogCommandAttempts(object):
    def __init__(self, dbname="test.db"):
        init_db = not os.path.exists(dbname)
        self.conn = sqlite3.connect(dbname)
        if init_db:
            c = self.conn.cursor()
            c.execute("CREATE TABLE session (ip TEXT)")
            c.execute("CREATE TABLE mesg (session INTEGER, date TEXT, cmd TEXT)")
            self.conn.commit()

    def __call__(self, environ, start_response):
        cursor = self.conn.cursor()
        request = Request(environ)
        response = Response()

        # Create a session if it isn't there
        if "session" not in request.cookies:
            cursor.execute("INSERT INTO session VALUES (?)", (
                request.form.get('ip', 'Unknown'),
            ))
            response.set_cookie("session", str(cursor.lastrowid))
            session = cursor.lastrowid
        else:
            session = int(request.cookies["session"])

        # Log a message
        if "cmd" in request.form and "timestamp" in request.form:
            cursor.execute("INSERT INTO mesg VALUES (?, ?, ?)", (
                session,
                request.form["timestamp"],
                request.form["cmd"]
            ))
        
        self.conn.commit()
        return response(environ, start_response)

if __name__ == "__main__":
    app = LogCommandAttempts()
    httpd = wsgiref.simple_server.make_server('0.0.0.0', port, app)
    print("Serving on port {}".format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Caught Ctrl-C. Shutting down.")
        app.conn.close()
