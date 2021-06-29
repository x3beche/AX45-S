#  AX45-S Algorithm by x3beche

#Required libraries
import os

#Algorithms
def f_encrypt(oW,nW,rtry):
    own=int(rtry[0][rtry[1].index(oW)])
    nwn=int(rtry[0][rtry[1].index(nW)])
    if own>nwn:
        chc=94-own+nwn
    else:
        chc=nwn-own
    return rtry[1][chc-1]
def f_decrypt(oW,nW,rtry):
    own=int(rtry[0][rtry[1].index(oW)])
    nwn=int(rtry[0][rtry[1].index(nW)])
    if own+nwn>94:
        chc=own+nwn-94
    else:
        chc=nwn+own
    return rtry[1][chc-1]
def keyComplier(fn):
    fn='operationFiles/key'+str(fn)+'.ax'
    f=open(fn,'r')
    klst=f.read().replace('\n','').split('split')
    f.close()
    a=klst[0].split('axen')
    rtry=[[],[]]
    for x in range(0,94):
        cache=klst[x].split('axen')
        rtry[0].append(cache[0])
        rtry[1].append(cache[1])
        cache.clear()
    return rtry,a
def axen_algorithm(text,keyNumber):
    a=keyComplier(keyNumber)[1]
    rtry=keyComplier(keyNumber)[0]
    oW=rtry[1][ord(a[1])-32]
    final=''
    for y in range(0,len(text)):
        oW=f_encrypt(oW,text[y],rtry)
        final=final+oW
    return final
def axde_algorithm(text,keyNumber):
    a=keyComplier(keyNumber)[1]
    rtry=keyComplier(keyNumber)[0]
    oW=rtry[1][ord(a[1])-32]
    final=''
    for y in range(0,len(text)):
        nW=text[y]
        final=final+f_decrypt(oW,nW,rtry)
        oW=text[y]
    return final
def axen(text,keyNumber):
    return axen_algorithm(axen_algorithm(text,keyNumber),keyNumber)
def axde(text,keyNumber):
    return axde_algorithm(axde_algorithm(text,keyNumber),keyNumber)
def opnr(data):
    print('\n')
    f = open(data, 'r')
    klst=f.read().split('split')
    f.close()
    for x in range(0,len(klst)-1):
        cache=klst[x].split('axen')
        print(cache[0],'-',cache[1])
        cache.clear()
def banner():
    f=open('easy_command/banner', 'r')
    print(f.read())
    f.close()
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def pause():
    input('\nPress ENTER to turn main menu.')
def line():
    print('-----------------------------------------------------')

#Key selection and compilation
keyFiles=[]
keyFeedback=True
with os.scandir('operationFiles/') as entries:
    for entry in entries:
        if entry.name[::-1][:2][::-1]=='ax':
            keyFiles.append(entry.name)
while keyFeedback==True:
    clear()
    banner()
    line()
    for q in range(0,len(keyFiles)):
        print(str(q+1)+'-)',keyFiles[q])
    line()
    keynum=input('Enter your key selection » ')
    key=int(keyFiles[int(keynum)-1].replace('key','').replace('.ax',''))
    line()
    if int(keynum)<=len(keyFiles) and int(keynum)>0:
        fn='operationFiles/'+keyFiles[int(keynum)-1]
        fc=os.path.isfile(fn)
        f=open(fn,'r')
        klst=f.read().replace('\n','').split('split')
        f.close()
        a=klst[0].split('axen')
        rtry=[[],[]]
        for x in range(0,94):
            cache=klst[x].split('axen')
            rtry[0].append(cache[0])
            rtry[1].append(cache[1])
            cache.clear()
        g=0
        for z in range(0,len(rtry[0])):
            g=g+int(rtry[0][z])
        if g!= 4465:
            print('Key file is missing or incorrect.')
            line()
            pause()
        keyFeedback=False
    else:
        print('Wrong option, choose another option.')
        pause()

#Main loop
while True:
    clear()
    banner()
    line()
    print('1-)Encrypt normal text\n2-)Decrypt normal text\n3-)Encrypt file\n4-)Decrypt file\n5-)Key viewer')
    line()
    obs=int(input('Option » '))
    clear()
    if obs==1:
        banner()
        line()
        text=input('Text » ')
        clear()
        banner()
        line()
        print('Entered Text   » "'+text+'"')
        line()
        print('Encrypted Text » "'+axen(text,key)+'"')
        line()
        pause()
    elif obs==2:
        banner()
        line()
        text=input('Text » ')
        clear()
        banner()
        line()
        print('Encrypted Text » "'+text+'"')
        line()
        print('Decrypted Text » "'+axde(text,key)+'"')
        line()
        pause()
    elif obs==3:
        banner()
        line()
        textFiles=[]
        textFiles.clear()
        with os.scandir('operationFiles/') as entries:
            for entry in entries:
                if entry.name[::-1][:3][::-1]=="txt":
                    textFiles.append(entry.name)
        if len(textFiles)>=1:
            for q in range(0,len(textFiles)):
                print(str(q+1)+"-)",textFiles[q])
            line()
            fnm=input("Which file » ")
            line()
            f=open("operationFiles/"+textFiles[int(fnm)-1],"r")
            text=f.read().replace("\n","")
            f.close()
            f = open("operationFiles/"+textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-4]+".axen","a")
            f.write(axen(text,key))
            f.close()
            print("Encryption process completed,",textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-4]+".axen created.")
            line()
            pause()
    elif obs==4:
        textFiles=[]
        textFiles.clear()
        with os.scandir('operationFiles/') as entries:
            for entry in entries:
                if entry.name[::-1][:4][::-1]=="axen":
                    textFiles.append(entry.name)
        banner()
        line()
        if len(textFiles)>=1:
            for q in range(0,len(textFiles)):
                print(str(q+1)+"-)",textFiles[q])
            line()
            fnm=input("Which file » ")
            line()
            f=open("operationFiles/"+textFiles[int(fnm)-1],"r")
            text=f.read().replace("\n","")
            f.close()
            f = open("operationFiles/"+textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-5]+".txt","a")
            f.write(axde(text,key))
            f.close()
            print("Decryption process completed,",textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-5]+".txt created.")
            line()
            pause()
    elif obs==5:
        clear()
        banner()
        line()
        opnr(fn)
        print("\n")
        pause()
    else:
        banner()
        line()
        print('Wrong option, choose another option.')
        line()
        pause()
