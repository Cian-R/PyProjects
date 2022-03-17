with open("frequencies.txt", "r") as f:
    dataList = f.read().splitlines()

with open("allwords.txt", "r") as d:
    wordList = d.read().splitlines()


print(dataList)
print(wordList)


index = 0
while index < len(dataList):
    print(dataList[index])
    dataList[index] = dataList[index].split(",")
    if dataList[index][0] not in wordList:
        print("Deleting!")
        del dataList[index]
    else:
        print("Keeping!=========================")
        index += 1

print("DATALIST:", dataList)

with open("frequencies.txt", "w") as newF:
    for i in dataList:
        newF.write(",".join(i) + "\n")

print("DATALIST:", len(dataList))
