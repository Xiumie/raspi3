#!/usr/bin/env python
#-*-coding:utf-8-*-
import urlparse, string
import urllib, urllib2, os, re
import requests
from bs4 import BeautifulSoup

def url_open(url):
    request = urllib2.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    })
    response = urllib2.urlopen(request)
    pageCode = response.read().decode('gbk')
    return pageCode

def get_downloadurl(pageCode):
    urls = []
    soup = BeautifulSoup(pageCode, 'html.parser')
    div1 = soup.find('div', class_='image-mz')
    div2 = div1.find('div', class_='tzpic3-mzindex')
    lis = div2.find_all('li') 
    for li in lis:
        data = {}
        da = li.find('a')
        url = da['href']
        ti = da['title']
        data['href'] = url
        data['title'] = ti
        urls.append(data)
    return urls

def get_url(pageCode, num):
    soup = BeautifulSoup(pageCode, 'html.parser')
    tem = soup.find('div', class_='arpic')
    link = tem.find('li')
    li = link.find('a')
    img = link.find('img')
    new_img = img['src']
    if num == 1:
        div = soup.find('div', class_='arfy')
        ul = div.find('ul', class_='jogger2')
        li = ul.li.a.text
        pattern = re.compile(r'.*?(\d+).*')
        res = re.findall(pattern, li)
        num = int(res[0])
        # print num
        return new_img, num
    
    return new_img

def download_cl(folder = '/mnt/udisk/youmzi/meizi'):               #主程序
    main_urls = 'http://www.youmzi.com/xg/list_10.html'
    for m in range(3, 91):
        try:
            strm = '_' + str(m) + '.html'
            main_url = main_urls.replace('.html', strm)
            pageCode = url_open(main_url)
            urls = get_downloadurl(pageCode)
            for url in urls:
                try:
                    print url['title']
                    files = folder+'/'+url['title']
                    try:
                        if not os.path.isdir(files):
                            # print u'创建'+files
                            os.mkdir(files)
                        else:
                            continue
                    except:
                        print u'创建错误'
                        continue
                    pageCode = url_open(url['href'])
                    new_img, num = get_url(pageCode, 1)
                    # print new_img, num
                    for n in range(2, num+1):
                        sr = '_' + str(n) + '.html'
                        p_url = url['href'].replace('.html', sr)
                        # print p_url
                        if new_img is not None:
                            filename = files+'/'+new_img.split('/')[-1]
                            if not os.path.isfile(filename):
                                # print u'正在下载'+filename
                                urllib.urlretrieve(new_img, filename)
                        
                        pageCode = url_open(p_url)
                        new_img = get_url(pageCode, 0)
                except:
                    print url['title'] + ' err'
                    continue
        except:
            print str(m) + ' err'
            continue


if __name__ == '__main__':
    download_cl()
