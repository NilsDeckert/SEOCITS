// This file was entirely written by Gemini

// Helper: Calculate Success Rate from an array of runs
#let calc-success-rate(runs) = {
  let total = runs.len()
  if total == 0 { return 0 }
  let successes = runs.filter(r => r.success == true).len()
  // return successes / total * 100
  return str(successes) + "/" + str(total)
}

// Helper: Calculate Median Latency from an array of runs
#let calc-median-latency(runs) = {
  let latencies = runs.map(r => r.latency).filter(l => l != none).sorted()
  let n = latencies.len()
  
  if n == 0 {
    return 0
  } else if calc.rem(n, 2) == 1 {
    // Odd number of elements: take the middle one
    return latencies.at(int(n / 2))
  } else {
    // Even number of elements: average the two middle ones
    let mid-right = int(n / 2)
    let mid-left = mid-right - 1
    let ret = (latencies.at(mid-left) + latencies.at(mid-right)) / 2.0
    // return ret
    return calc.round(ret, digits: 2)
  }
}

// Helper: Parse a JSONL string into an array of dictionaries
#let parse-jsonl(content) = {
  let lines = content.split("\n").filter(l => l.trim() != "")
  return lines.map(line => json(bytes(line)))
}

// Core function: processes an array of JSONL strings and generates the table
#let summarize-jsonl-data(jsonl-strings) = {
  let raw-data = ()

  // 1. Parse the JSONL strings
  for content in jsonl-strings {
    raw-data += parse-jsonl(content)
  }

  // 2. Group runs by task
  let tasks = (:)
  for entry in raw-data {
    let t = entry.task
    let current-runs = tasks.at(t, default: ())
    tasks.insert(t, current-runs + entry.runs)
  }

  // 3. Calculate metrics and build table rows
  let table-rows = ()
  for (task, runs) in tasks.pairs() {
    let success-rate = calc-success-rate(runs)
    let median-lat = calc-median-latency(runs)

    // Format the text for the table cells
    table-rows.push(task)
    table-rows.push(str(calc.round(success-rate, digits: 1)) + "%")
    table-rows.push(str(calc.round(median-lat, digits: 3)) + "s")
  }

  // 4. Render the Table (Styled like a clean, academic booktabs table)
  table(
    columns: (1fr, auto, auto),
    align: (left, center, right),
    stroke: none,
    fill: none,
    
    // Table Header
    table.hline(y: 0, stroke: 1.5pt),
    [*Task*], [*Success Rate*], [*Median Latency*],
    table.hline(y: 1, stroke: 0.75pt),
    
    // Table Body
    ..table-rows,
    
    // Table Footer line
    table.hline(y: tasks.len() + 1, stroke: 1.5pt)
  )
}

// Wrapper function: Give it an array of file paths to read them directly
#let summarize-jsonl-files(file-paths) = {
  let contents = file-paths.map(path => read(path))
  summarize-jsonl-data(contents)
}

// New Helper: Get raw metrics (success rate & median latency) for a single file as a dictionary
#let get-file-metrics(file-path) = {
  let content = read(file-path)
  let raw-data = parse-jsonl(content)
  let tasks = (:)
  
  for entry in raw-data {
    let t = entry.task
    let current-runs = tasks.at(t, default: ())
    tasks.insert(t, current-runs + entry.runs)
  }
  
  let results = (:)
  for (task, runs) in tasks.pairs() {

    results.insert("success-rate", calc-success-rate(runs))
    results.insert("median-latency", calc-median-latency(runs))
  }
  return results
}
