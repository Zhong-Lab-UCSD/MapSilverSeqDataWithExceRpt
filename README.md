# Silver-seq data processing pipeline
Pipeline for preprocessing, alignment and report of silver-seq datasets.
This pipeline consists of three modules: 
1. a **preprocessing** module where a python script is applied to perform reads deduplication on fastq files 
2. an **alignment** module where the *exceRpt* software (Rozowsky et al., 2019) is applied to map the reads to different RNA features 
3. a **report** module where another python script is applied to parse the alignment results from exceRpt to generate a table of gene expressions in terms of TPM
## Software Requirements
- Python 3.4 or later
- [exceRpt](http://github.gersteinlab.org/exceRpt/)
- [Docker](https://docs.docker.com/install/)

## Preprocssing
Three files are needed for this module: 
- silver-seq read fastq file `read1.fastq`
- silver-seq read index file `index.fastq`
- deduplication python script `runDedup.py`

Create a working directory for example `/path/silverSeq/` to store related input and output files for this pipeline.
To perform deduplication on silver-seq read fastq file, open a terminal and run <br />
`python /path/silverSeq/runDedup.py /path/silverSeq/read1.fastq /path/silverSeq/index.fastq /path/silverSeq/read1.dedup.fastq` <br />
where `read1.dedup.fastq` contains the deduplicated silver-seq reads that will be used for the downstream pipeline

## Alignment
This module follows the exceRpt small RNA-seq pipeline. [Here](http://github.gersteinlab.org/exceRpt/) is the installation instructions for exceRpt. The pre-compiled endogenenous genome and transcriptome indices of Human hg38 for is also needed for exceRpt to use, which can be downloaded [Here](http://org.gersteinlab.excerpt.s3-website-us-east-1.amazonaws.com/exceRptDB_v4_hg38_lowmem.tgz)
Create a sub-directory under the working directory for example `/path/silverSeq/excerptOutput/` to hold the output from exceRpt. The directory of downloaded genome and transcriptome indices is reffered as `/path/silverSeq/excerptHg38/`   
To map the silver-seq reads, open a terminal and run <br />
<pre><code>
docker run -v /path/silverSeq/:/exceRptInput \
           -v /path/silverSeq/excerptOutput/:/exceRptOutput \
           -v /path/silverSeq/excerptHg38:/exceRpt_DB/hg38 \
           -t rkitchen/excerpt \
           TRIM_N_BASES_3p=25 \
           INPUT_FILE_PATH=/exceRptInput/read1.dedup.fastq \
           ADAPTER_SEQ=none \
           STAR_outFilterMatchNminOverLread=0.66 \
           STAR_outFilterMismatchNmax=10
           
</code></pre>


## Report
`computeGeneExpression.py` is needed for this module

To get gene expressions of the silver-seq library, open a terminal and run <br />
`python /path/to/computeGeneExpression.py //path/silverSeq/excerptHg38 /path/to/excerptOut` <br />
A file named as `TPM.csv` will be output to `/path/to/excerptOut` directory as the gene expression table derived from the silver-seq library.



