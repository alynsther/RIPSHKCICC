#!/usr/bin/env python
#! coding: utf8
#encoding= utf-8

alist = [[],[],[],[],[]]

string_list = []
string = ''


punctuations = [u'，',u'。',u'？',u'！',u'；',u'：',u' ',u'.',u'(',u'、',u'（',u'）',u')',u'-']

for i in range(5):
    alist[i] = open('sample' + str(i) + '.txt', 'r')

    for line in alist[i]:
        u_line = unicode(line, 'utf8')
        for j in range(len(punctuations)):
            u_line = u_line.replace(punctuations[j], '')

        string += u_line.rstrip()
    string_list.append(string)
        
print 'string is: ' + string
print 'string_list is' , string_list
print string_list[0]


'''

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

'''
