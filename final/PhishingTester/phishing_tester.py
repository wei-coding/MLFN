import url_features as urlfe
import argparse
import ml_model

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--url", "-u", type=str)
    group.add_argument("--file", "-f", type=str)
    args = parser.parse_args()


if __name__ == "__main__":
    main()