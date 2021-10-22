from random import randint
from json import dump

# entering values
key, data, regularKey, randomFileNumber = {}, {}, [[],[]], randint(1,10**4)

# this function generating numbers in random order in the range from 1 to 94
def randomNumbers():
    randomNumberArray=[]
    while len(randomNumberArray)!=94:
        randomNumber=randint(1,94)
        if randomNumber not in randomNumberArray: randomNumberArray.append(randomNumber)
    return randomNumberArray

# generating a random key by matching the irregularly
# ordered set of numbers with the regularly ordered character set
irregularKey=[[chr(x) for x in range(32,127)],randomNumbers()]

# arranging the key in an orderly sequence to make it ready for use
for x in range(1,95):
    for y in range(0,94):
        if x==irregularKey[1][y]: regularKey[1].append(x), regularKey[0].append(irregularKey[0][y])

# arranging data in dictionary type
for a in range(0,94): key.update({regularKey[1][a]:regularKey[0][a]})
data.update({"algorithm":"AX45-S","layer":1,"key":key})

# saving data in json format to file with .ax extension
with open("operationFiles/key"+str(randomFileNumber)+".ax","w",encoding="UTF-8") as file: dump(data,file,ensure_ascii=False,indent=2)
