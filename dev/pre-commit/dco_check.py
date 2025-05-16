import sys

def main():
    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, 'r') as f:
        lines = f.readlines()

    if not any('Signed-off-by:' in line for line in lines):
        print(
            "Commit message missing DCO signoff (no 'Signed-off-by' line)."
            + " Use the -s parameter in your git commit"
        )
        sys.exit(1)

if __name__ == '__main__':
    main()