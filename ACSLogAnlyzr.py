#!/usr/bin/env python

defaultInputFileLocation=r'D:\ACS-LOG-Analysis\inp'
inpFileName= input("please inter your log file's name: ")
fullInputFilePath=defaultInputFileLocation+"\\"+inpFileName
fpr=open(fullInputFilePath)
#fpr=open("2015-01-05") #for Linux


logDic={}
logFormat=[]
lineCount=0
errorTypeCount=0
warnTypeCount=0
noticeTypeCount=0

def lineCounter(): 
    global lineCount
    lineCount=lineCount+1

    
def typeCounter():
    global errorTypeCount
    global warnTypeCount
    global noticeTypeCount
    if ls[nIndex] not in logFormat:
            logFormat.append(ls[nIndex])
    if ls[nIndex]=="ERROR":
        errorTypeCount+=1
    elif ls[nIndex]=="WARN":
        warnTypeCount+=1
    elif ls[nIndex]=="NOTICE":
        noticeTypeCount+=1
                
def typeRecognz(firstPartStr):  # must be passed by ls2[0] ,because this part
                                # of string include NOTICE WARN ERROR Type
    LogType=''
    if firstPartStr.find("NOTICE")!=-1:
        LogType="NOTICE"
    elif firstPartStr.find("WARN")!=-1:
        LogType="WARN"
    elif firstPartStr.find("ERROR")!=-1:
        LogType="ERROR"
    return LogType

def propert(t):
    eqIndex=t.find("=")
    if eqIndex==-1:
        return ['null','null']
    else:
        properties=t[0:eqIndex]
        value=t[eqIndex+1 :]
        if properties!='':
            if properties[0]==" ":
                properties=properties[1:]
            if properties[0]==" ":
                properties=properties[1:]
            if properties[-1]==" ":
                properties=properties[0:-1]
            if properties[-1]==" ":
                properties=properties[0:-1]
        if value!='':
            if value[0]==" ":
                value=value[1:]
            if value[0]==" ":
                value=value[1:]
            if value[-1]==" ":
                value=value[0:-1]
            if value[-1]==" ":
                value=value[0:-1]
        
        return [properties,value]

def firstPartResultRecogz(firstPart):
    Index=0
    if firstPart.find("NOTICE")!= -1:
        Index=firstPart.find("NOTICE")+7
    if firstPart.find("WARN")!= -1:
        Index=firstPart.find("WARN")+5
    if firstPart.find("ERROR")!= -1:
        Index=firstPart.find("ERROR")+6
    firstPart=firstPart[Index:]
    Index=firstPart.find(":")
    command=firstPart[0:Index]
    if command!='':
            if command[0]==" ":
                command=command[1:]
            if command[0]==" ":
                command=command[1:]
            if command[-1]==" ":
                command=command[0:-1]
            if command[-1]==" ":
                command=command[0:-1]
    arg=firstPart[Index+1 :]
    if arg!='':
            if arg[0]==" ":
                arg=arg[1:]
            if arg[0]==" ":
                arg=arg[1:]
            if arg[-1]==" ":
                arg=arg[0:-1]
            if arg[-1]==" ":
                arg=arg[0:-1]
    return [command ,arg]


line=fpr.readline()
print("Orginal Log File Processing To Make a File With \nOne Line Per Each Log started\n*************************************************")
while line:
    line=line.strip()
    lineCounter()
    ls=line.split(" ")
   
    if ls[9] in ['0','1','2','3']:
        i=ls[7]
        n=int(ls[9])
        nIndex=15
        lstemp=ls[10:]
    else:
        i=ls[6]
        n=int(ls[8])
        nIndex=14
        lstemp=ls[9:]
    if i not in logDic:
        x=["","","","",""]
        if n==0:
            x[n]=line
            logDic[i]=x
        else:
            y=''.join(lstemp)
            x[n]=y
            logDic[i]=x
    else:
        x=logDic[i]
        if n==0:
            x[n]=line
            logDic[i]=x
        else:
            y=''.join(lstemp)
            x[n]=y
            logDic[i]=x
    if n==0:
        typeCounter()
        
    line=fpr.readline()
fpr.close()
print("A Dictionary of Log Sequence Number and Value of \na List of 3 Line Log Detail Created")    
print("Log Type in This file :",logFormat)
print ("error Type count is :",errorTypeCount,"\nwarn type count is :",warnTypeCount,"\nNotice type Count is :",noticeTypeCount)
print("Number Of Items in Dictionary :",len(logDic))


defaultOutputFileLocation=r'D:\ACS-LOG-Analysis\oup'
fullOutputFilePath=defaultOutputFileLocation+"\\"+inpFileName+" OneLinePerEachLog"
fpw=open(fullOutputFilePath,"w")
#fpw=open("2015-01-05-OneLinePerEachLog","w") #for Linux
print("Making a New log File in OUP Path with One \nLine Per Each Log Is Started\n*************************************************")
logWithoutFirstPart=0
for k,v in logDic.items():
    if v[0]!='':
        strline=str(v[0])+str(v[1])+str(v[2])+str(v[3])+"\n"
        fpw.write(strline)
    else:
        logWithoutFirstPart+=1
print("Number of Logs Without first part : ",logWithoutFirstPart)
fpw.close()

      
fpr2=open(fullOutputFilePath)
lineR=fpr2.readline()
lineCountR=0
dataBaseDic={}
columnList=[]
print("Opening OUP File To Make Final Data Base Of \nLog Properties Started\n*************************************************")
while lineR:
    logPropertiesDic={}
    lineCountR+=1
    lineR=lineR.strip()
    lsC=lineR.split(",")
    lsS=lineR.split(" ")
    firstPartlsC=lsC[0].split()
    date=firstPartlsC[0]
    logTime=firstPartlsC[1]
    logType=typeRecognz(lsC[0])
    
    if lsS[9] in ['0','1','2','3']:
        i=lsS[7]
        nIndex=15
    else:
        i=lsS[6]
        nIndex=14
    
    FirstPartTypeComand=firstPartResultRecogz(lsC[0])
    logPropertiesDic['LogSeqNum']=i
    logPropertiesDic['Date']=date
    logPropertiesDic['Time']=logTime
    logPropertiesDic['MessageType']=logType
    logPropertiesDic['LogCategory']=FirstPartTypeComand[0]
    logPropertiesDic['LogCategoryParam']=FirstPartTypeComand[1]
    
    for j in lsC :
        temp=propert(j)
        logPropertiesDic[temp[0]]=temp[1]
    for k,v in  logPropertiesDic.items():
        if k not in columnList:
            columnList.append(k)
    dataBaseDic[i]=logPropertiesDic
    
    lineR=fpr2.readline()
fpr2.close()
print("Your Log Processed and A Data Base With \nDictionary Format Made. To See this Data Base Enter \ndataBaseDic As a Command In Your Python Interpreter")
print ("To See The Column Of Your Data Base Type \ncolumnList As a Command In Your Python Interpreter")
print("Line Of OUP Log File To Validation : ",lineCountR)
print("*************************************************")
input("press any key to exit")


    
 

