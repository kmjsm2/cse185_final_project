# quantgene
`quantgene` takes in file with relative gene expression units as a input and outputs file including converted TPM value or scatter plot of TPM values based on the user's choice.
## Download 
To download this tool, clone this repository:
```
git clone https://github.com/kmjsm2/cse185_final_project
```
Then change the current folder to cse185_final_project by:
```
cd cse185_final_project
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
quantgene {scatter,convert} [-h] [--p_title P_TITLE] [--o_title O_TITLE] file1 [file2] out_dir
```
```
required arguments:
  {scatter,convert}  Mode of operation: scatter for scatter plot, convert for gene expression conversion
  file1              Path to the first gene.results file
  file2              Path to the second gene.results file (not required for convert mode)
  out_dir            Directory to save the output plot or converted files
options:
  -h, --help         show this help message and exit
  --p_title P_TITLE  Title of the scatter plot
  --o_title O_TITLE  Title of the scatter plot.png
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
