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

def keyComplier(fn):
    fn,rtry='key'+str(fn)+'.ax',[[],[]]
    f=open(fn,'r')
    klst=f.read().replace('\n','').split('split')
    f.close()
    a=klst[0].split('axen')
    for x in range(0,94):
        cache=klst[x].split('axen')
        rtry[0].append(cache[0])
        rtry[1].append(cache[1])
        cache.clear()
    return rtry,a

def axen(text,keyNumber):
    return axen_algorithm(axen_algorithm(text,keyNumber),keyNumber)
def axde(text,keyNumber):
    return axde_algorithm(axde_algorithm(text,keyNumber),keyNumber)
