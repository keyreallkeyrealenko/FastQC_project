#!/usr/bin/env python
# coding: utf-8

# In[90]:


import pandas as pd
import matplotlib.pyplot as plt


def duplications(all_reads, outdir):
    # This script uses as input list of lines from fastafile with sequqncing results (4 lines
    # for a read) and output dir.
    # This function:
    # - saves one plot of levels of duplication
    # - saves one TSV with overrepresented sequences, each of wich take at least 0.1%
    # of all reads, their count and percentage.
    # - returns results for test of duplication level and test for overrepresented seqs
    #
    # :args all_reads - list of lines from fastafile with sequqncing results
    # :args outdir - dir for output files
    def which_cutoff(df):
        # which_cutoff function assigns group to each unique sequence by number of its' copies
        #
        # :args df - dataframe with counts of unique sequences
        if df['Count'] > 10000:
            return '>10k'
        elif df['Count'] > 5000:
            return '>5k'
        elif df['Count'] > 1000:
            return '>1k'
        elif df['Count'] > 500:
            return '>500'
        elif df['Count'] > 100:
            return '>100'
        elif df['Count'] > 50:
            return '>50'
        elif df['Count'] >= 10:
            return '>10'
        else:
            return str(int(df['Count']))

    def draw_plot(reads_df, n_of_reads, unique_percentage, outdir):
        #  draw_plot function saves plot of number of duplicated and deduplicated sequences
        #  by duplication level in orogonal set of reads.
        #  :args reads_df - pandas dataframe with unique sequence, their count and assigned
        #  cutoff group
        #  :args n_of_reads - number of reads in original set
        #  :args unique_percentage - percentage of unique seqs in original set
        #  :args outdir - path for saving plot
        reads_df['Cutoff'] = reads_df.apply(which_cutoff, axis=1)
        coords_dup = reads_df.groupby('Cutoff').sum('Count')
        coords_dup['Percentage'] = 100 * coords_dup['Count'] / n_of_reads
        coords_dup = coords_dup.drop(columns='Count')
        coords_dedup = reads_df.groupby('Cutoff').count()
        coords_dedup['Percentage'] = 100 * coords_dedup['Count'] / len(reads_df)
        coords_dedup = coords_dedup.drop(columns='Count')
        groups = [str(i) for i in range(1, 10)]
        groups.extend(['>10', '>50', '>100', '>500', '>1k', '>5k', '>10k'])
        graph_df = pd.DataFrame(0, index=groups, columns=['% Total sequences',
                                                          '% Deduplicated sequences'])
        for i in coords_dup.index:
            graph_df.loc[i, '% Total sequences'] = coords_dup.loc[i, 'Percentage']
            graph_df.loc[i, '% Deduplicated sequences'] = coords_dedup.loc[i, 'Percentage']
        # Plot construction starts here
        graph_df.plot(color=['blue', 'red'], figsize=(10, 8))
        plt.ylim(0, 100)
        plt.margins(x=0)
        plt.xticks(range(len(graph_df)), groups)
        for i in range(0, len(graph_df), 2):
            plt.axvspan(i, i+1, color='lightgrey')
        plt.title(f'Percentage of seqs remaining if deduplicated {round(unique_percentage*100, 2)}%')
        plt.grid(True, axis='x')
        plt.grid(True, axis='y', color='grey')
        plt.xlabel('Sequence Duplication Level')
        plt.savefig(outdir + '/duplications.png')

    def test_dupl_lvl(not_unique_percentage):
        # test for duplication level
        # :args not_unique_percentage - percentage of nonunique seqs in original set
        # Failed - > 50% of nonunique
        # Warning - between 20% and 50% of nonunique
        if not_unique_percentage < 0.2:
            return 'P'
        elif not_unique_percentage < 0.5:
            return 'W'
        else:
            return 'F'

    def test_overrepresented(max_represented):
        # test for duplication level
        # :args not_unique_percentage - percentage of nonunique seqs in original set
        # Failed - one sequence represents more then 1% of total number of reads
        # Warning - one sequence represent between 0.1% and 1% of total number of reads
        if max_represented < 0.1:
            return 'P'
        elif max_represented < 1:
            return 'W'
        else:
            return 'F'

    n_of_reads = len(all_reads) // 4
    # long reads are trimmed down to 50 nucleotides
    reads_df = pd.DataFrame(data=[i[:50] if len(i) > 75 else i for i in all_reads[1::4]],
                            columns=['Sequence'])
    reads_df = reads_df.value_counts('Sequence').to_frame('Count')
    reads_df['Percentage'] = 100 * reads_df['Count'] / n_of_reads
    max_represented = max(reads_df['Percentage'])
    overrepresented_test = test_overrepresented(max_represented)
    overrepresnted_df = reads_df[reads_df['Percentage'] >= 0.1]
    overrepresnted_df.to_csv(path_or_buf=f'{outdir}/overrepresented.tsv', sep='\t')
    unique_percentage = len(reads_df) / n_of_reads
    dupl_test = test_dupl_lvl(1 - unique_percentage)
    draw_plot(reads_df, n_of_reads, unique_percentage, outdir)
    return dupl_test, overrepresented_test

if __name__ == '__main__':
    with open('SRR1705851.fastq') as f:
        file = f.readlines()
    outdir = './'
    duplications(file, outdir)

