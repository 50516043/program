# -*- coding: utf-8 -*-
# client3.py
# python3 client3.py HostName PortNumber

from socket import *
import time
import sys
import pbl2017
import shutil
import math
import os.path

#hostlist2 = ['pbl1','pbl2','pbl3','pbl4','pbl5']
hostlist2 = ['pbl1','pbl2','pbl3','pbl4',]
hostlist=[]
ft_port = 50000
cl_port = 50001
rep_sentence=''
server_name =''

def receive_data(client_socket):#データ受信関数,aの長さが0のとき終了
    response_server = bytearray()
    while True:
        a =  client_socket.recv(1)#1024バイトずつ
        if len(a)<=0 :
            break
        response_server.append(a[0])
    receive_str = response_server.decode()
    return receive_str

def receive_data2(client_socket):#データ受信関数,改行で終了
    response_server = bytearray()
    while True:
        a =  client_socket.recv(1)#1バイトずつ
        if len(a)==0:
            continue
        response_server.append(a[0])
        if a == b'\n':
            break
    receive_str = response_server.decode()
    return receive_str

def GET_FILE_request(arg_str,client_socket):
    filename = arg_str[3]
    token_str = arg_str[4]
    print('token_str:',arg_str[4])
    #getarg = pbl2017.genkey(token_str)
    getarg = "e8cf514f7e854da883e9a26421acf2db35d455e7c6ad33435d003678abd8eb00"
    print("hash:",getarg)
    sentence = '{} {} {} {} \n'.format("GETFILE",filename,getarg,int(arg_str[2]))
    #GETFILE rnd50K.txt toke_nstr server_port
    client_socket.send(sentence.encode())
    res_str = receive_data(client_socket)#データを受信
    print(res_str)
  
def rep_request_client(filename,client_socket,token_str):
    global rep_sentence
    sentence = 'REP {} {}\n'.format(filename,pbl2017.repkey(token_str,filename))
    #print(sentence)
    client_socket.send(sentence.encode())
    rep_sentence = receive_data2(client_socket)#REP時間
    #print(rep_sentence)
    
def time_request():
    bandwidth_list = []
    for i in range(len(hostlist)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostlist[i], ft_port))
        s.send('TIMELIST'.encode())
        sentence = receive_data(s)
        print(sentence)
        tmp_list = sentence.split()
        s.close()
        for i in range(2,len(tmp_list)):
            bandwidth_list.append(tmp_list[i])  
    #print(bandwidth_list)
    return bandwidth_list
def send_passlist(passlist):
    sentence = ''
    for i in range(len(passlist)):
        sentence += '{} '.format(passlist[i])
    
    for i in range(len(hostlist)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostlist[i], ft_port))
        s.send('PASSLIST \n'.encode())
        res_str = receive_data2(s)
        print(res_str)
        
        s.send(sentence.encode())
        s.close()
    
def shortest_path(bandwidth_list):
    a12 = float(bandwidth_list[0])
    a13 = float(bandwidth_list[1])
    a14 = float(bandwidth_list[2])
    #a15 = 0.4
    a23 = float(bandwidth_list[3])
    a24 = float(bandwidth_list[4])
    #a25 = 0.06
    a34 = float(bandwidth_list[5])
    #a35 = 0.3
    #a45 = 0.1
    
    route_list = [[0, a12, a13, a14],
              [a12, 0, a23, a24],
              [a13, a23, 0, a34],
              [a14, a24, a34, 0]] # 初期のノード間の距離のリスト
    #print(route_list)
    node_num = len(route_list) #ノードの数
    unsearched_nodes = list(range(node_num)) # 未探索ノード
    distance = [math.inf] * node_num # ノードごとの距離のリスト
    previous_nodes = [-1] * node_num # 最短経路でそのノードのひとつ前に到達するノードのリスト
    distance[0] = 0 # 初期のノードの距離は0とする
    
    while(len(unsearched_nodes) != 0): #未探索ノードがなくなるまで繰り返す
    # まず未探索ノードのうちdistanceが最小のものを選択する
        posible_min_distance = math.inf # 最小のdistanceを見つけるための一時的なdistance。初期値は inf に設定。
        for node_index in unsearched_nodes: # 未探索のノードのループ
            if posible_min_distance > distance[node_index]: 
                posible_min_distance = distance[node_index] # より小さい値が見つかれば更新
        target_min_index = get_target_min_index(posible_min_distance, distance, unsearched_nodes) # 未探索ノードのうちで最小のindex番号を取得
        unsearched_nodes.remove(target_min_index) # ここで探索するので未探索リストから除去

        target_edge = route_list[target_min_index] # ターゲットになるノードからのびるエッジのリスト
        for index, route_dis in enumerate(target_edge):
            if route_dis != 0:
                if distance[index] > (distance[target_min_index] + route_dis):
                    distance[index] = distance[target_min_index] + route_dis # 過去に設定されたdistanceよりも小さい場合はdistanceを更新
                    previous_nodes[index] =  target_min_index #　ひとつ前に到達するノードのリストも更新
    passlist = []
    print("-----経路-----")
    previous_node = node_num - 1
    while previous_node != -1:
        if previous_node !=0:
            #print(str(previous_node + 1) + " <- ", end='')
            print(hostlist[previous_node] , " <- ", end='')
            passlist.append(hostlist[previous_node])
        else:
            #print(str(previous_node + 1))
            print(hostlist[previous_node])
            passlist.append(hostlist[previous_node])
        previous_node = previous_nodes[previous_node]
    
    tmp_passlist=[]
    print("-----距離-----")
    print(distance[node_num - 1])
    for i in range(len(passlist)-1,-1,-1):
        tmp_passlist.append(passlist[i])
    print(tmp_passlist)
    return tmp_passlist            
                
