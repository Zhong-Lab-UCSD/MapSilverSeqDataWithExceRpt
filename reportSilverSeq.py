import glob
import numpy as np
import sys



geneList=set()                    
with open('%s/STAR_INDEX_transcriptome/chrName.txt'%(sys.argv[1]),'r') as f:
    for line in f:
        if 'miRNA'==line[:5]:
            splitLine=line.strip().split(':')
            geneList.add(splitLine[1])
        if 'circRNA'==line[:7]:
            splitLine=line.strip().split(':')
            geneList.add(splitLine[1])
        if 'piRNA'==line[:5]:
            splitLine=line.strip().split('|')
            geneList.add(splitLine[0][6:])
        if 'gencode'==line[:7]:
            splitLine=line.strip().split(':')
            geneList.add(splitLine[3][:-4])
                    
geneList=list(geneList)
geneList.sort()

sampleIdList=[]
fileList=glob.glob('%s/*'%(sys.argv[2]))
fileNum=len(fileList)
for file in fileList:
    splitLine=file.split('/')
    sampleId=splitLine[-1]
    sampleIdList.append(sampleId)
sampleIdList.sort()

dicGene_Count={}
for gene in geneList:
    dicGene_Count[gene]=np.zeros(fileNum)
    
    
i=-1
for sampleId in sampleIdList:
    i+=1
    
    
    fileList=glob.glob('%s/%s/*/readCount*geneLevel.txt'%(sys.argv[2],sampleId))
    for file in fileList:
        with open(file,'r') as f:
            next(f)
            for line in f:
                splitLine=line.strip().split('\t')
                geneName=splitLine[0]
                dicGene_Count[geneName][i]+=float(splitLine[3])
            
#get miRNA infos
    fileList=glob.glob('%s/%s/*/readCounts_piRNA_*.txt'%(sys.argv[2],sampleId))
    for file in fileList:
        with open(file,'r') as f:
            next(f)
            for line in f:
                splitLine=line.strip().split('\t')
                info=splitLine[0].split('|')
                geneName=info[0]
                dicGene_Count[geneName][i]+=float(splitLine[3])

    fileList=glob.glob('%s/%s/*/readCounts_circRNA_*.txt'%(sys.argv[2],sampleId))
    for file in fileList:
        with open(file,'r') as f:
            next(f)
            for line in f:
                splitLine=line.strip().split('\t')
                info=splitLine[0].split('|')
                geneName=info[0]
                dicGene_Count[geneName][i]+=float(splitLine[3])
            
    fileList=glob.glob('%s/%s/*/readCounts_miRNA*.txt'%(sys.argv[2],sampleId))
    for file in fileList:
        with open(file,'r') as f:
            next(f)
            for line in f:
                splitLine=line.strip().split('\t')
                info=splitLine[0].split(':')
                geneName=info[0]
                geneName=geneName.lower()
                if '3p' in geneName or '5p' in geneName:
                    geneName=geneName[:-3]
                #dicGene_Count_unique[geneName][i]+=float(splitLine[1])
                try:
                    dicGene_Count[geneName][i]+=float(splitLine[3])
                except KeyError:
                    geneName=geneName+'-1'
                    try:
                        dicGene_Count[geneName][i]+=float(splitLine[3])
                    except KeyError:
                        geneName=geneName[:-2]+'a'
                        try:
                            dicGene_Count[geneName][i]+=float(splitLine[3])
                        except KeyError:
                            pass
            
targetFile=open('%sgeneCounts.csv'%(sys.argv[3]),'w')
targetFile.write('Gene,')
ha=','.join(sampleIdList)
targetFile.write(ha)
targetFile.write('\n')
for gene in geneList:
    targetFile.write('%s,'%(gene))
    ha=','.join([str(x) for x in dicGene_Count[gene]])
    targetFile.write(ha)
    targetFile.write('\n')
    
targetFile.close()


featureList=['#Input','#Filtered_Input','#Genome','#Transcriptome','GenomeFilteredInputRatio','TranscriptomeGenomeRatio',
             'TranscriptomeComplexity','#gencode','#miRNA','#tRNA','#piRNA','#circularRNA']
dicGene_Mapping={}
for feature in featureList:
    dicGene_Mapping[feature]=np.zeros(fileNum)
i=-1
for sampleId in sampleIdList:
    i+=1
    fileList=glob.glob('%s/%s/*.stats'%(sys.argv[2],sampleId))
    for file in fileList:
        with open(file,'r') as f:
            tempSum=0
            for line in f:
                splitLine=line.strip().split('\t')
                if 'miRNA' in splitLine[0]:
                    dicGene_Mapping['#miRNA'][i]+=int(splitLine[1])
                    tempSum+=int(splitLine[1])
                if 'tRNA' in splitLine[0]:
                    dicGene_Mapping['#tRNA'][i]+=int(splitLine[1])
                    tempSum+=int(splitLine[1])
                if 'piRNA' in splitLine[0]:
                    dicGene_Mapping['#piRNA'][i]+=int(splitLine[1])
                    tempSum+=int(splitLine[1])
                if 'gencode' in splitLine[0]:
                    dicGene_Mapping['#gencode'][i]+=int(splitLine[1])
                    tempSum+=int(splitLine[1])
                if 'circularRNA' in splitLine[0]:
                    dicGene_Mapping['#circularRNA'][i]+=int(splitLine[1])
                    tempSum+=int(splitLine[1])
                if 'genome'==splitLine[0]:
                    dicGene_Mapping['#Genome'][i]+=int(splitLine[1])
                    a=int(splitLine[1])
                if 'input'==splitLine[0]:
                    dicGene_Mapping['#Input'][i]+=int(splitLine[1])
                if 'reads_used_for_alignment'==splitLine[0]:
                    dicGene_Mapping['#Filtered_Input'][i]+=int(splitLine[1])
                    b=int(splitLine[1])
            dicGene_Mapping['#Transcriptome'][i]=tempSum
            dicGene_Mapping['GenomeFilteredInputRatio'][i]=a*1.0/b
            dicGene_Mapping['TranscriptomeGenomeRatio'][i]=tempSum*1.0/a
            
    fileList=glob.glob('%s/%s/*.qcResult'%(sys.argv[2],sampleId))
    for file in fileList:
        with open(file,'r') as f:
            for line in f:
                splitLine=line.strip().split(':')
                if 'TranscriptomeComplexity'in line:
                    dicGene_Mapping['TranscriptomeComplexity'][i]=float(splitLine[1])
            

targetFile=open('%smappingStats.csv'%(sys.argv[3]),'w')
targetFile.write('Feature,')
ha=','.join(sampleIdList)
targetFile.write(ha)
targetFile.write('\n')
for feature in featureList:
    targetFile.write('%s,'%(feature))
    ha=','.join([str(x) for x in dicGene_Mapping[feature]])
    targetFile.write(ha)
    targetFile.write('\n')
    
targetFile.close()
                



