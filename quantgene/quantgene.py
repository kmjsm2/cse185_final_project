"""
command-line script to quantify the gene expression level 
by enabling the unit coversion from FPKM to TPM ('convert') and generating the scatter plot that compares the TPM value for replicates
"""
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# Read a gene expression file, trying tab delimiter first and then comma delimiter if tab fails or column not found.
# param file_path: Path to the gene.results file
# return: DataFrame with gene expression data

def read_file_with_fallback(file_path):

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


# Read and merge gene expression results from two input files. (used for 'scatter' option)
# param file_path1: Path to the first input file
# param file_path2: Path to the second input file
# return: Merged DataFrame with gene expression data

def read_and_merge_gene_results(file_path1, file_path2):

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


# Generate a scatter plot from the data, transforming TPM values using log10.
# param data: DataFrame containing the merged data
# param x_column: Column name for x-axis
# param y_column: Column name for y-axis
# param title: Title of the plot
# param output_file: Path to save the output plot

def generate_scatter_plot(data, x_column, y_column, title, output_file, x_axis, y_axis):

    plt.figure(figsize=(10, 6))
    xvals = np.log10(data[x_column] + 1)  # Apply log10 transformation
    yvals = np.log10(data[y_column] + 1)  # Apply log10 transformation
    plt.scatter(xvals, yvals, alpha=0.5)
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig(output_file)
    plt.close()


# Convert FPKM to TPM. (used for 'convert' option)
# param fpkm: FPKM values
# return: TPM values

def fpkm_to_tpm(fpkm):

    sum_fpkm = np.sum(fpkm, axis=0)
    tpm = (fpkm / sum_fpkm) * 1e6
    return tpm


# Process all CSV files in the input directory, converting FPKM to TPM and saving with appropriate names.
# param input_dir: Directory containing the input files.
# param output_dir: Directory to save the output files.

def process_directory(input_dir, output_dir):

    for file_name in os.listdir(input_dir):
        if file_name.endswith('_fpkm.csv'):
            file_path = os.path.join(input_dir, file_name)
            data = read_file_with_fallback(file_path)
            tpm_data = fpkm_to_tpm(data.iloc[:, 1:].values)
            for i, col in enumerate(data.columns[1:]):
                data[f'TPM'] = tpm_data[:, i]
            output_file_name = file_name.replace('_fpkm.csv', '_converted.csv')
            output_file_path = os.path.join(output_dir, output_file_name)
            data.to_csv(output_file_path, index=False)
            print(f"Converted file saved to {output_file_path}")

def main():
    parser = argparse.ArgumentParser(prog="quantgene",
                                     description="Command-line script to create scatter plot from two inputs of gene.results files and convert from FPKM to TPM")
    parser.add_argument('mode', type=str, choices=['scatter', 'convert'], help='Mode of operation: scatter for scatter plot, convert for gene expression conversion')
    parser.add_argument('file1', type=str, help='Path to the first file, need to have column gene_id and FPKM for convert and TPM for scatter')
    parser.add_argument('file2', type=str, help='Path to the second file (not required for convert mode), need to have column TPM for scatter', nargs='?')
    parser.add_argument('out_dir', type=str, help='Directory to save the output plot or converted files')
    parser.add_argument('--x_label', type=str, help='Label for x-axis')
    parser.add_argument('--y_label', type=str, help='Label for y-axis')
    parser.add_argument('--p_title', type=str, help='Title of the scatter plot')
    parser.add_argument('--o_title', type=str, help='Name of the output scatter plot file')
    parser.add_argument('--converted', type=str, help='Name of the output file for convert mode')
    parser.add_argument('--input_dir', type=str, help='Directory containing input files for batch conversion, files must be ending with _fpkm.csv and each file have column gene_id and FPKM')
    args = parser.parse_args()

    file1_name = os.path.splitext(os.path.basename(args.file1))[0]

    if args.mode == 'scatter':
        # Read and merge the gene results files
        data_merged = read_and_merge_gene_results(args.file1, args.file2)
        file2_name = os.path.splitext(os.path.basename(args.file2))[0]
        x_label = args.x_label if args.x_label else f"TPM from {file1_name}"
        y_label = args.y_label if args.y_label else f"TPM from {file2_name}"
        title = args.p_title if args.p_title else f"Gene Expression {file1_name} vs {file2_name}"
        o_title = args.o_title if args.o_title else f"{file1_name} vs {file2_name}_scatter.png"

        # Generate scatter plot
        output_file_path = f"{args.out_dir}/{o_title}"
        generate_scatter_plot(data_merged, 'TPM_Rep1', 'TPM_Rep2', title, output_file_path, x_label, y_label)
        print(f"Scatter plot saved to {output_file_path}")
    elif args.mode == 'convert':
        if args.input_dir:
            process_directory(args.input_dir, args.out_dir)
        else:
            # Read the gene results file
            data = read_file_with_fallback(args.file1)
            if 'TPM' in data.columns:
                data['Calc_TPM'] = fpkm_to_tpm(data['FPKM'])
            else:
                tpm_data = fpkm_to_tpm(data.iloc[:, 1:].values)
                for i, col in enumerate(data.columns[1:]):
                    data[f'TPM'] = tpm_data[:, i]
            converted = args.converted if args.converted else f"{file1_name}_converted.csv"
            output_file_path = f"{args.out_dir}/{converted}"
            data.to_csv(output_file_path, index=False)
            print(f"Converted data saved to {output_file_path}")

if __name__ == '__main__':
    main()