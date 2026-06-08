import sys
import json
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

sns.set_theme(style="ticks", palette="pastel")

path = ""

if sys.argv[1]:
    path = sys.argv[1]
else:
    path = "benchmark/"

files = Path(path).rglob("*.jsonl")
latencies_by_group = {}
for file in files:
    parts = file.parts[1:] if file.parts[0] == "benchmark" else file.parts
    group = parts[0]
    latencies = []
    with open(file) as f:
        data = json.load(f)
        if 'runs' in data:
            for run in data['runs']:
                if 'latency' in run:
                    latencies.append(run['latency'])

    if group not in latencies_by_group:
        latencies_by_group[group] = latencies
    else:
        latencies_by_group[group] += latencies

sns.boxplot(data=latencies_by_group)
plt.xticks(rotation=45, ha='right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.title("Latency per model")
plt.ylabel("Latency (s)")
plt.savefig("images/boxplot.png")