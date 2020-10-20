from modules.AnnotatedFile import AnnotatedFile
from modules.WebAnnoObject import WebAnnoObject
import os
import time
import argparse

def readable_dir(prospective_dir):
    # Create directory if it doesn't exist
    if not os.path.isdir(prospective_dir):
        os.makedirs(prospective_dir)
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))

def parse_arguments():
    # Read command line parameters
    parser = argparse.ArgumentParser(description="Script to convert from XML format to Web Anno 3.2 format.")

    parser.add_argument('-i', '--input_dir',
                        type=readable_dir,
                        help="Folder with the original input files",
                        default='input')
    parser.add_argument('-o', '--output_dir',
                        type=readable_dir,
                        help="Folder to store the output converted files",
                        default='output')
    args = parser.parse_args()
    return args.input_dir, args.output_dir

def main():
    print("Converting your corpus...\n")
    start_time = time.time()
    input_dir, output_dir = parse_arguments()
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir+"/"+input_dir):
        file_path = current_dir+"/"+input_dir+"/"+filename
        file = AnnotatedFile(file_path)
        processed_file = WebAnnoObject(file, 1)
        file_out = current_dir+"/"+output_dir+"/"+filename.replace("xml","tsv")
        with open(file_out, 'w') as f:
            for line in processed_file.converted_file:
                f.write("%s\n" % line)
        print "File processed:",filename
    print("Processing time: %.2f seconds.\n" % (time.time() - start_time))

main()
