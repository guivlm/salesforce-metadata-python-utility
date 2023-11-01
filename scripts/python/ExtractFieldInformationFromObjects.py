import os
import csv
from xml.dom import minidom
import argparse

# Parse command line arguments for input and output directories
parser = argparse.ArgumentParser(description='Process XML files.')
parser.add_argument('--input_dir', type=str, help='Input directory containing the XML files')
parser.add_argument('--output_dir', type=str, help='Output directory to save the CSV file')
args = parser.parse_args()

# Directory containing the XML files
root_directory = args.input_dir

# CSV file to write to
csv_file = os.path.join(args.output_dir, 'fields_information_extract_results.csv')

# A set to store all unique tags
all_tags = set()

# Iterate over all directories in the root directory
for dir_name in os.listdir(root_directory):
    # Construct the full directory path
    directory = os.path.join(root_directory, dir_name, 'fields')

    # Check if the directory exists
    if os.path.isdir(directory):
        # Get a list of all the XML files in the directory
        xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]
        print(f'Found {len(xml_files)} XML files in {directory}.')

        # Iterate over the XML files and extract all unique tags
        for filename in xml_files:
            print(f'Processing file: {filename}')
            # Parse the XML file
            xmldoc = minidom.parse(os.path.join(directory, filename))

            # Extract all unique tags
            for element in xmldoc.documentElement.childNodes:
                if element.nodeType == element.ELEMENT_NODE:
                    all_tags.add(element.tagName)

# Convert the set of tags to a list and sort it
all_tags = sorted(list(all_tags))

# Open the CSV file and write the headers
with open(csv_file, 'w', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file, delimiter=';')
    writer.writerow(['dir_name', 'file_name'] + all_tags)

    # Iterate over all directories in the root directory again to write the data
    for dir_name in os.listdir(root_directory):
        # Construct the full directory path
        directory = os.path.join(root_directory, dir_name, 'fields')

        # Check if the directory exists
        if os.path.isdir(directory):
            # Get a list of all the XML files in the directory
            xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]

            # Iterate over the XML files and extract the data
            for filename in xml_files:
                print(f'Processing file: {filename}')
                # Parse the XML file
                xmldoc = minidom.parse(os.path.join(directory, filename))

                # Extract data from specific tags and write to CSV file
                data = [dir_name, filename.split('.', 1)[0]]
                for tag in all_tags:
                    elements = xmldoc.getElementsByTagName(tag)
                    data.append(elements[0].firstChild.data if elements and elements[0].firstChild else '')
                writer.writerow(data)

print('Finished writing CSV file.')
