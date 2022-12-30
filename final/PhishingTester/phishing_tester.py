import argparse
import ml_model

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--url", "-u", type=str)
    group.add_argument("--file", "-f", type=str)
    args = parser.parse_args()
    if args.url:
        print(ml_model.get_phishing_percentage(args.url))

if __name__ == "__main__":
    main()