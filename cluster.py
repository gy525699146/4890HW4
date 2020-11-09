import math
import xlrd
import copy
def getdata():
    workbook = xlrd.open_workbook("FraudRaw.xls")
    sheet = workbook.sheet_by_index(0)
    info = []
    for i in range(1,1001):
        dict = {'Age': "", 'Gender': "", 'Claim': "", 'tickets': "", 'prior claims': "", 'atty': "", 'outcome': ""}
        dict['Age'] = sheet.cell_value(i, 0)
        dict['Gender'] = sheet.cell_value(i, 1)
        dict['Claim'] = sheet.cell_value(i, 2)
        dict['tickets'] = sheet.cell_value(i, 3)
        dict['prior claims'] = sheet.cell_value(i, 4)
        dict['atty'] = sheet.cell_value(i, 5)
        dict['outcome'] = sheet.cell_value(i, 6)
        info.append(dict)

    info1 = []
    for i in range(1001,2001):
        dict = {'Age': "", 'Gender': "", 'Claim': "", 'tickets': "", 'prior claims': "", 'atty': "", 'outcome': ""}
        dict['Age'] = sheet.cell_value(i, 0)
        dict['Gender'] = sheet.cell_value(i, 1)
        dict['Claim'] = sheet.cell_value(i, 2)
        dict['tickets'] = sheet.cell_value(i, 3)
        dict['prior claims'] = sheet.cell_value(i, 4)
        dict['atty'] = sheet.cell_value(i, 5)
        dict['outcome'] = sheet.cell_value(i, 6)
        info1.append(dict)
    # for i in info:
    #     print(i)
    return info,info1


def processdata(processdata):
    #process age
    for i in processdata:
        if i['Age'] < 20:
            i['Age'] = 0
        elif i['Age'] < 40 :
            i['Age'] = (i['Age'] - 20)/20
        elif i['Age'] < 60:
            i['Age'] = 1
        elif i['Age'] < 70:
            i['Age'] = 1 - (i['Age'] - 60)/10
        else:
            i['Age'] = 0

    # process claim
    for i in processdata:
        i['Claim'] = (1 - i['Claim']/5000)

    # process ticket
    for i in processdata:
        if i['tickets'] == 0:
            i['tickets'] = 1
        elif i['tickets'] == 1:
            i['tickets'] = 0.6
        else:
            i['tickets'] = 0

    # process ticket
    for i in processdata:
        if i['prior claims'] == 0:
            i['prior claims'] = 1
        elif i['prior claims'] == 1:
            i['prior claims'] = 0.5
        else:
            i['prior claims'] = 0

    # process att
    for i in processdata:
        if i['atty'] == 'none':
            i['atty'] = 1
        else:
            i['atty'] = 0

    # process outcome
    for i in processdata:
        if i['outcome'] == 0:
            i['outcome'] = 'Cluster1'
        else:
            i['outcome'] = 'Cluster2'
    return processdata


def trainning(traindata,cluster1,cluster2):
    newdata = copy.deepcopy(traindata)
    for Item in newdata:
        distance1 = 0
        distance2 = 0
        distance1 = math.pow(Item['Age'] - cluster1['Age'], 2) \
                    + math.pow(Item['Age'] - cluster1['Age'], 2) \
                    + math.pow(Item['Gender'] - cluster1['Gender'], 2) \
                    + math.pow(Item['Claim'] - cluster1['Claim'], 2) \
                    + math.pow(Item['tickets'] - cluster1['tickets'], 2) \
                    + math.pow(Item['prior claims'] - cluster1['prior claims'], 2) \
                    + math.pow(Item['atty'] - cluster1['atty'], 2)

        distance2 = math.pow(Item['Age'] - cluster2['Age'], 2) \
                    + math.pow(Item['Age'] - cluster2['Age'], 2) \
                    + math.pow(Item['Gender'] - cluster2['Gender'], 2) \
                    + math.pow(Item['Claim'] - cluster2['Claim'], 2) \
                    + math.pow(Item['tickets'] - cluster2['tickets'], 2) \
                    + math.pow(Item['prior claims'] - cluster2['prior claims'], 2) \
                    + math.pow(Item['atty'] - cluster2['atty'], 2)

        if distance1 < distance2:
            Item['outcome'] = 'Cluster1'
        else:
            Item['outcome'] = 'Cluster2'
        # print(distance1)
        # print(distance2)
    return newdata


