import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_file_with_fallback(file_path):
    """
    Read a gene expression file, trying tab delimiter first and then comma delimiter if tab fails or column not found.
    :param file_path: Path to the gene.results file
    :return: DataFrame with gene expression data
    """
    try:
        data = pd.read_csv(file_path, sep='\t')
        data.columns = data.columns.str.strip()  # Remove any leading/trailing whitespace from column names
        if 'gene_id' not in data.columns:
            raise ValueError("gene_id column not found with tab delimiter")
    except (pd.errors.ParserError, ValueError):
        try:
            data = pd.read_csv(file_path, sep=',')
            data.columns = data.columns.str.strip()  # Remove any leading/trailing whitespace from column names
            if 'gene_id' not in data.columns:
                raise ValueError("gene_id column not found with comma delimiter")
        except (pd.errors.ParserError, ValueError) as e:
            print(f"Error reading file {file_path}: {e}")
            exit(1)
    return data

def read_and_merge_gene_results(file_path1, file_path2):
    """
    Read and merge gene expression results from two specified files.
    :param file_path1: Path to the first .gene.results file
    :param file_path2: Path to the second .gene.results file
    :return: Merged DataFrame with gene expression data
    """
    try:
        data1 = read_file_with_fallback(file_path1)
        data2 = read_file_with_fallback(file_path2)

        # Check if 'gene_id' column exists in both dataframes
        if 'gene_id' not in data1.columns:
            print(f"'gene_id' column not found in {file_path1}. Columns found: {data1.columns.tolist()}")
            exit(1)
        if 'gene_id' not in data2.columns:
            print(f"'gene_id' column not found in {file_path2}. Columns found: {data2.columns.tolist()}")
            exit(1)

        data_merged = pd.merge(data1, data2, on="gene_id", suffixes=("_Rep1", "_Rep2"))
        return data_merged
    except Exception as e:
        print(f"Error reading or merging gene results files: {e}")
        exit(1)

def generate_scatter_plot(data, x_column, y_column, title, output_file):
    """
    Generate a scatter plot from the data, transforming TPM values using log10.
    :param data: DataFrame containing the merged data
    :param x_column: Column name for x-axis
    :param y_column: Column name for y-axis
    :param title: Title of the plot
    :param output_file: Path to save the output plot
    """
    plt.figure(figsize=(10, 6))
    xvals = np.log10(data[x_column] + 1)  # Apply log10 transformation
    yvals = np.log10(data[y_column] + 1)  # Apply log10 transformation
    plt.scatter(xvals, yvals, alpha=0.5)
    plt.title(title)
    plt.xlabel(f"log10 {x_column}")
    plt.ylabel(f"log10 {y_column}")
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(prog="quantgene",
                                     description="Command-line script to create scatter plot from two inputs of gene.results files")
    parser.add_argument('file1', type=str, help='Path to the first gene.results file')
    parser.add_argument('file2', type=str, help='Path to the second gene.results file')
    parser.add_argument('out_dir', type=str, help='Directory to save the output plot')
    parser.add_argument('--x', type=str, default='TPM_Rep1', help='Column name for x-axis values in the merged data')
    parser.add_argument('--y', type=str, default='TPM_Rep2', help='Column name for y-axis values in the merged data')
    parser.add_argument('--p_title', type=str, default='Gene Expression Comparison', help='Title of the scatter plot')
    parser.add_argument('--o_title', type=str, default='TPM_Scatter_Plot.png', help='Name of the output scatter plot file')
    args = parser.parse_args()
    
    # Read and merge the gene results files
    data_merged = read_and_merge_gene_results(args.file1, args.file2)
    
    # Generate scatter plot
    output_file_path = f"{args.out_dir}/{args.o_title}"
    generate_scatter_plot(data_merged, args.x, args.y, args.p_title, output_file_path)

if __name__ == '__main__':
    main()