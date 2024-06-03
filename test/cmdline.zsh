#!/bin/zsh

# Example usage
echo "Example usage:"
echo "  $0 scatter /path/to/first_file /path/to/second_file /path/to/output_directory --p_title 'My Scatter Plot' --o_title 'scatter_plot.png'"
echo "  $0 convert /path/to/fpkm_file /path/to/output_directory --conversion fpkm_to_tpm"
echo

# Usage function to display help
usage() {
  echo "Usage: $0 mode file1 [file2] out_dir [options]"
  echo
  echo "Modes:"
  echo "  scatter  - Create a scatter plot from two gene results files"
  echo "  convert  - Convert gene expression values (FPKM to TPM or TPM to FPKM)"
  echo
  echo "Arguments:"
  echo "  mode     - Mode of operation: scatter or convert"
  echo "  file1    - Path to the first gene.results file"
  echo "  file2    - Path to the second gene.results file (required for scatter mode)"
  echo "  out_dir  - Directory to save the output plot or converted files"
  echo
  echo "Options:"
  echo "  --p_title    - Title of the scatter plot (optional, scatter mode only)"
  echo "  --o_title    - Name of the output scatter plot file (optional, scatter mode only)"
  echo "  --conversion - Type of conversion (required for convert mode): fpkm_to_tpm or tpm_to_fpkm"
  echo
  exit 1
}

# Check if at least 3 arguments are provided
if [ "$#" -lt 3 ]; then
  usage
fi

# Assign arguments to variables
MODE=$1
FILE1=$2
OUT_DIR=$3
FILE2=""
PTITLE="Gene Expression Comparison"
OTITLE="TPM_Scatter_Plot.png"
CONVERSION=""

# Parse additional options
shift 3
while [ "$#" -gt 0 ]; do
  case "$1" in
    --p_title)
      PTITLE=$2
      shift 2
      ;;
    --o_title)
      OTITLE=$2
      shift 2
      ;;
    --conversion)
      CONVERSION=$2
      shift 2
      ;;
    *)
      if [ -z "$FILE2" ]; then
        FILE2=$1
      else
        echo "Unknown option: $1"
        usage
      fi
      shift 1
      ;;
  esac
done

# Determine the path to quantgene.py relative to this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
QUANTGENE_PY="$SCRIPT_DIR/../quantgene/quantgene.py"

# Execute the Python script based on the mode
if [ "$MODE" = "scatter" ]; then
  if [ -z "$FILE2" ]; then
    echo "Error: file2 is required for scatter mode"
    usage
  fi
  echo "Running scatter plot mode..."
  python3 "$QUANTGENE_PY" scatter "$FILE1" "$FILE2" "$OUT_DIR" --p_title "$PTITLE" --o_title "$OTITLE"
elif [ "$MODE" = "convert" ]; then
  if [ -z "$CONVERSION" ]; then
    echo "Error: --conversion option is required for convert mode"
    usage
  fi
  echo "Running convert mode..."
  python3 "$QUANTGENE_PY" convert "$FILE1" "$OUT_DIR" --conversion "$CONVERSION"
else
  echo "Unknown mode: $MODE"
  usage
fi
