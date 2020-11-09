import math
import xlrd
import copy
def getdata():
    workbook = xlrd.open_workbook("LoanRaw.xls")
    sheet = workbook.sheet_by_index(0)
    info = []
    for i in range(1,601):
        dict = {'Age': "", 'Income': "", 'Credit Rating': "", 'Risk': "", 'On-time': "",'cluster':''}
        dict['Age'] = sheet.cell_value(i, 0)
        dict['Income'] = sheet.cell_value(i, 1)
        dict['Credit Rating'] = sheet.cell_value(i, 5)
        dict['Risk'] = sheet.cell_value(i, 6)
        dict['On-time'] = sheet.cell_value(i, 7)
        info.append(dict)

    info1 = []
    for i in range(601,651):
        dict = {'Age': "", 'Income': "", 'Credit Rating': "", 'Risk': "", 'On-time': ""}
        dict['Age'] = sheet.cell_value(i, 0)
        dict['Income'] = sheet.cell_value(i, 1)
        dict['Credit Rating'] = sheet.cell_value(i, 5)
        dict['Risk'] = sheet.cell_value(i, 6)
        dict['On-time'] = sheet.cell_value(i, 7)
        info1.append(dict)
    # for i in info:
    #     print(i)
    return info,info1


def processdata(processdata):
    #process age
    age = []
    for item in processdata:
        age.append(item['Age'])
    agemax = max(age)
    agemin = min(age)
    for item in processdata:
        item['Age'] = (item['Age'] - agemin)/(agemax - agemin)

    # process income
    income = []
    for item in processdata:
        income.append(item['Income'])
    incomemax = max(income)
    incomemin = min(income)
    for item in processdata:
        item['Income'] = (item['Income'] - incomemin) / (incomemax - incomemin)

    #process credit
    for item in processdata:
        if item['Credit Rating'] == 'green':
            item['Credit Rating'] = 0
        elif item['Credit Rating'] == 'amber':
            item['Credit Rating'] = 0.5
        elif item['Credit Rating'] == 'red':
            item['Credit Rating'] = 1


    #process risk
    for item in processdata:
        if item['Risk'] == 'low':
            item['Risk'] = 0
        elif item['Risk'] == 'medium':
            item['Risk'] = 0.5
        elif item['Risk'] == 'high':
            item['Risk'] = 1
    return processdata


#dict = {'Age': "", 'Income': "", 'Credit Rating': "", 'Risk': "", 'On-time': ""}
def trainning(traindata,cluster1,cluster2):
    newdata = copy.deepcopy(traindata)
    for Item in newdata:
        distance1 = 0
        distance2 = 0

        distance1 = math.pow(Item['Age'] - cluster1['Age'], 2) \
                    + math.pow(Item['Income'] - cluster1['Income'], 2) \
                    + math.pow(Item['Credit Rating'] - cluster1['Credit Rating'], 2) \
                    + math.pow(Item['Risk'] - cluster1['Risk'], 2) \
                    + math.pow(Item['On-time'] - cluster1['On-time'], 2)

        distance2 = math.pow(Item['Age'] - cluster2['Age'], 2) \
                    + math.pow(Item['Income'] - cluster2['Income'], 2) \
                    + math.pow(Item['Credit Rating'] - cluster2['Credit Rating'], 2) \
                    + math.pow(Item['Risk'] - cluster2['Risk'], 2) \
                    + math.pow(Item['On-time'] - cluster2['On-time'], 2)

        if distance1 < distance2:
            Item['cluster'] = 'Cluster1'
        else:
            Item['cluster'] = 'Cluster2'
        # print(distance1)
        # print(distance2)
    return newdata

#
#dict = {'Age': "", 'Income': "", 'Credit Rating': "", 'Risk': "", 'On-time': ""}
def getNewCluster(data):
    cluster1 = {'Age': 0, 'Income': 0, 'Credit Rating': 0, 'Risk': 0, 'On-time': 0, 'cluster':''}
    cluster2 = {'Age': 0, 'Income': 0, 'Credit Rating': 0, 'Risk': 0, 'On-time': 0, 'cluster':''}

    averageList1 = [0,0,0,0,0]
    averageList2 = [0,0,0,0,0]

    count1 = 0
    count2 = 0

    for item in data:
        if item['cluster'] == 'Cluster1':
            averageList1[0] += item['Age']
            averageList1[1] += item['Income']
            averageList1[2] += item['Credit Rating']
            averageList1[3] += item['Risk']
            averageList1[4] += item['On-time']
            count1 += 1
        else:
            averageList2[0] += item['Age']
            averageList2[1] += item['Income']
            averageList2[2] += item['Credit Rating']
            averageList2[3] += item['Risk']
            averageList2[4] += item['On-time']
            count2 += 1

    cluster1['Age'] = averageList1[0]/count1
    cluster1['Income'] = averageList1[1]/count1
    cluster1['Credit Rating'] = averageList1[2]/count1
    cluster1['Risk'] = averageList1[3]/count1
    cluster1['On-time'] = averageList1[4]/count1

    cluster2['Age'] = averageList2[0] / count2
    cluster2['Income'] = averageList2[1] / count2
    cluster2['Credit Rating'] = averageList2[2] / count2
    cluster2['Risk'] = averageList2[3] / count2
    cluster2['On-time'] = averageList2[4] / count2

    return cluster1,cluster2

#
#

def compare(data1,data2):
    same = True
    leng = len(data1)
    try:
        for i in range(leng):
            if data1[i]['cluster'] == data2[i]['cluster']:
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
cluster2 = Origindata[3]
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
Cluster1 = 0
Cluster2 = 0
for item in testtrain:
    if item['cluster'] == 'Cluster1':
        Cluster1 += 1
    else:
        Cluster2 += 1
print(Cluster1,Cluster2)
print(cluster1)
print(cluster2)