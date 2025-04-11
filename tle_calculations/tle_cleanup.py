def clean_tle_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith('1 ') or line.startswith('2 '):
                outfile.write(line + '\n')

# Example usage:
clean_tle_file('tle_2013.txt', 'tle_2013_clean.txt')
