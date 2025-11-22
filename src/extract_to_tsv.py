import argparse
import json
import random

def get_parser():
    parser = argparse.ArgumentParser(description="Extract specified fields from a JSON file and save them to a TSV file.")
    parser.add_argument("-o", "--out_file", type=str, required=True, help="Output TSV file path.")
    parser.add_argument("input_file", type=str, help="Input JSON file path.")
    parser.add_argument("num_posts_to_output", type=int, help="Number of posts to output.")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    raw_posts = data["data"]["children"]
    n = min(args.num_posts_to_output, len(raw_posts))
    random.shuffle(raw_posts)
    posts = [
        {"Name": post["data"]["author_fullname"], 
         "title": post["data"]["title"]} for post in raw_posts[:n]
    ]

    with open(args.out_file, 'w', encoding='utf-8') as outfile:
        outfile.write("Name\ttitle\tcoding\n")
        for post in posts:
            name = post["Name"]
            title = post["title"]
            outfile.write(f"{name}\t{title}\t\n")

if __name__ == "__main__": 
    main() 