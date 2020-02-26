# SILVER-seq data processing pipeline
Pipeline for preprocessing, alignment and report of SILVER-seq datasets.
This pipeline consists of three modules: 
1. a **preprocessing** module where a python script is applied to perform reads deduplication on fastq files 
2. an **alignment** module where the *exceRpt* software (Rozowsky et al., 2019) is applied to map the reads to different RNA features 
3. a **report** module where another python script is applied to parse the alignment results from exceRpt to generate a table of mapping statistics and a table of gene counts. The script is enabled to report results from one or multiple SILVER-seq datasets in the form of one mapping statisitcs table and one gene counts table. 
## Software Requirements
- Python 3.4 or later
- [exceRpt](http://github.gersteinlab.org/exceRpt/)
- [Docker](https://docs.docker.com/install/)

## Preprocssing
Three files are needed for this module: 
- SILVER-seq read fastq file `sample1.fastq` where `sample1` is the sample ID for this silver-seq dataset
- SILVER-seq read index file `sample1.index.fastq`
- deduplication python script `runDedup.py`

Create a working directory for example `/path/silverSeq/` to store related input and output files for this pipeline.
To perform deduplication on SILVER-seq read fastq file, open a terminal and run <br />
`python /path/silverSeq/runDedup.py /path/silverSeq/sample1.fastq /path/silverSeq/sample1.index.fastq /path/silverSeq/sample1.fastq.dedup` <br />
where `sample1.fastq.dedup` contains the deduplicated silver-seq reads that will be used for the downstream pipeline

## Alignment
This module follows the exceRpt small RNA-seq pipeline. [Here](http://github.gersteinlab.org/exceRpt/) is the installation instructions for exceRpt. The pre-compiled endogenenous genome and transcriptome indices of Human hg38 for is also needed for exceRpt to use, which can be downloaded [Here](http://org.gersteinlab.excerpt.s3-website-us-east-1.amazonaws.com/exceRptDB_v4_hg38_lowmem.tgz)
Create a sub-directory under the working directory for example `/path/silverSeq/excerptOutput/` to hold the output from exceRpt. The directory holding the downloaded genome and transcriptome indices is reffered as `/path/silverSeq/excerptHg38/`   
To map the SILVER-seq reads, open a terminal and run <br />
<pre><code>
docker run -v /path/silverSeq/:/exceRptInput \
           -v /path/silverSeq/excerptOutput/sample1/:/exceRptOutput \
           -v /path/silverSeq/excerptHg38:/exceRpt_DB/hg38 \
           -t rkitchen/excerpt \
           TRIM_N_BASES_3p=25 \
           INPUT_FILE_PATH=/exceRptInput/sample1.fastq.dedup \
           ADAPTER_SEQ=none \
           N_THREADS=10 \
           STAR_outFilterMatchNminOverLread=0.66 \
           STAR_outFilterMismatchNmax=10
           
</code></pre>
While the value of `N_THREADS` parameter in the above command can be adjusted accorodingly, we do not recrommand to change the value of other parameters. After the mapping process finishes, the output is held under the directory of `/path/silverSeq/excerptOutput/sample1/`

## Report
`reportSilverSeq.py` is needed for this module.

If you have mapping results of multiple silver-seq libraries, put all exceRpt output subdirectories under a same directory for example `/path/silverSeq/excerptOutput/` so that the directory architerture will look like
<pre><code>
/path/silverSeq/excerptOutput/
           --sample1/
           --sample2/
           --sample3/
           ...
           ...
</code></pre>
To get gene counts of these SILVER-seq libraries, run the following command <br />
`python /path/silverSeq/reportSilverSeq.py /path/silverSeq/excerptHg38 /path/silverSeq/excerptOutput prefix` <br /> where `prefix` is the prefix you want to add to your output files.
A file named as `mappingStats.csv` will be output as the mapping statsitics table derived from the SILVER-seq libraries. A file named as `geneCounts.csv` will be output as the gene counts table derived from the SILVER-seq libraries.



