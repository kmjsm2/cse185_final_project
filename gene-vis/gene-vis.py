import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_and_merge_gene_results(file_path1, file_path2):
    """
    Read and merge gene expression results from two specified files.
    :param file_path1: Path to the first .gene.results file
    :param file_path2: Path to the second .gene.results file
    :return: Merged DataFrame with gene expression data
    """
    try:
        data1 = pd.read_csv(file_path1, sep='\t')
        data2 = pd.read_csv(file_path2, sep='\t')
        data_merged = pd.merge(data1, data2, on="gene_id", suffixes=("_Rep1", "_Rep2"))
        return data_merged
    except Exception as e:
        print(f"Error reading or merging gene results files: {e}")
        exit(1)

def generate_scatter_plot(data, x_column, y_column, title, output_file):
    """
    Generate a scatter plot from the data.
    :param data: DataFrame containing the merged data
    :param x_column: Column name for x-axis
    :param y_column: Column name for y-axis
    :param title: Title of the plot
    :param output_file: Path to save the output plot
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_column], data[y_column], alpha=0.5)
    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(prog="gene-vis",
                                     description="Command-line script to create scatter plot from two inputs of gene.results files")
    parser.add_argument('gene_results_file1', type=str, help='Path to the first gene.results file')
    parser.add_argument('gene_results_file2', type=str, help='Path to the second gene.results file')
    parser.add_argument('output_directory', type=str, help='Directory to save the output plot')
    parser.add_argument('--x_column', type=str, default='TPM_Rep1', help='Column name for x-axis values in the merged data')
    parser.add_argument('--y_column', type=str, default='TPM_Rep2', help='Column name for y-axis values in the merged data')
    parser.add_argument('--plot_title', type=str, default='Gene Expression Comparison', help='Title of the scatter plot')
    
    args = parser.parse_args()
    
    # Read and merge the gene results files
    data_merged = read_and_merge_gene_results(args.gene_results_file1, args.gene_results_file2)
    
    # Generate scatter plot
    output_file_path = f"{args.output_directory}/scatter_plot.png"
    generate_scatter_plot(data_merged, args.x_column, args.y_column, args.plot_title, output_file_path)

if __name__ == '__main__':
    main()
