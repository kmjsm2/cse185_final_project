#!/bin/bash

# This script contains command line tests for quantgene

die()
{
    BASE=$(basename "$0")
    echo "$BASE error: $1" >&2
    exit 1
}

runcmd_pass()
{
    echo "[runcmd_pass]: $1"
    sh -c "$1" || die "Error running: $1"
}

runcmd_fail()
{
    echo "[runcmd_fail]: $1"
    sh -c "$1" && die "Command should have failed: $1"
}

if [ $# -lt 3 ]; then
    echo "usage: cmdline_tests.sh {mode} {test_file1} {output_dir} [test_file2]"
    echo "Expected at least 3 arguments but received $#"
    exit 1
fi

MODE=$1
TEST_FILE1=$2
OUTPUT_DIR=$3

if [ "$MODE" = "scatter" ]; then
    if [ $# -ne 4 ]; then
        echo "usage: cmdline_tests.sh scatter {test_file1} {output_dir} {test_file2}"
        echo "Expected 4 arguments for scatter mode but received $#"
        exit 1
    fi
    TEST_FILE2=$4
elif [ "$MODE" != "convert" ]; then
    echo "Unknown mode: $MODE"
    echo "Supported modes: scatter, convert"
    exit 1
fi

TMPDIR=$(mktemp -d -t tmp-XXXXXXXXXX)

echo "Saving tmp files in ${TMPDIR}"

# Define the path to quantgene.py
QUANTGENE_PATH="/Users/zoekim/Documents/GitHub/cse185_final_project/quantgene/quantgene.py"

# Successful tests
if [ "$MODE" = "scatter" ]; then
    runcmd_pass "python3 $QUANTGENE_PATH scatter $TEST_FILE1 $TEST_FILE2 $OUTPUT_DIR --p_title 'Test Scatter Plot' --o_title 'test_scatter_plot.png'"
else
    runcmd_pass "python3 $QUANTGENE_PATH convert $TEST_FILE1 $OUTPUT_DIR"
fi

# Failing tests
if [ "$MODE" = "scatter" ]; then
    runcmd_fail "python3 $QUANTGENE_PATH scatter nonexistent_file1.genes.results $TEST_FILE2 $OUTPUT_DIR --p_title 'Test Scatter Plot' --o_title 'test_scatter_plot.png'"
    runcmd_fail "python3 $QUANTGENE_PATH scatter $TEST_FILE1 nonexistent_file2.genes.results $OUTPUT_DIR --p_title 'Test Scatter Plot' --o_title 'test_scatter_plot.png'"
else
    runcmd_fail "python3 $QUANTGENE_PATH convert nonexistent_file1.genes.results $OUTPUT_DIR"
fi

echo "All tests completed. Temporary files are saved in ${TMPDIR}"
