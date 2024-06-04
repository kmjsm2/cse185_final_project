# quantgene
`quantgene` takes in file with relative gene expression units as a input and outputs file including converted TPM value or scatter plot of TPM values based on the user's choice.
## Download 
To download this tool, clone this repository:
```
git clone https://github.com/kmjsm2/quantgene
```
Then change the current folder to quantgene by:
```
cd quantgene
```
## Installiation  
`quantgene` requires the `pandas`, `numpy`, and `matplotlib.pyplot` libraries to be installed. 

To install those libraries: 
```
pip install pandas numpy matplotlib
```

After required libraries installed, install `quantgene` by below command: 
```
pip install .
```
## Basic usage
To run `quantgene` 
```
quantgene [-h] [--x_label X_LABEL] [--y_label Y_LABEL] [--p_title P_TITLE] [--o_title O_TITLE] [--converted CONVERTED] [—input_dir INPUT_DIR]{scatter,convert} file1 [file2] out_dir
```
```
required arguments:
  {scatter,convert}  Mode of operation: scatter for scatter plot, convert for gene expression conversion
  file1              Path to the first gene.results file
  file2              Path to the second gene.results file (not required for convert mode)
  out_dir            Directory to save the output plot or converted files
options:
  -h, --help            show this help message and exit
  --x_label X_LABEL     Label for x-axis
  --y_label Y_LABEL     Label for y-axis
  --p_title P_TITLE     Title of the scatter plot
  --o_title O_TITLE     Name of the output scatter plot file
  --converted CONVERTED
                        Name of the output file for convert mode
  --input_dir INPUT_DIR
                        Directory containing input files for batch conversion
```
Example to use convert: 
```
quantgene convert benchmark/Chow_Rep1.genes.results ./
```
Above code will convert the FPKM value to TPM value. When the input already have existing column TPM like this input, it will generate new column as Calc_TPM, otherwise TPM. 

Example to use scatter:
``` 
quantgene scatter benchmark/Chow_Rep1.genes.results benchmark/Chow_Rep2.genes.results ./
```
Takes in two files with TPM value and save the image of scatter plot of TPM values. 
