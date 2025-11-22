import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="merge two tsv files and save into a tsv file with blank codings")
    parser.add_argument("-a", "--tsv_a", required=True, help="First TSV file")
    parser.add_argument("-b", "--tsv_b", required=True, help="Second TSV file")
    parser.add_argument("-o", "--out_csv", required=True, help="Output TSV file")
    return parser

def read_tsv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        next(f)  # skip header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                rows.append(parts)  # [name, title, gold_label]
    return rows

def main():
    parser = get_parser()
    args = parser.parse_args()

    rows_a = read_tsv(args.tsv_a)
    rows_b = read_tsv(args.tsv_b)

    all_rows = rows_a + rows_b

    with open(args.out_csv, "w", encoding="utf-8") as f:
        f.write("name,title,category\n")
        for name, title, gold in all_rows:
            f.write(f"{name}\t{title}\t\n")

if __name__ == "__main__":
    main()