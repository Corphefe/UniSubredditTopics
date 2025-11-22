# UniSubredditTopics
Data Science Project on Data annotation and Manual encoding.

## Data
The data was dwnloaded directly off of the Reddit API's /new posts on the subreddits r/mcgill, and r/concordia. Theraw json is stored in mcgill.json, and concordian.json.

## Tools
extract_to_csv.py is a CLI tool which takes in a Reddit json file and randomly extracts the user id and Title of a sepcificed number of posts and writes the information into an output file in the format "Author\tTitle\t".
Its usage is:

python3 extract_to_csv.py -o annotated_mcgill.tsv mcgill.json 50

This tool was used to create final_labeled_dataset_concordia.tsv, and final_labeled_dataset_mcgill.tsv. In these files we manually labelled each title some encoding, based on a typology that we conceptualized via prior open coding. 

This typology (with 8 categories) is summarized in taxonomy_guide.md
