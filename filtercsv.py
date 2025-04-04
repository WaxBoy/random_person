def replace_semicolons_with_commas(input_file, output_file):
    """
    Replaces all semicolons with commas in a CSV file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
    """

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        for line in infile:
            outfile.write(line.replace(';', ','))

# Example usage:
input_csv_file = 'expanded_states.csv'  # Replace with your input file name
output_csv_file = 'colleges.csv'
replace_semicolons_with_commas(input_csv_file, output_csv_file)

print(f"Semicolons replaced with commas in {output_csv_file}")