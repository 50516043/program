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
hostlist2 = ['pbl1','pbl2','pbl3','pbl4','pbl5','pbl6','pbl7']
hostlist=[]
bandwidth_list2 = []
ft_port = 54900
cl_port = 54901
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
    getarg = pbl2017.genkey(token_str)
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
    for i in range(len(hostlist2)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostlist2[i], ft_port))
        s.send('TIMELIST \n'.encode())
        sentence = receive_data(s)
        print(sentence)
        tmp_list = sentence.split()
        s.close()
        for i in range(2,len(tmp_list)):
            bandwidth_list.append(tmp_list[i])  
    #print(bandwidth_list)
    
    a12 = float(bandwidth_list[0])
    a13 = float(bandwidth_list[1])
    a14 = float(bandwidth_list[2])
    a15 = float(bandwidth_list[3])
    a16 = float(bandwidth_list[4])
    a17 = float(bandwidth_list[5])
    
    a23 = float(bandwidth_list[6])
    a24 = float(bandwidth_list[7])
    a25 = float(bandwidth_list[8])
    a26 = float(bandwidth_list[9])
    a27 = float(bandwidth_list[10])
    
    a34 = float(bandwidth_list[11])
    a35 = float(bandwidth_list[12])
    a36 = float(bandwidth_list[13])
    a37 = float(bandwidth_list[14])
    
    a45 = float(bandwidth_list[15])
    a46 = float(bandwidth_list[16])
    a47 = float(bandwidth_list[17])
    
    a56 = float(bandwidth_list[18])
    a57 = float(bandwidth_list[19])
    
    a67 = float(bandwidth_list[20])
    bandwidth_time_list   = [[0, a12, a13, a14, a15, a16, a17],
                             [a12, 0,  a23, a24, a25, a26, a27],
                             [a13, a23, 0, a34 ,a35 , a36, a37],
                             [a14, a24, a34, 0, a45 , a46, a47],
                             [a15, a25, a35, a45, 0,  a56, a57],
                             [a16, a26, a36, a46, a56 , 0, a67],
                             [a17, a27, a37, a47, a57 , a67,0 ]] 
    
    #print('bandwidth_list')
    #print(bandwidth_time_list)
    
    print('hostlist',hostlist)
    hostnumber = []
    for i in range(len(hostlist)):
        hostnumber.append(int(list(hostlist[i])[3]))
    #print(hostnumber)
    
    for i in range(len(hostlist)):
        for j in range(i+1,len(hostlist)):
            #print(hostnumber[i],hostnumber[j])
            bandwidth_list2.append(bandwidth_time_list[hostnumber[i]-1][hostnumber[j]-1]) 
             
    #print("bandwidth_list")
    #print(bandwidth_list2)
    
    return bandwidth_list2

def send_passlist(passlist):
    sentence = ''
    for i in range(len(passlist)):
        sentence += '{} '.format(passlist[i])
    for i in range(len(hostlist)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((hostlist[i], ft_port))
        s.send('PASSLIST \n'.encode())
        res_str = receive_data2(s)
        s.send(sentence.encode())
        s.close()
    
def shortest_path(bandwidth_list):
    print(len(bandwidth_list))
    a12 = float(bandwidth_list[0])
    a13 = float(bandwidth_list[1])
    a14 = float(bandwidth_list[2])
    a15 = float(bandwidth_list[3])
    a16 = float(bandwidth_list[4])
    a17 = float(bandwidth_list[5])
    
    a23 = float(bandwidth_list[6])
    a24 = float(bandwidth_list[7])
    a25 = float(bandwidth_list[8])
    a26 = float(bandwidth_list[9])
    a27 = float(bandwidth_list[10])
    
    a34 = float(bandwidth_list[11])
    a35 = float(bandwidth_list[12])
    a36 = float(bandwidth_list[13])
    a37 = float(bandwidth_list[14])
    
    a45 = float(bandwidth_list[15])
    a46 = float(bandwidth_list[16])
    a47 = float(bandwidth_list[17])
    
    a56 = float(bandwidth_list[18])
    a57 = float(bandwidth_list[19])
    
    a67 = float(bandwidth_list[20])
    
    route_list = [[0, a12, a13, a14, a15, a16, a17],
                 [a12, 0,  a23, a24, a25, a26, a27],
                 [a13, a23, 0, a34 ,a35 , a36, a37],
                 [a14, a24, a34, 0, a45 , a46, a47],
                 [a15, a25, a35, a45, 0,  a56, a57],
                 [a16, a26, a36, a46, a56 , 0, a67],
                 [a17, a27, a37, a47, a57 , a67,0]] 
    
    
    # 初期のノード間の距離のリスト
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
        s.connect((hostlist2[i], ft_port))
        s.send('INFO \n'.encode())
        s.send(sentence.encode())
        s.close()
    
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
    #print(hostlist)
    
    send_info()
    
    bandwidth_list = time_request()
    passlist = shortest_path(bandwidth_list)
    send_passlist(passlist)
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
    print(sentence)
    s.close()
    
    data = ''
    for i in range(5):
        f0 = open('{}.dat'.format(i),'r')
        data += f0.read()
        f0.close()
    
    f = open(filename,'w')
    f.write(data)
    f.close()
    
    client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
    client_socket.connect((server_name, server_port))  # サーバのソケットに接続する
    
    rep_request_client(filename,client_socket,token_str)
    client_socket.close()  
    print(rep_sentence)
    
    time1 = get_sentence.split()[14]
    time2 = rep_sentence.split()[11]
    timelist1 = time1.split(':')
    timelist2 = time2.split(':')
    
    passtime = int(timelist2[0])*60*60+int(timelist2[1])*60+int(timelist2[2])-(int(timelist1[0])*60*60+int(timelist1[1])*60+int(timelist1[2]))
    
    print('Tile transfer finished: Transmission time: {} sec'.format(passtime))
    
    
if __name__ == '__main__':
     main()