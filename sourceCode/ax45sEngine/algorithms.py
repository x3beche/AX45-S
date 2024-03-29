from json import load,dumps,loads
from base64 import b64decode,b64encode
from os import scandir

def f_encrypt(oW,nW,rtry):
    own,nwn=int(rtry[0][rtry[1].index(oW)]),int(rtry[0][rtry[1].index(nW)])
    if own>nwn: chc=94-own+nwn
    else: chc=nwn-own
    return rtry[1][chc-1]

def f_decrypt(oW,nW,rtry):
    own,nwn=int(rtry[0][rtry[1].index(oW)]),int(rtry[0][rtry[1].index(nW)])
    if own+nwn>94: chc=own+nwn-94
    else: chc=nwn+own
    return rtry[1][chc-1]

def axen_algorithm(text,keyNumber):
    a,rtry,final=keyComplier(keyNumber)[1],keyComplier(keyNumber)[0],''
    oW=rtry[1][ord(a[1])-32]
    for y in range(0,len(text)):
        oW=f_encrypt(oW,text[y],rtry)
        final=final+oW
    return final

def axde_algorithm(text,keyNumber):
    a,rtry,final=keyComplier(keyNumber)[1],keyComplier(keyNumber)[0],''
    oW=rtry[1][ord(a[1])-32]
    for y in range(0,len(text)):
        nW=text[y]
        final=final+f_decrypt(oW,nW,rtry)
        oW=text[y]
    return final

def axen(text,keyNumber):
    return axen_algorithm(axen_algorithm(dumps({"data":text})[10:len(dumps({"data":text}))-2],keyNumber),keyNumber)

def axde(text,keyNumber):
    return loads('{"data": "'+axde_algorithm(axde_algorithm(text,keyNumber),keyNumber)+'"}')["data"]

def keyComplier(fileNumber):
    fileName,keyList='key'+str(fileNumber)+'.ax',[[],[]]
    try:
        with open(fileName,"r",encoding="utf-8") as file: json_data=load(file)
        if json_data["algorithm"]=="AX45-S" and json_data["layer"] == 1:
            for x in range(1,len(json_data["key"].keys())+1): keyList[0].append(str(x)),keyList[1].append(json_data["key"][str(x)])
            return keyList, [keyList[0][0],keyList[1][0]]
        else:print("This key file is not compatible with this encryption")
    except:print("Wrong key format!")

def keyAnalyzer(fileNumber):
    fileName ='key'+str(fileNumber)+'.ax'
    try:
        with open(fileName,"r",encoding="utf-8") as file: json_data=load(file)
        if json_data["algorithm"]=="AX45-S" and json_data["layer"] == 1:
            for x in range(1,95): print("{} - {}".format(x, json_data["key"][str(x)]))
    except:print("Wrong key format!")

def fileLister(direction):
    programFiles,extensions,files = ["keyConverterOldToNew.py","algorithms.py","AX45-S.py","ax45sEngine","keygenerator.py"],["ax","axen"],[]
    with scandir() as entries:
        if direction == "EN":
            for entry in entries:
                if entry.name.rsplit(".")[-1] not in extensions and entry.name not in programFiles and len(entry.name.split(".")) >= 2 : files.append(entry.name)
            return files
        elif direction == "DE":
            for entry in entries:
                if entry.name.rsplit(".")[-1] == "axen" and len(entry.name.split("."))>=3: files.append(entry.name)
            return files
        elif direction == "KEY":
            for entry in entries: 
                if entry.name.rsplit(".")[-1] == "ax" and len(entry.name.split("."))==2 :files.append(int(entry.name.replace("key","").split(".")[0]))
            return files
        else: return "Wrong direction!"

def fileEN(fileInput,keynum):
    with open(fileInput,"rb") as file: data = axen(b64encode(file.read()).decode(),keynum)
    with open(fileInput+".axen","w") as file: file.write(data)

def fileDE(fileInput,keynum):
    with open(fileInput,"r") as file: data = file.read() 
    with open(fileInput.rsplit(".",1)[0],"wb") as file: file.write(b64decode(axde(data,keynum)))