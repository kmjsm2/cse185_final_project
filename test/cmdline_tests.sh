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
    if command -v /usr/bin/time &> /dev/null
    then
        /usr/bin/time -v sh -c "$1" 2>&1 | tee >(grep -E 'Elapsed \(wall clock\) time|Maximum resident set size') || die "Error running: $1"
    else
        /bin/time -v sh -c "$1" 2>&1 | tee >(grep -E 'elapsed|maximum resident set size') || die "Error running: $1"
    fi
}

runcmd_fail()
{
    echo "[runcmd_fail]: $1"
    if command -v /usr/bin/time &> /dev/null
    then
        /usr/bin/time -v sh -c "$1" 2>&1 | tee >(grep -E 'Elapsed \(wall clock\) time|Maximum resident set size') && die "Command should have failed: $1"
    else
        /bin/time -v sh -c "$1" 2>&1 | tee >(grep -E 'elapsed|maximum resident set size') && die "Command should have failed: $1"
    fi
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

# Function to find quantgene.py in common directories
find_quantgene_py() {
    local search_dirs=("$PWD" "$PWD/.." "$PWD/../.." "$PWD/../../..")
    for dir in "${search_dirs[@]}"; do
        if [ -f "$dir/quantgene/quantgene.py" ]; then
            echo "$dir/quantgene/quantgene.py"
            return
        fi
    done
    echo ""
}

# Automatically find the path to quantgene.py
QUANTGENE_PATH=$(find_quantgene_py)

if [ -z "$QUANTGENE_PATH" ]; then
    echo "Could not find quantgene.py. Please set the QUANTGENE_DIR environment variable to the directory containing quantgene.py."
    exit 1
fi

echo "Using quantgene.py found at: $QUANTGENE_PATH"

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
