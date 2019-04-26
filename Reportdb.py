# "Database code" for the DB Forum.


import psycopg2


#POSTS = [("This is the first post.", datetime.datetime.now())]
DBNAME ="news"
def get_article():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c=db.cursor()
  c.execute("select a.title, count(l.id)||' views' from articles_view a, log l where substring(l.path,10) like a.match and l.status='200 OK' group by a.title order by count(l.id) desc limit 3")
  db.close
  return c.fetchall()
  
def get_author():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select aa.name,count(l.id)||' views' from articles_view a inner join log l on substring(l.path,10) like a.match left outer join authors aa on aa.id=a.author group by aa.name,l.status having l.status='200 OK' order by count(l.id) desc")
  db.close
  return c.fetchall()

def get_percent():
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select to_char(a.time2,'dd/Mon/yyyy'),a.percent||' % errors' from (select round((x.num404::DECIMAL/y.num)*100,2) as percent,y.time2 from(select date(time) as time1,count(*) as num404 from log group by date(time),status having status='404 NOT FOUND') x join (select date(time) as time2,count(*) as num from log group by date(time)) y on x.time1=y.time2) as a where a.percent >1")
  db.close
  return c.fetchall()



