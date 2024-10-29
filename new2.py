import subprocess
import os
import shutil
import argparse

def run_paramspider(domain):
    subprocess.run(['python3', 'paramspider.py', '-d', domain, '-o', f'output/{domain}_target.txt'])

def move_target_file(domain):
    output_file = f'output/{domain}_target.txt'
    target_file = f'{domain}_target.txt'
    
    if os.path.exists(output_file):
        try:
            shutil.move(output_file, target_file)
            print(f"{target_file} moved successfully to the main directory.")
        except FileNotFoundError:
            print(f"Error: The {output_file} file does not exist in the output directory.")
    else:
        try:
            open(target_file, 'w').close()  # Create an empty target.txt file
            print(f"An empty {target_file} file has been created in the main directory.")
        except Exception as e:
            print("Error:", e)

def run_gxss(domain):
    target_file = f'{domain}_target.txt'
    filter_file = f'filter_{domain}.txt'
    
    subprocess.run(f'cat {target_file} | ./Gxss -o {filter_file}', shell=True)
    
    # Check if filter.target.txt is empty
    if os.path.getsize(filter_file) == 0:
        print(f"Warning: {filter_file} is empty. No XSS parameters found.")

def run_xss_vibe(domain):
    filter_file = f'filter_{domain}.txt'
    result_file = f'result_{domain}.txt'
    
    subprocess.run(['python3', 'main.py', '-f', filter_file, '-o', result_file])

def run_final_output(domain):
    result_file = f'result_{domain}.txt'
    
    subprocess.run(f'cat {result_file}', shell=True)
    
    if os.path.getsize(result_file) == 0:
        print(f"Warning: {result_file} is empty. No XSS parameters found.")

def main():
    parser = argparse.ArgumentParser(description='Run security scans on multiple domains.')
    parser.add_argument('-f', '--file', required=True, help='File containing list of domains (one per line)')
    args = parser.parse_args()

    # Read the domains from the file
    if os.path.exists(args.file):
        with open(args.file, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
        
        for domain in domains:
            print(f"\nRunning scan for domain: {domain}")
            run_paramspider(domain)
            move_target_file(domain)
            run_gxss(domain)
            run_xss_vibe(domain)
            run_final_output(domain)
    else:
        print(f"Error: File {args.file} does not exist.")

if __name__ == "__main__":
    main()
