#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
from os import path


def crawl_category(URL):
    urls = []
    headers = {"User-Agent":
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    li = str(soup.find_all(id="double"))
    split = li.split('\"')
    for i  in range(len(split)):
        if 'href=' in split[i]:
                urls.append(split[i + 1])
    return urls

def read_file(category_url):
    file = open(category_url, "r").read()
    return file.split("\n")

def write_in_file(cat):   
    file = open("url.txt", "a")
    for i in range(len(cat)):
        file.write(cat[i])
        file.write('\n')

def crawl():
    if not(path.exists("category.txt")):
        print("Need category.txt")
        exit()
    category_url = read_file("category.txt")
    for i in range(len(category_url)):
         if 'https://www.bureau-vallee.fr/' in category_url[i]:
            print("Category URL:", category_url[i])
            cat = crawl_category(category_url[i])
            write_in_file(cat)

def parse_number_of_product(URL):
    count = 0
    headers = {"User-Agent":
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    li = str(soup.body).split('<span>')
    for i in range(len(li)):
        if '="amount"' in li[i]:
            count = int((li[i + 1]).split('</span>')[0])
            break
    return count

def main():
    count = 0
    crawl()
    category_url = read_file("url.txt")
    for i in range(len(category_url)):
        if 'https://www.bureau-vallee.fr/' in category_url[i]:
            print("Category URL:", category_url[i])
            count = count + parse_number_of_product(category_url[i])
    print(count)

if __name__ == "__main__":
    main()