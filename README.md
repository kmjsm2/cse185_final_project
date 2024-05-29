# quantgene
`quantgene` takes in file with relative gene expression units as a input and outputs converted gene expression units.
## Installiation 
Installiation requires the `pandas`, `numpy`, and `matplotlib.pyplot` libraries to be installed. 

To install those libraries: 
```
pip install -r requirements.txt
```

After required libraries installed, install `quantgene` by below command: 
```
pip install .
```
## Basic usage
To run `quantgene` 
```
quantgene [-h] [--p_title P_TITLE] [--o_title O_TITLE] file1 file2 out_dir
```
```
required arguments:
  file1              Path to the first gene.results file
  file2              Path to the second gene.results file
  out_dir            Directory to save the output plot
options:
  -h, --help         show this help message and exit
  --p_title P_TITLE  Title of the scatter plot
  --o_title O_TITLE  Title of the scatter plot.png
```