from collections import defaultdict
import sys

dicReadId_index={}
count=0
with open('%s'%(sys.argv[2]),'r') as f:
    for line in f:
        count+=1
        if count==1:
            splitLine=line.strip().split()
            readId=splitLine[0][1:]
        if count==2:
            dicReadId_index[readId]=line[:-1]
        if count==4:
            count=0
            
dicCombo_count=defaultdict(int)
#dicReadId_sequence
count=0
temp=[]
writeFlag=False
targetFile=open('%s'%(sys.argv[3]),'w')
with open('%s'%(sys.argv[1]),'r') as f:
    for line in f:
        temp.append(line)
        count+=1
        if count==1:
            splitLine=line.strip().split()
            readId=splitLine[0][1:]
            index=dicReadId_index[readId]
        if count==2:
            sequence=line[:-1]
            combo=';'.join([sequence,index])
            if dicCombo_count[combo] ==0:
                writeFlag=True
            dicCombo_count[combo]+=1
        if count==4:
            if writeFlag:
                for ha in temp:
                    targetFile.write(ha)
            writeFlag=False
            temp=[]
            count=0
targetFile.close()
print ('haha')