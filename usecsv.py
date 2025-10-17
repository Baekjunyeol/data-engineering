import csv, os

def opencsv(filename):
    f = open(filename, 'r', encoding='utf8') #한글 저장할거니까
    reader = csv.reader(f)
    output = []
    for i in reader:
        output.append(i)
    f.close()
    return output

def writecsv(filename, the_list):
    with open(filename, 'w', newline = '', encoding ='utf-8-sig') as f:
        a = csv.writer(f, delimiter=',')
        a.writerows(the_list)

def switch(listName):
    for i in listName:
        for j in i:
            try:
                i[i.index(j)] = float(j.replace(',', ''))
            except:
                pass
    return listName
