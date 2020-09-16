from socket import *            # Socket通信 - 依据Socket搭建HTTP
import time                     # 时间 - 获取当前时间日期
from bs4 import BeautifulSoup   # HTML工具 - 解析编辑HTML文档
import json                     # 服务器消息打包 - json格式转换

admin = [['18120189', 'linyijun'],                          # 管理员用户
         ['18120162', 'sunyiqi'],
         ['18120172', 'wangruyan']]

serverName = "localhost"    # 主机名
serverPort = 9999           # 端口号
serverSocket = socket(AF_INET, SOCK_STREAM)                 # 创建客户端Socket - AF_INET IPv4 - SOCK_STREAM TCP
serverSocket.bind((serverName, serverPort))                 # Bind主机名及端口号
serverSocket.listen(20)                                     # 开启ServerSocket监听（最多20个进程）
print("The Server is READY to RECEIVE via TCP.")            # 输出提示语句

while 1:
    connectionSocket, clientAddr = serverSocket.accept()    # 与客户端Socket建立连接
    receivedMsg = connectionSocket.recv(2048)               # 接收客户端发送数据 - 大小

    if receivedMsg.decode()[0:3] == 'GET':                  # 识别为GET请求
        # recvSentMsg = "The Server has received '" + receivedMsg.decode() + "' as your message."
        recvSentMsg = 'HTTP/1.1 200 OK\r\n' \
                      'Connection: close\r\n'               # 服务器响应语句
        datetime = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                 time.localtime())          # 获取当前时间
        recvSentMsg = recvSentMsg + datetime + '\r\nServer: Just For Testing(YijunStudio)\r\nLast-Modified: Tue, 15 Sep 2020 23:47:55 GMT\r\nContent-type: text-html\r\n'
                                                            # 服务器响应语句（续）
        # print("The Server has received '" + receivedMsg.decode() + "' as client's message.")
        print('ClientMsg:\r\n'
              + receivedMsg.decode())                       # 输出客户端请求 - 仅供提示
        htmlstr = BeautifulSoup(open('/Users/reneelin/PycharmProjects/HTTP/Server/index.html'), features='html.parser')
        recvSentMsg = json.dumps({'httpmsg': recvSentMsg,   # 使用json格式编制发送数据
                                  'htmldom': htmlstr.prettify(),
                                  'endmsg': 'Connection closed by foreign host.\r\n'})
        connectionSocket.send(recvSentMsg.encode())         # 向客户端返回数据
        connectionSocket.close()                            # 关闭Socket连接

    elif receivedMsg.decode()[0:4] == 'POST':               # 识别为POST请求
        receivedMsgNew = receivedMsg.decode()               # 将Bytes解码为Str
        receivedMsgNew = receivedMsgNew.split('\r\n')       # CRLF分割POST请求
        usr, pwd = receivedMsgNew[3].split('&')             # 获取传参行并分割各个参数
        if usr.split('=')[0] == 'usr' \
                and pwd.split('=')[0] == 'pwd':             # 识别为登录信息
            usr = usr.split('=')[1]                         # 分割username参数与参数值
            pwd = pwd.split('=')[1]                         # 分割password参数与参数值
            input = [usr, pwd]                              # 将username与password组成列表供查阅

            if input in admin:                                  # username及password合法
                # recvSentMsg = "The Server has received '" + receivedMsg.decode() + "' as your message."
                recvSentMsg = 'HTTP/1.1 200 OK\r\n' \
                              'Connection: close\r\n'           # 服务器响应语句
                datetime = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                         time.localtime())      # 获取当前时间
                recvSentMsg = recvSentMsg + datetime + '\r\nServer: Just For Testing(YijunStudio)\r\nLast-Modified: Tue, 15 Sep 2020 23:47:55 GMT\r\nContent-type: text-html\r\n'
                                                                # 服务器响应语句（续）
                # print("The Server has received '" + receivedMsg.decode() + "' as client's message.")
                print('ClientMsg:\r\n' + receivedMsg.decode())  # 输出客户端请求 - 仅供提示
                htmlstr = BeautifulSoup(open('/Users/reneelin/PycharmProjects/HTTP/Server/home.html'),
                                        features='html.parser') # BeautifulSoup解析HTML文档 - 进入功能页
                recvSentMsg = json.dumps({'status': 'success',  # 使用json格式编制发送数据
                                          'httpmsg': recvSentMsg,
                                          'htmldom': htmlstr.prettify(),
                                          'endmsg': 'Connection closed by foreign host.\r\n'})
                connectionSocket.send(recvSentMsg.encode())     # 向客户端返回数据
                connectionSocket.close()                        # 关闭Socket连接
            else:                                               # username及password不合法
                recvSentMsg = 'HTTP/1.1 200 OK\r\n' \
                              'Connection: close\r\n'           # 服务器响应语句
                datetime = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                         time.localtime())      # 获取当前时间
                recvSentMsg = recvSentMsg + datetime + '\r\nServer: Just For Testing(YijunStudio)\r\nLast-Modified: Tue, 15 Sep 2020 23:47:55 GMT\r\nContent-type: text-html\r\n'
                                                                # 服务器响应语句（续）
                # print("The Server has received '" + receivedMsg.decode() + "' as client's message.")
                print('ClientMsg:\r\n' + receivedMsg.decode())  # 输出客户端请求 - 仅供提示
                htmlstr = BeautifulSoup(open('/Users/reneelin/PycharmProjects/HTTP/Server/wrong.html'),
                                        features='html.parser') # BeautifulSoup解析HTML文档 - 错误提示
                recvSentMsg = json.dumps({'status': 'fail',     # 使用json格式编制发送数据
                                          'httpmsg': recvSentMsg,
                                          'htmldom': htmlstr.prettify(),
                                          'endmsg': 'Connection closed by foreign host.\r\n'})
                connectionSocket.send(recvSentMsg.encode())     # 向客户端返回数据
                connectionSocket.close()                        # 关闭Socket连接

        elif usr.split('=')[0] == 'itm' \
                and pwd.split('=')[0] == 'prc':             # 识别为条目信息
            usr = usr.split('=')[1]                         # 分割item参数与参数值
            pwd = pwd.split('=')[1]                         # 分割price参数与参数值
            input = [usr, pwd]                              # 将item与price组成列表

            recvSentMsg = 'HTTP/1.1 200 OK\r\n' \
                          'Connection: close\r\n'           # 服务器响应语句
            datetime = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                     time.localtime())      # 获取当前时间 - 响应用
            dnt = time.strftime("%b %d %Y %H:%M:%S",
                                time.localtime())           # 获取当前时间 - 账本用
            recvSentMsg = recvSentMsg + datetime + '\r\nServer: Just For Testing(YijunStudio)\r\nLast-Modified: Tue, 15 Sep 2020 23:47:55 GMT\r\nContent-type: text-html\r\n'
                                                            # 服务器响应语句（续）
            # print("The Server has received '" + receivedMsg.decode() + "' as client's message.")
            print('ClientMsg:\r\n' + receivedMsg.decode())  # 输出客户端请求 - 仅供提示
            htmlstr = BeautifulSoup(open('/Users/reneelin/PycharmProjects/HTTP/Server/home.html'),
                                    features='html.parser') # BeautifulSoup解析HTML文档并编辑
            new_tr = htmlstr.new_tag("tr")                  # 创建新HTML标签'tr'
            tb = htmlstr.find('table')                      # 在HTML文档中搜索HTML标签'table'
            tb.append(new_tr)                               # 将新建的'tr'标签置于'table'标签之后
            new_th_dnt = htmlstr.new_tag("th")              # 创建新HTML标签'th' - dnt
            new_th_itm = htmlstr.new_tag("th")              # 创建新HTML标签'th' - itm
            new_th_prc = htmlstr.new_tag("th")              # 创建新HTML标签'th' - prc
            new_tr.insert(0, new_th_dnt)                    # 将新建的'th'标签dnt - 插入新建的'tr'标签内
            new_tr.insert(1, new_th_itm)                    # 将新建的'th'标签itm - 插入新建的'tr'标签内
            new_tr.insert(2, new_th_prc)                    # 将新建的'th'标签prc - 插入新建的'tr'标签内
            new_th_dnt.string = dnt                         # 修改新建的'th'标签dnt内容
            new_th_itm.string = input[0]                    # 修改新建的'th'标签itm内容
            new_th_prc.string = input[1]                    # 修改新建的'th'标签prc内容
            fo = open('/Users/reneelin/PycharmProjects/HTTP/Server/home.html', 'w')
            fo.write(htmlstr.prettify())                    # 打开并写入修改后的home.html
            fo.close()                                      # 关闭文件
            recvSentMsg = json.dumps({'status': 'insert',   # 使用json格式编制发送数据
                                      'httpmsg': recvSentMsg,
                                      'htmldom': htmlstr.prettify(),
                                      'endmsg': 'Connection closed by foreign host.\r\n'})
            connectionSocket.send(recvSentMsg.encode())     # 向客户端返回数据
            connectionSocket.close()                        # 关闭Socket连接