import json
import urllib
import re

capMin=50 #minimum capacity in GB
ids=[]
for page in range(1,6):
    data = {
        "NValue": "", 
        "StoreDepaId": 1, 
        "NodeId": 11693, 
        "BrandId": -1, 
        "PageNumber": 1,
        "Sort": "PRICE",
        "CategoryId": 636,
        "PageNumber": page
    }
    params = json.dumps(data).replace("null", "-1")
    f = urllib.urlopen("http://www.ows.newegg.com/Search.egg/Advanced", params)

    a=json.load(f)["ProductListItems"]
    for i in a:
       ids.append([i["ItemNumber"],i["FinalPrice"]])
finalspecs=[]
def chksize(j):
    capacitySpecs=js["SpecificationGroupList"][1]["SpecificationPairList"]
    for spec in capacitySpecs:
        if spec["Key"]=="Capacity":
            cap=int(re.search('\d+',spec["Value"]).group(0))
            if cap>=capMin-1:
                return True
            else:
                return False
for itemN in ids:
    f = urllib.urlopen("http://www.ows.newegg.com/Products.egg/"+itemN[0]+"/Specification")
    js=json.load(f)
    neweggItemNumber=js["NeweggItemNumber"]
    specs=js["SpecificationGroupList"][2]["SpecificationPairList"]
    if not chksize(js["SpecificationGroupList"][1]["SpecificationPairList"]):
        continue
    write=0
    read=0
    price=float(itemN[1][1:])
    for spec in specs:
        if spec["Key"]=="Sustained Sequential Write":
            write=int(re.search('\d{2,}',spec["Value"]).group(0))
        elif spec["Key"]=="Sustained Sequential Read":
            read=int(re.search('\d{2,}',spec["Value"]).group(0))
    finalspecs.append([neweggItemNumber,price,read,write])
bestAvg=["",100]
bestRead=["",100]
bestWrite=["",100]
for i in finalspecs:
    if i[2]==0:
        i[2]=1
    if i[3]==0:
        i[3]=1
    avg=float(i[1])/float(((i[2]+i[3])/2))
    read=float(i[1])/float((i[2]))
    write=float(i[1])/float((i[3]))
    if(avg<bestAvg[1]):
        bestAvg[1]=avg
        bestAvg[0]=i[0]
    if(read<bestRead[1]):
        bestRead[1]=read
        bestRead[0]=i[0]
    if(write<bestWrite[1]):
        bestWrite[1]=write
        bestWrite[0]=i[0]
print "best overall: "+bestAvg[0]+"\n"+"best read: "+bestRead[0]+"\n"+"best write: "+bestWrite[0]
    

