import requests
from pprint import pprint
import time
from bs4 import BeautifulSoup
import multiprocessing
from functools import partial
from config import mydb
#from config import Post
import copy

class Post:
    def __init__(self, url, title, start_date, end_date, summary, content):
        self.url = url
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.summary = summary
        self.content = content

def crawl_notice_detail(total_post_lst, sub_url):
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#contents > div > div.vc_row.wpb_row.vc_row-fluid > div > div > div > div > div.col-12.col-lg-9.col-xl-10 > div.bg-white.p-4.mb-5 > h2')
    write_date = soup.select_one('#contents > div > div.vc_row.wpb_row.vc_row-fluid > div > div > div > div > div.col-12.col-lg-9.col-xl-10 > div.bg-white.p-4.mb-5 > div.clearfix > div.float-left.mr-4')
    end_date = None
    #summary = soup.select_one('#ModuleEcoProgramView > div:nth-child(1) > div > div:nth-child(3) > div.abstract.open > div > div.text').text
    summary = None
    content_body = soup.select('#contents > div > div.vc_row.wpb_row.vc_row-fluid > div > div > div > div > div.col-12.col-lg-9.col-xl-10 > div.bg-white.p-4.mb-5 > div:nth-child(5) p')
    content = ''
    title = title.text if title else None
    write_date = write_date.text if write_date else None
    for i in content_body:
        content += i.text
        content += '\n'
    print(content)
    #post = Post(sub_url,title,write_date,end_date,summary,content)
    #total_post_lst[sub_url] = post
    
def crawl_notice_page(total_post_lst, sub_url):
    cnt=0
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    a_tags = soup.select('#contents > div > div.vc_row.wpb_row.vc_row-fluid > div > div > div > div:nth-child(2) > div > ul a')
    if len(a_tags) == 0:
        return 1
    
    for a_tag in a_tags:
        href = sub_url + a_tag.get("href")
        if href in total_post_lst.keys():
            continue
        if href and href.startswith(""):
            #print(href)
            crawl_notice_detail(total_post_lst, href)
            cnt+=1
    if not cnt:
        return 1
    return 0

def crawl_notice_main(total_post_lst, idx):
    start_url = 'https://scatch.ssu.ac.kr/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD/'
    url_option = '?sort=date'
    while True:
        url = start_url+str(idx)+url_option
        
        if crawl_notice_page(total_post_lst, url):
            break
        idx += 3

def save_data(total_post_lst):
    cursor = mydb.cursor()
    sql = "INSERT INTO post (url, title, start_date, end_date, summary, content) VALUES (%s, %s, %s, %s, %s, %s)"
    for key, post in total_post_lst.items():
        data = (post.url, post.title, post.start_date, post.end_date, post.summary, post.content)
        cursor.execute(sql, data)
    mydb.commit()
    cursor.close()
    mydb.close()

def fetch_data(post_dict):
    cursor = mydb.cursor()
    sql = "SELECT * FROM post"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    for row in result:
        url = row[0]
        title = row[1]
        start_date = row[2]
        end_date = row[3]
        summary = row[4]
        content = row[5]

        post = Post(url, title, start_date, end_date, summary, content)
        post_dict[url] = post
        
def remove_previous_data(total_post, prev_post):
    for key in prev_post.keys():
        if key in total_post:
            del total_post[key]

if __name__ == "__main__":
    start_time = time.time()
    idx_values = [1, 2, 3]
    total_post = multiprocessing.Manager().dict()
    #fetch_data(total_post)
    #pprint(total_post.keys())
    prev_post = copy.deepcopy(total_post)
    pool = multiprocessing.Pool(processes=3)
    f1 = partial(crawl_notice_main, total_post)
    pool.map(f1, idx_values)
    pool.close()
    pool.join()
    #remove_previous_data(total_post, prev_post)
    #save_data(total_post)
    res = list(total_post.values())
    print(time.time()-start_time)

#contents > div > div.vc_row.wpb_row.vc_row-fluid > div > div > div > div:nth-child(2) > div > ul