def get_target_min_index(min_index, distance, unsearched_nodes):
    start = 0
    while True:
        index = distance.index(min_index, start)
        found = index in unsearched_nodes
        if found:
            return index
        else:
            start = index + 1
    
def send_info():
    uname =  os.uname()[1]
    sentence = '{} {} {} '.format('client',uname,'hostlist')
    for i in range(len(hostlist)):
        sentence += '{} '.format(hostlist[i])
    sentence += '\n'
    
    for i in range(len(hostlist2)):
        s = socket(AF_INET, SOCK_STREAM)
        print(hostlist2[i])
        print(sentence)
        s.connect((hostlist2[i], ft_port))
        s.send('INFO \n'.encode())
        s.send(sentence.encode())
        s.close()
    print(sentence)
    
def main():#main
    if len(sys.argv) < 5:
        sys.exit('Usage: python3 client4.py [Server_Host] [PortNumber] [File_Name] [token_str]')
    
    global server_name
    global hostlist
    server_name = sys.argv[1]     #ホスト名
    server_port = int(sys.argv[2])#ポート番号
    filename = sys.argv[3]          #ファイル名
    token_str = sys.argv[4]        #トークン文字列
    passlist = []
    uname =  os.uname()[1]
    hostlist.append(server_name)
    for n in range(len(hostlist2)):
        if server_name != hostlist2[n] and uname != hostlist2[n]:
            hostlist.append(hostlist2[n])
    hostlist.append(uname)
    print(hostlist)
    
    send_info()
    
    while True:
        print('BAND','TIME','PATH','PASSLIST')
        str = input('>>>')
        if str == 'BAND':
            print(hostlist[0])
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((hostlist[0], ft_port))
            client_socket.send('BANDWIDTH CALCULATION'.encode())
            client_socket.close()
        elif str == 'TIME':
            bandwidth_list = time_request()
        elif str == 'PATH':
            #print(bandwidth_list)
            passlist = shortest_path(bandwidth_list)
        elif str == 'PASSLIST':
            send_passlist(passlist)
        else:
            break
            
    #ファイル転送プログラムに接続
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, ft_port))  # サーバのソケットに接続する
    GET_FILE_request(sys.argv,client_socket)
    client_socket.close()  
    
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, ft_port))  # サーバのソケットに接続する
    client_socket.send('GETTIME \n'.encode())
    get_sentence = receive_data2(client_socket)
    client_socket.close()  
    #print(get_sentence)
    
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', cl_port))
    s.listen(1)
    print('Transmitting file...')
    connection_socket, addr = s.accept()
    sentence = receive_data2(connection_socket)
    #print(sentence)
    s.close()
    
    shutil.copy("filedata.dat",filename)
    
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, 60623))  # サーバのソケットに接続する
    
    rep_request_client(filename,client_socket,token_str)
    client_socket.close()  
    
    time1 = get_sentence.split()[14]
    time2 = rep_sentence.split()[11]
    timelist1 = time1.split(':')
    timelist2 = time2.split(':')
    
    passtime = int(timelist2[0])*60*60+int(timelist2[1])*60+int(timelist2[2])-(int(timelist1[0])*60*60+int(timelist1[1])*60+int(timelist1[2]))
    
    print('Tile transfer finished: Transmission time: {} sec'.format(passtime))
    
    
if __name__ == '__main__':
     main()