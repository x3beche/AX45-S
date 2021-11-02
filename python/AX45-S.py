# Required libraries
import os
from ax45sEngine.algorithms import *

# Some algorithms for better view
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

# Setting key file to program
while True:
    clear(),banner(),line()
    keyFiles = fileLister("KEY")
    for x in range(0,len(keyFiles)): print(str(x+1)+'-) key'+str(keyFiles[x])+".ax")
    line()
    keynum=input('Enter your key selection » ')

    if keynum.isdigit()==True:
        if int(keynum)<=len(keyFiles) and int(keynum)>0:
            key=keyFiles[int(keynum)-1]
            break

# Main loop
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
        clear(),banner(),line(),print('Encrypted Text » "'+text+'"'),line()
        try : print('Decrypted Text » "'+axde(text,key)+'"')
        except : print("ERROR :: Algorithm, key and text do not complement each other. This text cannot be decrypted with the key you used!")
        line(),pause()
    elif obs=="3":  
        banner(),line()
        files = fileLister("EN")
        if len(files)>=1:
            for x in range(0,len(files)): print(str(x+1)+"-) "+files[x])
            line()
            try :
                fileName=files[int(input("Which file » "))-1]
                line(),fileEN(fileName,key),print(f"Encryption process completed {fileName}.axen created."),line(),pause()
            except : line(),print('ERROR :: Wrong option, choose correct option.'),line(),pause()
    elif obs=="4":
        banner(),line()
        files = fileLister("DE")
        if len(files)>=1:
            for x in range(0,len(files)): print(str(x+1)+"-)",files[x])
            line()
            try :
                fileName = files[int(input("Which file » "))-1]
                fileNameDecrpted = fileName.rsplit(".",1)[0]
                line(),fileDE(fileName,key),print(f"Decryption process completed {fileNameDecrpted} created."),line(),pause()
            except : line(),print('ERROR :: Wrong option, choose correct option.'),line(),pause()
    elif obs=="5":
        clear(),banner(),line(),keyAnalyzer(key),pause()
    elif obs=="q": 
            clear(),banner(),line(),print('1-)Encrypt normal text\n2-)Decrypt normal text\n3-)Encrypt file\n4-)Decrypt file\n5-)Key viewer'),line(),print('Enter your key selection » Bye!'),exit()
    else:banner(),line(),print('ERROR :: Wrong option, choose correct option.'),line(),pause()