# FASTQC reverse engineering

## per_sequence_gc_content
The function per_sequence_gc_content(sequence, path_to_dir) takes list of sequences and path to output file.
This function plots the dependence of the distribution density of reads on the GC content in percent.

## per_base_sequence_content
The function per_base_sequence_content(sequence, path_to_dir) takes list of sequences and path to output file.
This function plots the dependence of the percentage of base content on the position in the read.

## per_base_n_content
The function per_base_n_content(sequence, path_to_dir) takes list of sequences and path to output file.
This function plots the dependence of the percentage of the content of undetermined bases (N) on the position in the read.

## duplications
This script uses as input list of lines from fastafile with sequqncing results (4 lines for a read) and output dir. 
This function:
- saves one plot of levels of duplication
- saves one TSV with overrepresented sequences, each of wich take at least 0.1% of all reads, their count and percentage.
- returns results for test of duplication level and test for overrepresented seqs

