#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import pymysql


from tornado.options import define,options
from tornado.web import url,Application,RequestHandler

define("port",default=8000,help ="run on the given port",type=int)
class IndexHandler(tornado.web.RequestHandler):
    def get(self):

        self.write("<a href='" + self.reverse_url("input_data") + "'>数据输入</a>")
        self.write("<a href='" + self.reverse_url("output_data") + "'>数据输出</a>")
class InputHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("input_data.html")

    def post(self, *args, **kwargs):
        inputdata_BMName = self.get_argument("BMName")
        inputdata_VMName = self.get_argument("VMName")
        inputdata_VMIp= self.get_argument("VMIp")
        inputdata_UpOrDown = self.get_argument("UpOrDown")
        inputdata_Remark = self.get_argument("Remark")

        inputdata_BMNamed = "".join(inputdata_BMName)
        inputdata_VMNamed = "".join(inputdata_VMName)
        inputdata_VMIpd = "".join(inputdata_VMIp)
        inputdata_UpOrDownd = "".join(inputdata_UpOrDown)
        inputdata_Remarkd = "".join(inputdata_Remark)

        conn = pymysql.connect(host="192.168.105.86", port=3306, user="root", password="123456", db="tornadodata")
        cur = conn.cursor()

        ##数据插入数据库
        sql = "insert into inputdata (BMName,VMName,VMIp,UpOrDown,Remark) values ('%s','%s','%s','%s','%s')" %(inputdata_BMNamed,inputdata_VMNamed,inputdata_VMIpd,inputdata_UpOrDownd,inputdata_Remarkd)
        #执行数据库操作
        try:
           cur.execute(sql)
           conn.commit()
           # self.write("添加成功")
           self.redirect("/input_data")
        except:
           conn.rollback()
        cur.close()
        conn.close()
class OutputHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host="192.168.105.86", port=3306, user="root", password="123456", db="tornadodata")
        cur = conn.cursor()
        sql = "select BMName,VMName,VMIp,UpOrDown,Remark from inputdata"
        try:
           cur.execute(sql)
           conn.commit()

           result = cur.fetchall()
           # for reads in result:
           #     print(reads)


           print(result)
           self.write("查询成功")
           #for k in result:
           self.render("output_data.html", Outputdata_BMNamed=result)

           # for row in result:
           #     BMName = row[1]
           # self.render("output_data.html", Outputdata_BMNamed=BMName)
           # print(result)
        except:
           conn.rollback()
        cur.close()
        conn.close()
        # result = cur.fetchall()
        # for row in result:
        #     BMName = row[0]
        # BMNames = "".join(BMName)
        # # self.render("output_data.html",Outputdata_BMNamed=BMNames)
        # print(BMNames)
#模版文件路径声明
setting = dict(template_path = os.path.join(os.path.dirname(__file__),"template"))

application = tornado.web.Application([(r"/",IndexHandler),
                                       url(r"/input_data",InputHandler,name="input_data"),
                                       url(r"/output_data",OutputHandler,name="output_data")
                                       ],**setting)

http_server = tornado.httpserver.HTTPServer(application)

if __name__=="__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


