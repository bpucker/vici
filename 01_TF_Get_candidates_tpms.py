### Katharina Wolff & Melina Sophie Nowak ###

import csv
import sys

def retrieve_sequences(input_table, output_table, ids_file):
    # Read the list of IDs from a file
    with open(ids_file, "r") as ids_file:
        ids_to_search = [line.strip() for line in ids_file]

    # Write the retrieved sequences to the output table
    with open(output_table, "w", newline='') as output_file:
        with open(input_table, "r", newline='') as input_file:
            csv_reader = csv.reader(input_file, delimiter=';')
            csv_writer = csv.writer(output_file, delimiter='\t')
            header = next(csv_reader)  # Read the header row

            # Write the header to the output file
            csv_writer.writerow(header)

            # Iterate through each row in the input table
            for row_number, row in enumerate(csv_reader, 2):  # Start from 2nd row (after header)
                # Debugging output to print the row being processed
                #print("Processing row", row_number, ":", row)
                sys.stdout.flush()  # Flush the output buffer

                # Check if any cell in the row contains the gene ID substring
                for id_value in ids_to_search:
                    if any(id_value in cell_value for cell_value in row):
                        csv_writer.writerow(row)
                        print("Match found in row", row_number, "for gene ID:", id_value)
                        sys.stdout.flush()  # Flush the output buffer
                        break  # Exit the loop once a match is found
                else:
                    #print("No match found in row", row_number, "for any gene ID")
                    sys.stdout.flush()  # Flush the output buffer

    print("Sequences containing the substring IDs saved to ", output_table)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Retrieve sequences from a table containing certain IDs")
    parser.add_argument("--input", required=True, help="Input table containing sequences")
    parser.add_argument("--output", required=True, help="Output table to save retrieved sequences")
    parser.add_argument("--ids-file", required=True, help="File containing IDs to search for")

    args = parser.parse_args()
    retrieve_sequences(args.input, args.output, args.ids_file)
