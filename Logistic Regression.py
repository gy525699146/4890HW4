import pandas
import xlrd
import xlwt
import math
from xlutils.copy import copy
def getdata():
    workbook = xlrd.open_workbook("FraudRaw.xls")
    sheet = workbook.sheet_by_index(0)
    info = []
    for i in range(1,1001):
        smallinfo = []
        smallinfo.append(sheet.cell_value(i, 0))
        smallinfo.append(sheet.cell_value(i, 1))
        smallinfo.append(sheet.cell_value(i, 2))
        smallinfo.append(sheet.cell_value(i, 3))
        smallinfo.append(sheet.cell_value(i, 4))
        smallinfo.append(sheet.cell_value(i, 5))
        smallinfo.append(sheet.cell_value(i, 6))
        info.append(smallinfo)

    info1 = []
    for i in range(1001,2001):
        smallinfo = []
        smallinfo.append(sheet.cell_value(i, 0))
        smallinfo.append(sheet.cell_value(i, 1))
        smallinfo.append(sheet.cell_value(i, 2))
        smallinfo.append(sheet.cell_value(i, 3))
        smallinfo.append(sheet.cell_value(i, 4))
        smallinfo.append(sheet.cell_value(i, 5))
        smallinfo.append(sheet.cell_value(i, 6))
        info1.append(smallinfo)
    # for i in info:
    #     print(i)
    return info,info1

#Age	Gender	Claim	tickets	 prior claims	atty	outcome

def processdata(processdata):
    #process age
    for item in processdata:
        if item[0] <= 20:
            item[0] = 0
        elif item[0] < 50:
            item[0] = item[0]/30
        else:
            item[0] = 1
    #process claim
    for item in processdata:
        item[2] = item[2]/5000

    #process tickets and prior claims
    for item in processdata:
        if item[3] == 0:
            pass
        elif item[3] == 1:
            item[3] = 0.5
        else:
            item[3] = 1

        if item[4] == 0:
            pass
        elif item[4] == 1:
            item[4] = 0.5
        else:
            item[4] = 1

    #process att:
    for item in processdata:
        if item[5] == 'none':
            item[5] = 0
        else:
            item[5] = 1
    return processdata


def writedata(listdata):
    index = len(listdata)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('fraulrawprocess.xls')
    for i in range(0, index):
        for j in range(0, len(listdata[i])):
            sheet.write(i,j,listdata[i][j])
    workbook.save('fraulrawprocess.xls')


a,b = getdata()
processdata(a)
processdata(b)
# for i in a:
#     print(i)
# writedata(a)

intercept = -0.01061
Agefactor = -0.00351
Genderfacotr = 0.001264
claimfactor = 0.069708
ticketsfactor = -0.03019
priorclaimfacotrs = -0.01504
attyfactory = 0.352672

logisticRegression = []
for item in b:
     y = intercept + Agefactor*item[0]+ Genderfacotr*item[1]\
         + claimfactor*item[2]+ ticketsfactor*item[3]\
         + priorclaimfacotrs*item[4]+ attyfactory*item[5]
     Pj = 1 / (1 + math.exp(0 - y))

     logisticRegression.append(Pj)


class1count = 0
class2count = 0
for i in  logisticRegression:
    if i < 0.5:
        class1count += 1
    else:
        class2count += 1

print('Test data have {} class1, and {} class2'.format(class1count,class2count))
for item in logisticRegression:
    print(item)



