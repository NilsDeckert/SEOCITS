#import "summary_table.typ": *

#let models = (
  "gpt-5-mini",
  "gpt-5.3-chat",
  "DeepSeek-V3.2",
  "Kimi-K2.5",
  "gemini-3.1-flash-lite",
  "gemini-3.5-flash",
  "gemini-3.1-pro-preview"
)

// Create a list of all .jsonl files per task
// Not all benchmarks where done at once

// TURN LEFT
#let date1 = "2026-06-01_20-39-59"
#let paths_tl = models.map(m => "/benchmark/"+m+"/Turn_left_90/"+date1+"/summary.jsonl")
#let srs_tl = paths_tl.map(p => get-file-metrics(p).at("success-rate"))
#let ml_tl = paths_tl.map(p => get-file-metrics(p).at("median-latency"))

// TURN RIGHT
#let paths_tr = models.map(m => "/benchmark/"+m+"/Turn_right_90/"+date1+"/summary.jsonl")
#let srs_tr = paths_tr.map(p => get-file-metrics(p).at("success-rate"))
#let ml_tr = paths_tr.map(p => get-file-metrics(p).at("median-latency"))

// WALK BACK FORTH
#let paths_bf = models.map(m => "/benchmark/"+m+"/Back_forth/"+date1+"/summary.jsonl")
#let srs_bf = paths_bf.map(p => get-file-metrics(p).at("success-rate"))
#let ml_bf = paths_bf.map(p => get-file-metrics(p).at("median-latency"))

// TOUCH RED
#let paths_rd = (
  "/benchmark/gpt-5-mini/Touch_Red_object/2026-06-01_22-01-00/summary.jsonl",
  "/benchmark/gpt-5.3-chat/Touch_Red_object/2026-06-01_22-01-00/summary.jsonl",
  "/benchmark/DeepSeek-V3.2/Touch_Red_object/2026-06-01_22-01-00/summary.jsonl",
  "/benchmark/Kimi-K2.5/Touch_Red_object/2026-06-01_22-01-00/summary.jsonl",
  "/benchmark/gemini-3.1-pro-preview/Touch_Red_object/2026-06-01_22-01-00/summary.jsonl",
  "/benchmark/gemini-3.5-flash/Touch_Red_object/2026-06-01_22-01-00/summary.jsonl",
  "/benchmark/gemini-3.1-flash-lite/Touch_Red_object/2026-06-01_22-01-00/summary.jsonl",
)
#let srs_rd = paths_rd.map(p => get-file-metrics(p).at("success-rate"))
#let ml_rd = paths_rd.map(p => get-file-metrics(p).at("median-latency"))

// CIRCLE GREEN
#let paths_cg = (
  "/benchmark/gpt-5-mini/Circle_green/2026-06-02_21-34-02/summary.jsonl",
  "/benchmark/gpt-5.3-chat/Circle_green/2026-06-02_21-57-05/summary.jsonl",
  "/benchmark/DeepSeek-V3.2/Circle_green/2026-06-05_17-14-34/summary.jsonl",
  "/benchmark/Kimi-K2.5/Circle_green/2026-06-06_15-04-35/summary.jsonl",
)
#let srs_cg = paths_cg.map(p => get-file-metrics(p).at("success-rate"))
#let ml_cg = paths_cg.map(p => get-file-metrics(p).at("median-latency"))
