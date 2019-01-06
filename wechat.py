# coding=utf-8

import itchat
import  mysqldemo



# for str in rst:
#     print str[0].decode('utf-8'), '-----', str[1].decode('utf-8')
#itchat.auto_login(hotReload=True)
sqlopt = mysqldemo.mysqldemo(host='127.0.0.1', port=3306, user='root',passwd='', db='MessageMerge', charset='utf8')

name1 = '软件'
name2 = '测试'
quesql = "select name,url,con_finish_time from qjwqzhb2 where (name like '%%"+name1+"%%') and (name like '%%"+name2+"%%')"
rst =[]
try:
    sqlopt.cursor.execute(quesql)  # 影响的行数
except Exception as abnormal:
    print("SQL有误，错误内容 %s" % abnormal)
if sqlopt.cursor.rowcount == 0:  # 0 则代表没有查询结果
    print "没有查询的结果.."
elif sqlopt.cursor.rowcount == 1:  # 影响行数 为1 fetchone
    rst = list(sqlopt.cursor.fetchone())
else:  # 多行情况下 使用fetchall
    rst = sqlopt.cursor.fetchall()

text = ''
if len(rst)>0:
    i=0
    for tp in rst:
        i += 1
        text +=  str(i) + '、' +'项目:'+   tp[0].decode('utf-8') + '\n    网址:' +  tp[1].decode('utf-8') + '\n    截止时间:' +  tp[2].decode('utf-8') + '\n'
print text

# users=itchat.search_friends("李宁")
# userName= users[0]['UserName']
# print(userName)
# itchat.send(text,toUserName=userName)
