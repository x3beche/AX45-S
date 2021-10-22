#Required libraries
import os
from json import load
from ax45sEngine.algorithms import *

# some algorithms for better view
def banner():
    f=open('ax45sEngine/banner', 'r')
    print(f.read())
    f.close()
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def pause():
    input('\nPress ENTER to turn main menu.')
def line():
    print('-----------------------------------------------------')

# key selection and compilation
keyFiles=[]
with os.scandir() as entries:
    for entry in entries:
        if entry.name[::-1][:2][::-1]=='ax':keyFiles.append(entry.name)

# set key file to program
while True:
    clear(),banner(),line()
    for q in range(0,len(keyFiles)): print(str(q+1)+'-)',keyFiles[q])
    line()
    keynum=input('Enter your key selection » ')

    if keynum.isdigit()==True:
        if int(keynum)<=len(keyFiles) and int(keynum)>0:
            key=int(keyFiles[int(keynum)-1].replace('key','').replace('.ax',''))
            break
        else: pass
    else: pass

#Main loop
while True:
    clear(),banner(),line(),print('1-)Encrypt normal text\n2-)Decrypt normal text\n3-)Encrypt file\n4-)Decrypt file\n5-)Key viewer'),line()
    obs=input('Option » ')
    clear()
    if obs=="1":
        banner(),line()
        text=input('Text » ')
        clear(),banner(),line(),print('Entered Text   » "'+text+'"'),line(),print('Encrypted Text » "'+axen(text,key)+'"'),line(),pause()
    elif obs=="2":
        banner(),line()
        text=input('Text » ')
        clear(),banner(),line(),print('Encrypted Text » "'+text+'"'),line(),print('Decrypted Text » "'+axde(text,key)+'"'),line(),pause()
    elif obs=="3":  
        banner(),line()
        textFiles=[]
        with os.scandir() as entries:
            for entry in entries:
                if entry.name[::-1][:3][::-1]=="txt":textFiles.append(entry.name)
        if len(textFiles)>=1:
            for q in range(0,len(textFiles)):print(str(q+1)+"-)",textFiles[q])
            line()
            fnm=input("Which file » ")
            line()
            f=open(textFiles[int(fnm)-1],"r")
            text=f.read().replace("\n","")
            f.close()
            f = open(textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-4]+".axen","a")
            f.write(axen(text,key))
            f.close()
            print("Encryption process completed,",textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-4]+".axen created.")
            line(),pause()
    elif obs=="4":
        textFiles=[]
        with os.scandir() as entries:
            for entry in entries:
                if entry.name[::-1][:4][::-1]=="axen": textFiles.append(entry.name)
        banner(),line()
        if len(textFiles)>=1:
            for q in range(0,len(textFiles)): print(str(q+1)+"-)",textFiles[q])
            line()
            fnm=input("Which file » ")
            line()
            f=open(textFiles[int(fnm)-1],"r")
            text=f.read().replace("\n","")
            f.close()
            f = open(textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-5]+".txt","a")
            f.write(axde(text,key))
            f.close()
            print("Decryption process completed,",textFiles[int(fnm)-1][:len(textFiles[int(fnm)-1])-5]+".txt created."),line(),pause()
    elif obs=="5":
        clear(),banner(),line(),keyAnalyzer(key),pause()
    else:
        banner(),line(),print('Wrong option, choose another option.'),line(),pause()