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

In order to test the LLMs reasoning capabilites using relative coordinates, the model is tested on multiple tasks with increasing complexity.

#figure(
  table(
    columns: (auto, auto),
    table.header(
      [*Short*],
      [*Description*]
    )
  )
)

== Robot API

To solve the tasks described in @tasks, the LLM is given API descriptions of the following commands:

- `move_forward(distance_in_meters)`
- `turn_left(angle in degrees)`
- `turn_right(angle in degrees)`

The LLMs output is then parsed for the described commands. Recognised calls are executed, while misformed calls and comments are ignored.

= Results

#let path_tl_gpt_chat = "/benchmark/turn_left_90.jsonl"
#let path_tr_gpt_chat = "/benchmark/turn_right_90.jsonl"

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
    [Turn left 90°],[],[],[],[],
    [Turn right 90°],[],[],[],[],
    [Walk back and forth],[],[],[],[],
    [Touch red],[],[],[],[],
    [Touch green],[],[],[],[],
    [Touch blue],[],[],[],[],
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
    [Turn left 90°],[],[],[],
    [Turn right 90°],[],[],[],
    [Walk back and forth],[],[],[],
    [Touch red],[],[],[],
    [Touch green],[],[],[],
    [Touch blue],[],[],[],
  ),
  caption: "Success rate per model per task"
)<tab_succ_gemini>

= Discussion

= Conclusion
