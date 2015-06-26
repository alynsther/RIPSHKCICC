#encoding=utf8

def countWords(strlist):
    worep=""
    for j in range(len(strlist)):
        for i in range(len(strlist[j])):
            if strlist[j][i] not in worep:
                worep+=strlist[j][i]
    print worep
    occurrences=[]
    for i in range(len(strlist)):
        occurrences.append([])
    for i in range(len(strlist)):
        for j in range(len(worep)):
            occurrences[i].append(strlist[i].count(worep[j]))
            total=float(sum(occurrences[i]))
        for j in range(len(occurrences[i])):
            occurrences[i][j] = occurrences[i][j]/total
    return occurrences

string=u"今天我起来得很晚上午我们做了一大堆没用的事情并且我现在特别困"
string2=u"他他他他他"
string3=u"abcd"
strlist=[string,string2,string3]
print countWords(strlist)
