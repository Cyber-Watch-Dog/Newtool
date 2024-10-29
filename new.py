import subprocess
import os
import shutil
import argparse

def run_subfinder(domain):
    subprocess.run(['./subfinder', '-d', domain, '-o', 'subdomain.txt'])
    if not os.path.exists('subdomain.txt') or os.path.getsize('subdomain.txt') == 0:
        print("Error: No subdomains found or subdomain.txt is empty.")
        return False
    return True

def run_paramspider(subdomain):
    subprocess.run(['python3', 'paramspider.py', '-d', subdomain, '-o', 'output/target.txt'])

def move_target_file():
    if os.path.exists('output/target.txt'):
        try:
            shutil.move('output/target.txt', 'target.txt')
            print("target.txt moved successfully to the main directory.")
        except FileNotFoundError:
            print("Error: The target.txt file does not exist in the output directory.")
    else:
        try:
            open('target.txt', 'w').close()  # Create an empty target.txt file
            print("An empty target.txt file has been created in the main directory.")
        except Exception as e:
            print("Error:", e)

def run_gxss():
    subprocess.run('cat target.txt | ./Gxss -o filter.target.txt', shell=True)
    # Check if filter.target.txt is empty
    if os.path.getsize('filter.target.txt') == 0:
        print("Warning: filter.target.txt is empty. No XSS parameters found.")

def run_xss_vibe():
    subprocess.run(['python3', 'main.py', '-f', 'filter.target.txt', '-o', 'result.target.txt'])

def run_final_output():
    subprocess.run('cat result.target.txt', shell=True)
    if os.path.getsize('result.target.txt') == 0:
        print("Warning: result.target.txt is empty. No XSS parameters found.")

def process_subdomains():
    with open('subdomain.txt', 'r') as file:
        subdomains = file.readlines()
    for subdomain in subdomains:
        subdomain = subdomain.strip()
        if subdomain:
            print(f"Running ParamSpider on {subdomain}...")
            run_paramspider(subdomain)
            move_target_file()
            run_gxss()
            run_xss_vibe()
            run_final_output()

def main():
    parser = argparse.ArgumentParser(description='Run security scans.')
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    args = parser.parse_args()

    if run_subfinder(args.domain):
        process_subdomains()

if __name__ == "__main__":
    main()
