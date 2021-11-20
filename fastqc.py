# It is the main script. It reads Fastq file as input (-i) from a command line
# and then executes all imported functions and save all plots, tables to output (-o) directory
import argparse
from basic_statistics import basic_statistics

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help='directory to .fastq file to execute', required=True)
parser.add_argument('-o', '--output', help='directory to store all the resulting'
                                           ' files (default – current dir)', default='.')
args = parser.parse_args()

input_file = args.input
output_dir = args.output

with open(input_file) as f:
    file = f.readlines()


def main():
    basic_statistics(file, input_file, output_dir)


if __name__ == '__main__':
    main()
