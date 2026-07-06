import json
import os
from pathlib import Path

def clean_summary_files(root_dir="."):
    """Recursively finds summary.jsonl files and removes duplicate runs."""
    # Find all summary.jsonl files recursively
    for file_path in Path(root_dir).rglob('summary.jsonl'):
        process_file(file_path)

def process_file(file_path):
    cleaned_lines = []
    modified = False

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                
                # Filter duplicates in 'runs' by latency
                if "runs" in data:
                    seen_latencies = set()
                    unique_runs = []
                    
                    for run in data["runs"]:
                        latency = run.get("latency")
                        if latency not in seen_latencies:
                            unique_runs.append(run)
                            seen_latencies.add(latency)
                    
                    # If the length changed, we found and removed duplicates
                    if len(unique_runs) < len(data["runs"]):
                        data["runs"] = unique_runs
                        modified = True
                        
                cleaned_lines.append(json.dumps(data) + "\n")
                
            except json.JSONDecodeError:
                print(f"Skipping malformed JSON line in {file_path}")
                cleaned_lines.append(line)

    # Overwrite the file only if duplicates were removed
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        print(f"✅ Cleaned duplicates in: {file_path}")

if __name__ == "__main__":
    # You can change "." to a specific path if needed
    clean_summary_files(".")
