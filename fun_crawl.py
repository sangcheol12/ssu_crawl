import requests
from pprint import pprint
import time
from bs4 import BeautifulSoup
import multiprocessing
from functools import partial
from config import mydb
import copy

url = 'https://fun.ssu.ac.kr'

class Post:
    def __init__(self, url, title, start_date, end_date, summary, content):
        self.url = url
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.summary = summary
        self.content = content

def crawl_youtube_detail(total_post_lst, sub_url):
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#ModuleBoardunivView > article > div.header > div.title > h5').text
    write_date = soup.select_one('#ModuleBoardunivView > article > div.header > div.title > div > ul > li.date > time').text
    end_date = None
    summary = None
    content_body = soup.select('#ModuleBoardunivView > article > div.content > div p')
    content = ''
    for i in content_body:
        content += i.text
        content += '\n'
    post = Post(sub_url,title,write_date,end_date,summary,content)
    total_post_lst[sub_url] = post
    #print(title[0].text)
    #print(write_date[0].text)
    #print(content)

def crawl_youtube_page(total_post_lst, sub_url):
    cnt=0
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    a_tags = soup.select('#ModuleBoardunivListForm > div.list > ul a')
    if len(a_tags) == 0:
        return 1
    
    for a_tag in a_tags:
        href = url + a_tag.get("href")
        if href in total_post_lst.keys():
            continue
        if href and href.startswith("https://fun.ssu.ac.kr/ko/notige2/youtube/view/"):
            crawl_youtube_detail(total_post_lst, href)
            cnt+=1
    if not cnt:
        return 1
    return 0

def crawl_youtube_main(total_post_lst, idx):
    start_url = 'https://fun.ssu.ac.kr/ko/notige2/youtube/list/'
    while True:
        url = start_url+str(idx)
        if crawl_youtube_page(total_post_lst, url):
            break
        print(idx)
        idx+=3

def crawl_contest_detail(total_post_lst, sub_url):
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#ModuleBoardunivView > article > div.header > div.title > h5').text
    write_date = soup.select_one('#ModuleBoardunivView > article > div.header > div.title > div > ul > li.date > time').text
    end_date = None
    summary = None
    content_body = soup.select('#ModuleBoardunivView > article > div.content > div p')
    content = ''
    for i in content_body:
        content += i.text
        content += '\n'
    post = Post(sub_url,title,write_date,end_date,summary,content)
    total_post_lst[sub_url] = post
    

def crawl_contest_page(total_post_lst, sub_url):
    cnt=0
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    a_tags = soup.select('#ModuleBoardunivListForm > div.list > ul a')
    if len(a_tags) == 0:
        return 1
    
    for a_tag in a_tags:
        href = url + a_tag.get("href")
        if href in total_post_lst.keys():
            continue
        if href and href.startswith("https://fun.ssu.ac.kr/ko/notige2/info/view/"):
            crawl_contest_detail(total_post_lst, href)
            cnt+=1
    if not cnt:
        return 1
    return 0

def crawl_contest_main(total_post_lst, idx):
    start_url = 'https://fun.ssu.ac.kr/ko/notige2/info/list/'
    while True:
        url = start_url+str(idx)
        
        if crawl_contest_page(total_post_lst, url):
            break
        idx+=3

def crawl_program_detail(total_post_lst, sub_url):
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#ModuleEcoProgramView > div:nth-child(1) > div > div:nth-child(2) > div > h4')
    write_date = soup.select_one('#ModuleEcoProgramView > div:nth-child(1) > div > div:nth-child(4) > div.form > div:nth-child(1) > form > ul > li > div > label > p:nth-child(4) > time:nth-child(2)')
    end_date = soup.select_one('#ModuleEcoProgramView > div:nth-child(1) > div > div:nth-child(4) > div.form > div:nth-child(1) > form > ul > li > div > label > p:nth-child(4) > time:nth-child(3)')
    #summary = soup.select_one('#ModuleEcoProgramView > div:nth-child(1) > div > div:nth-child(3) > div.abstract.open > div > div.text').text
    summary = None
    content_body = soup.select('#ModuleEcoProgramView > div.context > div.description > div:nth-child(1) p')
    content = ''
    title = title.text if title else None
    write_date = write_date.text if write_date else None
    end_date = end_date.text if end_date else None
    for i in content_body:
        content += i.text
        content += '\n'
    post = Post(sub_url,title,write_date,end_date,summary,content)
    total_post_lst[sub_url] = post
    
def crawl_program_page(total_post_lst, sub_url):
    cnt=0
    response = requests.get(sub_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    a_tags = soup.select('body > div:nth-child(2) > main > div > div a')
    if len(a_tags) == 0:
        return 1
    
    for a_tag in a_tags:
        href = url + a_tag.get("href")
        if href in total_post_lst.keys():
            continue
        if href and href.startswith("https://fun.ssu.ac.kr/ko/program/all/view/"):
            crawl_program_detail(total_post_lst, href)
            cnt+=1
    if not cnt:
        return 1
    return 0

def crawl_program_main(total_post_lst, idx):
    start_url = 'https://fun.ssu.ac.kr/ko/program/all/list/all/'
    url_option = '?sort=date'
    while True:
        url = start_url+str(idx)+url_option
        
        if crawl_program_page(total_post_lst, url):
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
    fetch_data(total_post)
    pprint(total_post.keys())
    prev_post = copy.deepcopy(total_post)
    pool = multiprocessing.Pool(processes=3)
    f1 = partial(crawl_program_main, total_post)
    pool.map(f1, idx_values)
    f2 = partial(crawl_contest_main, total_post)
    pool.map(f2, idx_values)
    f3 = partial(crawl_youtube_main, total_post)
    pool.map(f3, idx_values)
    pool.close()
    pool.join()
    remove_previous_data(total_post, prev_post)
    save_data(total_post)
    res = list(total_post.values())
    print(time.time()-start_time)
