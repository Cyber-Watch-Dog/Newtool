import re
import requests
import argparse

def find_api_keys(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            # Regular expression pattern to match potential API keys
            pattern = r'(?:[A-Za-z0-9_-]{20,})(?![A-Za-z0-9_-])'
            api_keys = re.findall(pattern, content)
            return api_keys
        else:
            print("Failed to retrieve content from", url, ". Status code:", response.status_code)
    except Exception as e:
        print("An error occurred while processing", url, ":", e)
    return []

def main():
    parser = argparse.ArgumentParser(description="A tool to hunt down API key leaks in JS files and pages")
    parser.add_argument("-u", "--url", help="Single target URL to search for API keys")
    parser.add_argument("-f", "--file", help="Path to a .txt file containing multiple target URLs")
    parser.add_argument("-o", "--output", help="Path to the output file to store API keys (optional)")

    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    elif args.file:
        with open(args.file, "r") as file:
            urls = file.readlines()
        urls = [url.strip() for url in urls]
    else:
        print("Please specify either a single target URL (-u) or a file containing multiple target URLs (-f).")
        return

    api_keys_found = {}
    for url in urls:
        api_keys = find_api_keys(url)
        if api_keys:
            api_keys_found[url] = api_keys

    if args.output:
        with open(args.output, "w") as output_file:
            for url, keys in api_keys_found.items():
                output_file.write(f"URL: {url}\n")
                output_file.write("Potential API keys:\n")
                for key in keys:
                    output_file.write(f"{key}\n")
                output_file.write("\n")
        print("Output saved to", args.output)
    else:
        for url, keys in api_keys_found.items():
            print("URL:", url)
            print("Potential API keys:")
            for key in keys:
                print(key)
            print()

if __name__ == "__main__":
    main()
