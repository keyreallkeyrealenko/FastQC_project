# FastQC reverse engineering

## Description

This project was done as a homework at the Bioinformatics Institute, it copies the functionality of the __FastQC__
project. Our goal is to repeat the work of the FastQC program with the output of basic statistics, plots and tables,
the same as that performed by FastQC. 4 students participated in the project:
1) Kirill Kirilenko – performed first three tasks (__Basic Statistics, Per base sequence quality, Per sequence quality scores__)
2) Semyon Kupriyanov - ...
3) Mikhail Slizen - ...




### GC content
The function create_gc_base_n_graphs(sequence, path_to_dir) takes list of sequences and path to output file.
This function creates three graphs: Per base N content, Per base sequence content and Per sequence GC content.

### duplications
This script uses as input list of lines from fastafile with sequqncing results (4 lines for a read) and output dir. 
This function:
- saves one plot of levels of duplication
- saves one TSV with overrepresented sequences, each of wich take at least 0.1% of all reads, their count and percentage.
- returns results for test of duplication level and test for overrepresented seqs

