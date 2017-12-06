d# -*- coding: utf-8 -*-
# client3.py
# python3 client3.py HostName PortNumber
#

from socket import *
import time
import sys

def receive_data(client_socket):#データ受信関数,aの長さが0のとき終了
    response_server = bytearray()
    while True:
        a =  client_socket.recv(1)#1バイトずつ
        if len(a)<=0 :
            break
        response_server.append(a[0])
    receive_str = response_server.decode()
    return receive_str

def SEND_request_s(word_list,client_socket):
    sentence = "SEND \n"
    client_socket.send(sentence.encode())
    #res_str = receive_data(client_socket)
    res_str = client_socket.recv(1024).decode()
    res_str_list = res_str.split()
    print(res_str)
    if res_str_list[0] == "OK":
        print("SEND_FILE_DATA...",end='')
        filedata = "Helllo,World!!!"   ####ファイル送信####
        client_socket.send(filedata.encode())
        print('完了！')
    
def main():#main
    if len(sys.argv) < 2:
        sys.exit('Usage: python3 client3.py HostName PortNumber')
    server_name = sys.argv[1]     #ホスト名
    server_port = int(sys.argv[2])#ポート番号
    #server_name = 'localhost'     #ホスト名
    #server_port = 60623 #ポート番号
    
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, server_port))  # サーバのソケットに接続する
    
    input_sentence = input('SEND\n>>>')
    input_list = input_sentence.split()#命令分割
    
    if input_list[0] == 'SEND':
        SEND_request_s(input_list,client_socket)
    
    client_socket.close()  
if __name__ == '__main__':
    main()
