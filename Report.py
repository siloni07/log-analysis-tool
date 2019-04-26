#!/usr/bin/env python3
# 
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for

from Reportdb import get_article,get_author,get_percent

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis Tool</title>
    <style>
      h1 { text-align: center; }
      form { border : 1px solid #999;}
      div.article { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      div.author { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      div.percent { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
     
      
    </style>
  </head>
  <body>
    <h1>Log Analysis Tool</h1>
    <form method=get>
    <!-- post content will go here -->
        <div class=article>The most popular three articles of all time
            <ul>
                %s
            </ul>
        </div>
        <div class=author>The most popular articles author of all time
            <ul>
                %s
            </ul>
        </div>
        <div class=percent>On which days did more than 1 perc of requests lead to errors?
            <ul>
                %s
            </ul>
        </div>
    </form>
    
  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
            <li>%s -- %s</li>
'''
AUTHOR = '''\
            <li>%s -- %s</li>
'''
PERCENT = '''\
            <li>%s -- %s</li>
'''


@app.route('/', methods=['GET'])
def main():
  '''Main page of the forum.'''
  posts = "".join(POST % (text1, text2) for text1, text2 in get_article())
  authors = "".join(AUTHOR % (text1, text2) for text1, text2 in get_author())
  percent = "".join(PERCENT % (text1, text2) for text1, text2 in get_percent())
  html = HTML_WRAP % (posts,authors,percent)
  return html


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)

