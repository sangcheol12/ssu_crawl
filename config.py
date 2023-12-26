import pymysql

class Post:
    def __init__(self, url, title, start_date, end_date, summary, content):
        self.url = url
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.summary = summary
        self.content = content

mydb = pymysql.connect(
  host="127.0.0.1",
  user="admin",
  password="비밀번호",
  db="디비명",
  charset="utf8"
)