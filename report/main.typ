#import "@preview/charged-ieee:0.1.4": ieee
#import "functions/summary_table.typ": *

#show: ieee.with(
  title: [
From Global Coordinates to Robot-Centered Spatial Representations for Quadruped Robots],
  abstract: [
    The process of scientific writing is often tangled up with the intricacies of typesetting, leading to frustration and wasted time for researchers. In this paper, we introduce Typst, a new typesetting system designed specifically for scientific writing. Typst untangles the typesetting process, allowing researchers to compose papers faster. In a series of experiments we demonstrate that Typst offers several advantages, including faster document creation, simplified syntax, and increased ease-of-use.
  ],
  authors: (
    (
      name: "Nils Deckert",
      location: [Berlin, Germany],
      email: "deckert@campus.tu-berlin.de"
    ),
  ),
  bibliography: bibliography("refs.bib"),
  figure-supplement: [Fig.],
)

= Introduction

= Methods

To assess the viability of relative coordinates for the use in robot navigation, we setup a series of benchmarking tasks.

== Environment

The test environment is a PyBullet#footnote(link("https://pybullet.org/")) simulation consisting of 3 colored cubes and a controllable robot.
For each run, the robot is placed in the center of the objects around it.
Each object has the same dimensions and both the robot and the objects are positioned on the the plane. @fig_sim_env shows the arrangement of the simulation environment.

#figure(
  image("./images/SimEnvironment.png"),
  caption: "The simulation environment"
)<fig_sim_env>

== Tasks<tasks>

// The following variables are the short forms for the benchmarked tasks
#let s_TL = "Turn Left"
#let s_TR = "Turn Right"
#let s_BF = "Walk Back and Forth"
#let s_RD = "Touch Red"
#let s_CG = "Circle Green"
#let s_CA = "Circle All"

In order to test the LLMs reasoning capabilites using relative coordinates, the model is tested on multiple tasks with increasing complexity. @tab_tasks lists the benchmarked tasks.

#figure(
  table(
    columns: (25%, auto),
    table.header(
      [*Short*],
      [*Description*]
    ),
    [#s_TL],[Turn left 90 degrees],
    [#s_TR],[Turn right 90 degrees],
    [#s_BF],[Walk 3 meters forward, then turn around and walk back to you original position. Turn around until you are facing your starting position again.],
    [#s_RD],[Find a red object and touch it.],
    [#s_CG],[Walk around the green object.],
    [#s_CA],[Walk around each of the objects.],
  ),
  caption: "Summary of the benchmarked tasks"
)<tab_tasks>

== Robot API

To solve the tasks described in @tasks, the LLM is given API descriptions of the following commands:

- `move_forward(distance_in_meters)`
- `turn_left(angle in degrees)`
- `turn_right(angle in degrees)`

The LLMs output is then parsed for the described commands. Recognised calls are executed, while misformed calls and comments are ignored.

= Results

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

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    table.header(
      [*Task*],
      [*GPT 5 Mini*],
      [*GPT 5.3 Chat*],
      [*Deepseek*],
      [*Kimi K2*],
    ),
    [#s_TL],[#srs_tl.at(0)],[#srs_tl.at(1)],[#srs_tl.at(2)],[#srs_tl.at(3)],
    [#s_TR],[#srs_tr.at(0)],[#srs_tr.at(1)],[#srs_tr.at(2)],[#srs_tr.at(3)],
    [#s_BF],[#srs_bf.at(0)],[#srs_bf.at(1)],[#srs_bf.at(2)],[#srs_bf.at(3)],
    [#s_RD],[],[],[],[],
    [#s_CG],[],[],[],[],
    [#s_CA],[],[],[],[],
  ),
  caption: "Success rate per model per task"
)<tab_succ_gpt>

#figure(
  table(
    columns: (auto, auto, auto, auto),
    table.header(
      [*Task*],
      [*Gemini 3.1 Pro*],
      [*Gemini 3.5 Flash*],
      [*Gemini 3.5 Flash Lite*]
    ),
    [#s_TL],[],[],[],
    [#s_TR],[],[],[],
    [#s_BF],[],[],[],
    [#s_RD],[],[],[],
    [#s_CG],[],[],[],
    [#s_CA],[],[],[],
  ),
  caption: "Success rate per model per task"
)<tab_succ_gemini>

= Discussion

= Conclusion
