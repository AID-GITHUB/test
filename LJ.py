"""链家数据"""
import requests
import re
import pymysql
import warnings

class LianjiaSpider:
    def __init__(self):
        self.baseurl="https://xa.lianjia.com/ershoufang/pg"
        self.page=1
        self.headers={"User-Agent":"Mozilla/5.0"}
        self.proxies={'http':"http://47.94.200.124:3128"}
        self.db=pymysql.connect("localhost","root","123456",charset="utf8")
        self.cursor=self.db.cursor()

    #抓取页面代码
    def getPage(self,url):
        res=requests.get(url,proxies=self.proxies,headers=self.headers,timeout=5)
        res.encoding="utf-8"
        html=res.text
        self.parsePage(html)

    #解析
    def parsePage(self,html):
        p=re.compile('<div class="positionInfo">.*?class="no_resblock_a">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>.*?<div class="unitPrice".*?<span>(.*?)</span></div>',re.S)
        r_list=p.findall(html)
        self.writetToMysql(r_list)


    # 存入Mysql数据库
    def writetToMysql(self,r_list):
        c_db="create database if not exists Lianjiadb default charset=utf8"
        u_db="use Lianjiadb"
        c_tab="create table if not exists housePrice(id int primary key auto_increment,housename varchar(50),houseprice int)charset=utf8"
        warnings.filterwarnings("ignore")
        try:
            self.cursor.execute(c_db)
            self.cursor.execute(u_db)
            self.cursor.execute(c_tab)
        except Warning:
            pass
        ins="insert into housePrice(housename,houseprice)values (%s,%s)"
        for r_tuple in r_list:
            name=r_tuple[0].strip()
            price=float(r_tuple[1].strip())*10000
            #average=r_tuple[2].strip()
            L=[name,price]
            self.cursor.execute(ins,L)
            self.db.commit()

    #提示
    def workOn(self):
        while True:
            c=input("爬取按y(q退出):")
            if  c.strip().lower()=="y":
                url=self.baseurl+str(self.page)+"/"
                self.getPage(url)
                self.page+=1
            else:
                print("爬取结束，谢谢使用")
                break


if __name__=="__main__":
    spider=LianjiaSpider()
    spider.workOn()