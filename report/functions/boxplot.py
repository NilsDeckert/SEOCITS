import sys
import json
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

sns.set_theme(style="ticks", palette="pastel")

path = ""

INDEX_MODEL = 0
INDEX_TASK = 1

if sys.argv[1]:
    path = sys.argv[1]
else:
    path = "benchmark/"

def get_latencies_in_file(file: Path) -> list:
    latencies = []
    with open(file) as f:
        data = json.load(f)
        if 'runs' in data:
            for run in data['runs']:
                if 'latency' in run:
                    latencies.append(run['latency'])
    return latencies


files = Path(path).rglob("*.jsonl")
latencies_by_model = {}
latencies_by_task_by_model = {}
for file in files:
    parts = file.parts[1:] if file.parts[0] == "benchmark" else file.parts
    model = parts[INDEX_MODEL]
    task = parts[INDEX_TASK]

    latencies = get_latencies_in_file(file)

    if task not in latencies_by_task_by_model:
        latencies_by_task_by_model[task] = {model: latencies}
    else:
        by_task = latencies_by_task_by_model[task]
        # Make sure we don't have duplicates
        assert model not in by_task
        by_task[model] = latencies

    if model not in latencies_by_model:
        latencies_by_model[model] = latencies
    else:
        latencies_by_model[model] += latencies

tasks = list(latencies_by_task_by_model.keys())
models = list(latencies_by_task_by_model["Back_forth"].keys())

# Validate data
assert(len(latencies_by_model.keys()) == len(models))
for model in models:
    assert(len(latencies_by_model[model]) == 20 * len(tasks))

for task in tasks:
    assert(len(latencies_by_task_by_model[task]) == len(models))

sns.boxplot(data=latencies_by_model)
plt.xticks(rotation=45, ha='right')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.title("Latency per model")
plt.ylabel("Latency (s)")
plt.savefig("images/boxplot.png")
plt.clf()

print("=================")
print(f"Found tasks: {tasks}")
print(f"Found models: {models}")

for task in tasks:
    task_name = " ".join(task.split("_"))

    plt.title(f"Latency per model ({task_name})")
    sns.boxplot(data=latencies_by_task_by_model[task])
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.ylabel("Latency (s)")
    plt.savefig(f"images/boxplot_{task}.png")
    plt.clf()
