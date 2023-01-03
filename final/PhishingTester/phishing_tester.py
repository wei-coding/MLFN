import argparse
import ml_model
import numpy as np
import json
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--url", "-u", type=str)
    group.add_argument("--file", "-f", type=str)
    args = parser.parse_args()
    if args.url:
        print(ml_model.get_phishing_percentage(args.url))
    if args.file:
        report = []
        with open(args.file) as f:
            with logging_redirect_tqdm():
                for site in tqdm(f.readlines()):
                    if site.strip():
                        report.append(ml_model.get_phishing_percentage(site.strip()))
        with open(args.file + ".report", "w") as f:
            json.dump(report, f)
        report_arr = np.array(report)
        print(np.count_nonzero(report_arr > 0.5))

if __name__ == "__main__":
    main()