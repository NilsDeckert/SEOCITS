import json
from pathlib import Path
from collections import Counter
import argparse

def count_comments(base_dir="."):
    """Recursively finds .jsonl files, parses them, and counts run comments."""
    comment_counter = Counter()
    
    # rglob finds all matching files in the directory and all subdirectories
    for filepath in Path(base_dir).rglob('*.jsonl'):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                
                try:
                    data = json.loads(line)
                    # Iterate through the runs array
                    for run in data.get("runs", []):
                        comment = run.get("comment")
                        # We only count actual string comments, ignoring null/None
                        if isinstance(comment, str):
                            comment_counter[comment] += 1
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON in {filepath} on line {line_number}")

    return comment_counter

if __name__ == "__main__":
    # Set up argument parsing to allow running with a specific directory
    parser = argparse.ArgumentParser(description="Count comments in JSONL files.")
    parser.add_argument("directory", nargs="?", default=".", help="Target directory (defaults to current directory)")
    args = parser.parse_args()

    print(f"Scanning directory: {args.directory}\n")
    counts = count_comments(args.directory)
    
    # Display the results
    if not counts:
        print("No comments found.")
    else:
        print(f"{'Count':<10} | {'Comment'}")
        print("-" * 50)
        # .most_common() returns a list sorted by count in descending order
        for comment, count in counts.most_common():
            print(f"{count:<10} | {comment}")
