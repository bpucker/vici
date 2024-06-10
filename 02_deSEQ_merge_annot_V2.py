### Katharina Wolff & Melina Nowak ###

import argparse
import pandas as pd

def combine_tables(table1_path, table2_path, shared_column, output_path):
    # Read the tables into pandas DataFrames
    table1 = pd.read_csv((table1_path), delimiter=';')
    table2 = pd.read_csv((table2_path), delimiter=';')

    # Merge the tables based on the shared column (inner merge)
    merged_table = pd.merge(table1, table2, on=shared_column, how='inner')

    # Save the merged table to a new CSV file
    merged_table.to_csv(output_path, index=False)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Combine two tables based on a shared column")

    # Add arguments for table paths, shared column, and output path
    parser.add_argument("--table1", type=str, help="Path to the first table")
    parser.add_argument("--table2", type=str, help="Path to the second table")
    parser.add_argument("--shared", type=str, help="Name of the shared column")
    parser.add_argument("--out", type=str, help="Path to the output file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if all required arguments are provided
    if not (args.table1 and args.table2 and args.shared and args.out):
        parser.print_usage()
        exit(1)

    # Call the combine_tables function with the provided arguments
    combine_tables(args.table1, args.table2, args.shared, args.out)

