from socket import *            # Socket通信 - 依据Socket搭建HTTP
from tkinter import *           # GUI - Button发送GET请求
import json                     # 服务器消息解析 - json格式转换
import os                       # 本地文件存在判断 - 本地文件阅后即焚
from threading import Timer     # 轮询 - 使用计时器 - 监测是否有POST消息
import webbrowser               # 浏览器 - 唤起 - 打开本地页面


def GET(url):
    clientSocket = socket(AF_INET, SOCK_STREAM)             # 创建客户端Socket - AF_INET IPv4 - SOCK_STREAM TCP
    clientSocket.connect((serverName, serverPort))          # 客户端Socket连接服务器 - 主机名与端口号
    # yourSentMsg = input("Send your message to the Server via TCP: ")
    yourSentMsg = 'GET /' + url + ' HTTP/1.1\r\nHOST:' + serverName + ':' \
                  + str(serverPort) + '\r\n\r\n'                 # GET请求
    clientSocket.send(yourSentMsg.encode())                 # 向服务器发送GET请求
    receivedMsg = clientSocket.recv(8192)                   # 接收服务器返回数据 - 大小
    print(json.loads(receivedMsg.decode())['httpmsg'])      # 解析服务器返回json数据 - httpmsg字段
    print(json.loads(receivedMsg.decode())['htmldom'])      # 解析服务器返回json数据 - htmldom字段
    print(json.loads(receivedMsg.decode())['endmsg'])       # 解析服务器返回json数据 - endmsg字段
    clientSocket.close()                                    # 关闭Socket连接
    fo = open('index.html', 'w')                            # 打开客户端index.html文件
    fo.write(json.loads(receivedMsg.decode())['htmldom'])   # 向index.html文件中写入服务器返回的htmldom字段
    fo.close()                                              # 关闭文件
    webbrowser.open('file:///Users/reneelin/PycharmProjects/HTTP/index.html')
    # print('openBrowser')                                  # 唤起浏览器并打开客户端index.html文件
    LOOP(detect, 2)                                         # 轮询监测是否有POST请求


def POST(url, data):
    clientSocket = socket(AF_INET, SOCK_STREAM)             # 创建客户端Socket - AF_INET IPv4 - SOCK_STREAM TCP
    clientSocket.connect((serverName, serverPort))          # 客户端Socket连接服务器 - 主机名与端口号
    # yourSentMsg = input("Send your message to the Server via TCP: ")
    yourSentMsg = 'POST /' + url + ' HTTP/1.1\r\nHOST:' + serverName + ':' + str(serverPort) \
                  + '\r\n\r\n' + data + '\r\n\r\n'          # POST请求 - 带参
    clientSocket.send(yourSentMsg.encode())                 # 向服务器发送POST请求
    receivedMsg = clientSocket.recv(8192)                   # 接收服务器返回数据 - 大小
    print(json.loads(receivedMsg.decode())['httpmsg'])      # 解析服务器返回json数据 - httpmsg字段
    print(json.loads(receivedMsg.decode())['htmldom'])      # 解析服务器返回json数据 - htmldom字段
    print(json.loads(receivedMsg.decode())['endmsg'])       # 解析服务器返回json数据 - endmsg字段
    clientSocket.close()                                    # 关闭Socket连接
    fo = open('index.html', 'w')                            # 打开客户端index.html文件
    fo.write(json.loads(receivedMsg.decode())['htmldom'])   # 向index.html文件中写入服务器返回的htmldom字段
    fo.close()                                              # 关闭文件
    webbrowser.open('file:///Users/reneelin/PycharmProjects/HTTP/index.html')
    # print('openBrowser')                                  # 唤起浏览器并打开客户端index.html文件


def detect():
    while os.path.isfile('/Users/reneelin/Downloads/login.txt'):
        login = open('/Users/reneelin/Downloads/login.txt',
                     'r', encoding='UTF-8-sig')             # 判断是否存在并打开本地数据缓存文件
        loginstr = login.readline()                         # 读取文件首行
        if loginstr != ' ' and loginstr != '':              # 有效字符串判断
            POST('index.html', loginstr)                    # 向服务器发送带参POST请求
            os.remove('/Users/reneelin/Downloads/login.txt')# 删除本地数据缓存文件
            break
    return


def LOOP(func, second):
    while 1:                    # 每隔second秒执行func函数
        timer = Timer(second, func)
        timer.start()
        timer.join()



if __name__ == '__main__':
    serverName = "localhost"    # 主机名
    serverPort = 9999           # 端口号
    root = Tk()                 # Tkinter GUI 图形界面创建
    button = Button(root,       # GET请求发起按钮
                    text = '使用浏览器请求HTML',
                    command = lambda: GET('index.html'))
    button.pack()               # 按钮创建完成
    root.mainloop()             # 进入图形界面循环