def getNewCluster(data):
    cluster1 = {'Age': 0, 'Gender': 0, 'Claim': 0, 'tickets': 0, 'prior claims': 0, 'atty': 0, 'outcome': "Cluster1"}
    cluster2 = {'Age': 0, 'Gender': 0, 'Claim': 0, 'tickets': 0, 'prior claims': 0, 'atty': 0, 'outcome': "Cluster2"}

    averageList1 = [0,0,0,0,0,0]
    averageList2 = [0,0,0,0,0,0]

    count1 = 0
    count2 = 0

    for item in data:
        if item['outcome'] == 'Cluster1':
            averageList1[0] += item['Age']
            averageList1[1] += item['Gender']
            averageList1[2] += item['Claim']
            averageList1[3] += item['tickets']
            averageList1[4] += item['prior claims']
            averageList1[5] += item['atty']

            count1 += 1
        else:
            averageList2[0] += item['Age']
            averageList2[1] += item['Gender']
            averageList2[2] += item['Claim']
            averageList2[3] += item['tickets']
            averageList2[4] += item['prior claims']
            averageList2[5] += item['atty']
            count2 += 1

    cluster1['Age'] = averageList1[0]/count1
    cluster1['Gender'] = averageList1[1]/count1
    cluster1['Claim'] = averageList1[2]/count1
    cluster1['tickets'] = averageList1[3]/count1
    cluster1['prior claims'] = averageList1[4]/count1
    cluster1['atty'] = averageList1[5]/count1

    cluster2['Age'] = averageList2[0] / count2
    cluster2['Gender'] = averageList2[1] / count2
    cluster2['Claim'] = averageList2[2] / count2
    cluster2['tickets'] = averageList2[3] / count2
    cluster2['prior claims'] = averageList2[4] / count2
    cluster2['atty'] = averageList2[5] / count2

    return cluster1,cluster2




def compare(data1,data2):
    same = True
    try:
        for i in range(1000):
            if data1[i]['outcome'] == data2[i]['outcome']:
                a = data1[i]['outcome']
                b = data2[i]['outcome']
                pass
            else:
                same =  False
    except:
        same = False
    return same


Origindata,test = getdata()
processdata(Origindata)
processdata(test)

cluster1 = Origindata[1]
cluster2 = Origindata[56]
count = 0

listdata1 = []
listdata2 = []
while True:
    listdata1 = trainning(Origindata,cluster1,cluster2)
    same = compare(listdata1,listdata2)
    if same == True:
        print(count)
        print("Right")
        break;
    cluster1,cluster2 = getNewCluster(listdata1)
    count += 1


    listdata2 = trainning(Origindata,cluster1,cluster2)
    same = compare(listdata1,listdata2)
    if same == True:
        print(count)
        print("Right")
        break;

    cluster1,cluster2 = getNewCluster(listdata2)
    count += 1


testtrain = trainning(test,cluster1,cluster2)
Cluster1Wrong = 0
Cluster2Wrong = 0
for i in range(0,1000):
    if test[i]['outcome'] == 'Cluster1':
        if testtrain[i]['outcome'] == 'Cluster2':
            Cluster1Wrong += 1

    if test[i]['outcome'] == 'Cluster2':
        if testtrain[i]['outcome'] == 'Cluster1':
            Cluster2Wrong += 1
print(Cluster1Wrong,Cluster2Wrong)