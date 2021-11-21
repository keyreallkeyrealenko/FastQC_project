# It is the main script. It reads Fastq file as input (-i) from a command line
# and then executes all imported functions and save all plots, tables to output (-o) directory
import argparse
import os
from basic_statistics import basic_statistics
from boxplots import compile_quality
from duplications import duplications
from sequence_length_distribution import sequence_length_distribution
from adapter_content import adapter_content
from Fastq_graph import per_base_n_content, per_base_sequence_content, per_sequence_gc_content
from Bio import SeqIO

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help='directory to .fastq file to execute', required=True)
parser.add_argument('-o', '--output', help='directory to store all the resulting'
                                           ' files (default – current dir)', default='.')
args = parser.parse_args()

input_file = args.input
output_dir = args.output

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file) as f:
    file = f.readlines()

sequence = []
for record in SeqIO.parse(path_to_file, "fastq"):
    sequence += [record.seq]


def main():
    basic_statistics(file, input_file, output_dir)
    boxplot_test, per_quality_ps_test = compile_quality(file, output_dir)
    duplications_test, overrepresented_test = duplications(file, output_dir)
    sequence_length_distribution(sequence, output_dir)
    adapter_content(sequence, output_dir)
    # base_n_content_test = per_base_n_content(file, output_dir)
    per_base_n_content(sequence, output_dir)
    # base_sequence_content_test = per_base_sequence_content(file, output_dir)
    per_base_sequence_content(sequence, output_dir)
    # sequence_gc_content_test = per_sequence_gc_content(file, output_dir)
    per_sequence_gc_content(sequence, output_dir)


if __name__ == '__main__':
    main()
