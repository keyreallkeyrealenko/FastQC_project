# FastQC reverse engineering

<<<<<<< HEAD
## Description

This project was done as a Python homework at the Bioinformatics Institute, it copies the functionality of the __FastQC__
project. Our goal is to repeat the work of the FastQC program with the output of basic statistics, plots and tables,
the same as that performed by FastQC. It is a Python program. 4 contributors participated in the project:
1) Kirill Kirilenko – performed first three tasks (__Basic Statistics, Per base sequence quality, Per sequence quality scores__)
2) Semyon Kupriyanov - ...
3) Mikhail Slizen - ...
4) Ekaterina Vostokova - ...

## How to run the code

To run this code just follow these steps:
1) open working directory with command ```cd /path_to_folder/```
2) clone our repository: ```git clone https://github.com/keyreallkeyrealenko/FastQC_project.git```
3) create virtual environment: ```python3.9 -m venv venv```
4) activate virtual environment ```source venv/bin/activate```
5) install all required libraries ```pip install -r requirements.txt```
6) run script ```python3 fastqc.py -i path_to/input.fastq -o output_dir/```.
You can use both version --input or -i and --output or -o (as default -i set as current directory). --help or -h shows help
7) wait and enjoy:)


## The functions implemented in this project:

### Per base sequence quality
The function called compile_quality invokes both per base sequence quality and Per sequence quality scores.
Iy creates two plots: boxplots describe quality per base and lineplot describes mean quality per read.
### GC content
The function create_gc_base_n_graphs(sequence, path_to_dir) takes list of sequences and path to output file.
This function creates three graphs: Per base N content, Per base sequence content and Per sequence GC content.
=======
### per_sequence_gc_content
The function per_sequence_gc_content(sequence, path_to_dir) takes list of sequences and path to output file.
This function plots the dependence of the distribution density of reads on the GC content in percent.

### per_base_sequence_content
The function per_base_sequence_content(sequence, path_to_dir) takes list of sequences and path to output file.
This function plots the dependence of the percentage of base content on the position in the read.

### per_base_n_content
The function per_base_n_content(sequence, path_to_dir) takes list of sequences and path to output file.
This function plots the dependence of the percentage of the content of undetermined bases (N) on the position in the read.
>>>>>>> c74855cca315899708a0e1f416f6124614f10b83

### duplications
This script uses as input list of lines from fastafile with sequqncing results (4 lines for a read) and output dir. 
This function:
- saves one plot of levels of duplication
- saves one TSV with overrepresented sequences, each of wich take at least 0.1% of all reads, their count and percentage.
- returns results for test of duplication level and test for overrepresented seqs

## adapter_content
This function uses list of sequences and path to output file. It has 4 adapter sequences and finds out the percentage of these adapters in reads.
Then it plots this percentage over the length of one read.

## sequence_length_distribution
This function uses list of sequences and path to output file. It checks if all sequences are of the same length and builds the distribution.
