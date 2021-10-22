from json import dump

introductions  = """Storage and operation of key files at 22.10.2021 have been improved. 
If you have old key files, you can update your keys using the /python/ax45sEngine/keyConverterOldToNew.py program.
*------------------------------------------------------------------------*
Introductions : First, make sure you back up the old key file, then put the old key file in the 
directory where this program is located and when program started enter your key number in the input section. 
The program will update the key file."""
print(introductions)

filenum = input("Number of the key file >> ")

def keyComplier(fn):
    fn,rtry='key'+fn+'.ax',[[],[]]
    try:
        f=open(fn,'r')
        klst=f.read().replace('\n','').split('split')
        f.close()
        a=klst[0].split('axen')
        for x in range(0,94):
            cache=klst[x].split('axen')
            rtry[0].append(cache[0])
            rtry[1].append(cache[1])
            cache.clear()
        return rtry
    except:
        print("Wrong key number!")
        exit()

oldDesignKey = keyComplier(filenum)
key, json_data, regularKey, randomFileNumber = {}, {}, [[],[]], filenum
for x in range(0,94): regularKey[0].append(oldDesignKey[1][x]), regularKey[1].append(oldDesignKey[0][x])
for x in range(0,94): key.update({regularKey[1][x]:regularKey[0][x]})
json_data.update({"algorithm":"AX45-S","layer":1,"key":key})
with open("key"+filenum+".ax","w",encoding="UTF-8") as file: dump(json_data,file,ensure_ascii=False,indent=2)