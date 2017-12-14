# -*- coding: utf-8 -*-
hostlist = ['pbl1','pbl2','pbl3','pbl4','pbl5']


def band_width():#帯域幅計算
    
    #uname =  os.uname()[1]
    uname = 'pbl5'
    for n in range(len(hostlist)):
        if hostlist[n] == uname:
            for i in range(1,len(hostlist)-n):
                #client_socket = socket(AF_INET, SOCK_STREAM)  # ソケットを作る
                #client_socket.connect((hostlist[n],server_port))
                print('Connect to',hostlist[n+i])
                
band_width()