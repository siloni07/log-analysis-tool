#!/usr/bin/env python2
#
# A buggy web service in need of a database.

# "Database code" for the DB Forum.

import psycopg2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


DBNAME = "news"


def get_article():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select a.title,count(l.id) as views
                    from articles a, log_view l
                    where
                    l.path_new =a.slug and l.status='200 OK'
                    group by a.title order by count(l.id) desc limit 3""")
    db.close
    return c.fetchall()


def get_author():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select aa.name,count(l.id)
                    from articles a inner join log_view l
                    on l.path_new=a.slug
                    left outer join authors aa
                    on aa.id=a.author
                    group by aa.name,l.status
                    having l.status='200 OK'
                    order by count(l.id) desc""")
    db.close
    return c.fetchall()


def get_percent():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select to_char(a.time2,'dd/Mon/yyyy'),a.percent
                    from (
                        select
                        round((x.num404::DECIMAL/y.num)*100,2) as percent,
                    y.time2
                    from(
                        select date(time) as time1,count(*) as num404
                        from log
                        group by date(time),status
                        having status='404 NOT FOUND') x
                        join (
                            select date(time) as time2,count(*) as num
                            from log
                            group by date(time)) y
                            on x.time1=y.time2) as a
                            where a.percent >1""")
    db.close
    return c.fetchall()


class MessageHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        '''Main page of the forum.'''
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        article = get_article()
        author = get_author()
        percent = get_percent()
        output = "#What are the most popular three articles of all time?"
        output += "\n-->"
        output += "\n-->".join("{} : {} views".format(title, views)
                               for (title, views) in article)
        output += "\n\n# Who are most popular article authors of all time?"
        output += "\n-->"
        output += "\n-->".join("{} : {} views".format(title, views)
                               for (title, views) in author)

        output += "\n\n#On which day did more than 1% requests lead errors?"
        output += "\n-->"
        output += "\n-->".join("{} : {} % errors".format(date, error)
                               for (date, error) in percent)
        print(output)
        with open("Output.txt", "w") as myFile:
            myFile.write(
                "# What are the most popular three articles of all time?\n")
            myFile.write("\n".join("{} - {} views".format(title, views)
                                   for (title, views) in article))
            myFile.write(
                "\n# Who are the most popular article authors of all time?\n")
            myFile.write("\n".join("{} - {} views".format(title, views)
                                   for (title, views) in author))
            myFile.write(
                """\n# On which days did more than 1% of requests lead to errors?
                    \n""")
            myFile.write("\n".join("{} - {} % errors".format(date, error)
                                   for (date, error) in percent))

        self.wfile.write(output.encode())


def main():
    try:
        port = 8000
        server_address = ('', port)
        httpd = HTTPServer(server_address, MessageHandler)
        print("Web Server start running on port %s" % port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server")
        httpd.socket.close()


if __name__ == '__main__':
    main()
