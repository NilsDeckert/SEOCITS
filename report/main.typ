#import "@preview/charged-ieee:0.1.4": ieee
#import "functions/benchmark_results.typ": *

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

#let red(txt) = { text(txt, fill: color.red, weight: "bold") }
#let citation_needed = red("[CITATION NEEDED]")

= Introduction

Recent advances in large language models have enabled developers to leverage artificial intelligence for numerous tasks, without requiring training of specialized models.
One example is the control of robots using large language models to solve natural language tasks in unknown environments.

#linebreak()
Traditionally, machine learning models that were used to control robots required large amounts of specialized training data #citation_needed.

Vision Language Models (VLMs) combine Large Language Models (LLMs) like Llama2 @touvronLlama2Open2023 or Gemma @teamGemmaOpenModels2024 with #red("vision encoders") like SigLIP @zhaiSigmoidLossLanguage2023 or CLIP #red("???") @radfordLearningTransferableVisual2021.
One such example is PaliGemma @beyerPaliGemmaVersatile3B2024, that can be used to for image classification or answering natural language questions about images @beyerPaliGemmaVersatile3B2024.

An extension of VLMs for the use in robot control are Vision Language Action Models (VLAs) like RT-2 @brohanRT2VisionLanguageActionModels2023, OpenVLA @kimOpenVLAOpenSourceVisionLanguageAction2024 or SmolVLA @shukorSmolVLAVisionLanguageActionModel2025.
VLAs build on-top of VLMs and directly output robot control actions expressed as text tokens @brohanRT2VisionLanguageActionModels2023.
This way, VLAs can leverage the 'internet-scale' training data of LLMs to generate robot controls to fulfill natural language goals @kimOpenVLAOpenSourceVisionLanguageAction2024.

In related work, perfect localization #footnote(cite(<HabitatChallenge2022>, form: "full")) @cartillierSemanticMapNetBuilding2021 or perfect control @henriquesMapNetAllocentricSpatial2018 of the robot are often assumed @raychaudhuriSemanticMappingIndoor2025.
While perfect actuation of the robot is more feasible, none the of these assumption is realistic in real-world scenarios.
Localization via Global Navigation Satellite Systems (e.g. GPS) can not be guaranteed for e.g. indoor environments and even under open sky, consumer devices only have an accuracy of up to 4.9 meters #footnote(cite(<HowYouMeasure2025>, form: "full")).
Depending on ground conditions and incline, perfect actuation also cannot be assumed.

With this work, we investigate the feasibility of using relative coordinates for robot navigation tasks through Large Language Models. To avoid the need for task or robot specific models, we utilize general-purpose LLMs hosted on remote hardware.

= Methods

To assess the viability of relative coordinates for the use in robot navigation, we setup a series of benchmarking tasks. The tasks are ordered in the order of approximate complexity and are executed by multiple Large Language Models to abstract per-models specifics.

== Environment

The test environment is a PyBullet#footnote(link("https://pybullet.org/")) simulation consisting of 3 colored cubes and a controllable robot in an open setting.
For each run, the environment is reset so that the robot is placed in the center of the objects around it.
Each object has the same dimensions and both the robot and the objects are positioned on the same plane. @fig_sim_env shows the arrangement of the simulation environment.

#figure(
  image("./images/SimEnvironment.png"),
  caption: "The simulation environment"
)<fig_sim_env>

== Simplifications

In order to focus on the evaluation of relative coordinates, we assume a number of simplifications.
First, we abstract necessary sensor readings like LiDAR and provide the model with processed data derived from our known state of the simulated environment.

Along with each task, the Large Language Model is given a description of its environment using relative coordinates.
@code_environment shows an example giving a description for one of the objects.

#figure(
  ```
  The following objects are in your vicinity:
   - rgba(0, 1, 0, 1) cube of width 1.0, height 2 and length 1.0.
    Corner 1: 2.12 meters away at -315.01 degrees.
  Corner 2: 2.92 meters away at -329.04 degrees.
  Corner 3: 2.92 meters away at -300.97 degrees.
  Corner 4: 3.54 meters away at -315.0 degrees.
  ```,
  caption: "Information given to the model to describe the location of a green cube to the front-right"
)<code_environment>

To focus on the navigation of the robot, we also keep the environment very minimal and only formulate the tasks in regard to the color of the objects. Thus, we do not test the identification of specific items.

== Tasks<tasks>

// The following variables are the short forms for the benchmarked tasks
#let s_TL = "Turn Left"
#let s_TR = "Turn Right"
#let s_BF = "Walk Back and Forth"
#let s_RD = "Touch Red"
#let s_CG = "Circle Green"
#let s_CA = "Circle All"

In order to test the LLMs reasoning capabilites using relative coordinates, the model is tested on multiple tasks with approximately increasing complexity. @tab_tasks lists the benchmarked tasks.
Tasks 1-3 are meant to ensure that the model is capable of the basic controls necessary to complete more complex tasks.
Task 4 requires 'understanding' of the simplified sensor readings and the deduced environment.
Finally, Task 5 combines the requirements necessary for the prior tasks and demands 'understanding' of the location changes caused by the robots movements.

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
  ),
  caption: "Summary of the benchmarked tasks"
)<tab_tasks>

To assess the success rate of a model for a given task, each task is executed 20 times by each model.
The completion of tasks 1-3 is evaluated programatically while tasks 4-5 are judged manually.

As the inference speed of the employed models is highly relevant for real-world usecases, we also record the time from task input to control output for every task execution.

== Robot API

To solve the tasks described in @tasks, the LLM is given API descriptions of the following commands to control the robot:

- `move_forward(distance_in_meters)`
- `turn_left(angle in degrees)`
- `turn_right(angle in degrees)`

The model is instructed to only return a combination of the given commands.
The LLMs output is then parsed for the described commands. Recognised calls are executed, while misformed calls and comments are ignored.

#linebreak()

#let models_long = (
  "GPT 5 Mini",
  "GPT 5.3 Chat",
  "Deepseek",
  "Kimi K2.5",
  "Gemini 3.5 Flash Lite",
  "Gemini 3.5 Flash",
  "Gemini 3.1 Pro",
)

The following Large Language Models are tested:

#for m in models_long [
  - #m
]

= Results

Each task was executed 20 times.

== Success Rate

@tab_succ_gpt and @tab_succ_gemini show the success rates of each model for each task.
The tasks #s_TL, #s_TR and #s_BF were sucessfully solved by all models on every try. 
The task #s_RD was solved with 100% success rate by all models except Deepseek, which touched the green object instead of the required red one once.

Notably, the last task of circling the green object shows a sudden drop in success rate for all tested models.
The models `GPT 5 Mini` and `Deepseek` showed the best success rate, successfully circling the green object 9 out of 20 times. Though only with a margin of one run compared to `GPT 5.3 Chat`, `Kimi K2` and `Gemini 3.5 Flash`.
The two Gemini models `3.5 Flash Lite` and `3.1 Pro` performed worst, only succeeding 6/20 and 5/20 times respectively.

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
    [#s_RD],[#srs_rd.at(0)],[#srs_rd.at(1)],[#srs_rd.at(2)],[#srs_rd.at(3)],
    [#s_CG],[#srs_cg.at(0)],[#srs_cg.at(1)],[#srs_cg.at(2)],[#srs_cg.at(3)],
  ),
  caption: "Success rate per model per task"
)<tab_succ_gpt>

#red("NOTE:") Gemini Flash made left turns around green object. All (?) other (non-gemini) models made right turns (like in example)

#figure(
  table(
    columns: (auto, auto, auto, auto),
    table.header(
      [*Task*],
      [*Gemini 3.5 Flash Lite*],
      [*Gemini 3.5 Flash*],
      [*Gemini 3.1 Pro*],
    ),
    [#s_TL],[#srs_tl.at(4)],[#srs_tl.at(5)],[#srs_tl.at(6)],
    [#s_TR],[#srs_tr.at(4)],[#srs_tr.at(5)],[#srs_tr.at(6)],
    [#s_BF],[#srs_bf.at(4)],[#srs_bf.at(5)],[#srs_bf.at(6)],
    [#s_RD],[#srs_rd.at(4)],[#srs_rd.at(5)],[#srs_rd.at(6)],
    [#s_CG],[#srs_cg.at(4)],[#srs_cg.at(5)],[#srs_cg.at(6)],
  ),
  caption: "Success rate per model per task"
)<tab_succ_gemini>

== Latency

@tab_lat shows the latency per model for each task.
The recorded latencies for the tasks "#s_TL" and "#s_TR" are very similar.
The latency for the "#s_RD" task is slightly higher and the tasks "#s_BF" and "#s_CG" showed the highest latency.


#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    table.header(
      [*Model*],
      [#s_TL (s)],
      [#s_TR (s)],
      [#s_BF (s)],
      [#s_RD (s)],
      [#s_CG (s)],
    ),
    [*GPT 5 Mini*], [#ml_tl.at(0)], [#ml_tr.at(0)],
    [#ml_bf.at(0)], [#ml_rd.at(0)], [#ml_cg.at(0)],

    [*GPT 5.3 Chat*], [#ml_tl.at(1)], [#ml_tr.at(1)],
    [#ml_bf.at(1)], [#ml_rd.at(1)], [#ml_cg.at(1)],

    [*Deepseek*], [#ml_tl.at(2)], [#ml_tr.at(2)],
    [#ml_bf.at(2)], [#ml_rd.at(2)], [#ml_cg.at(2)],

    [*Kimi K2*], [#ml_tl.at(3)], [#ml_tr.at(3)],
    [#ml_bf.at(3)], [#ml_rd.at(3)], [#ml_cg.at(3)],

    [*Gemini 3.5 Flash Lite*], [#ml_tl.at(4)], [#ml_tr.at(4)],
    [#ml_bf.at(4)], [#ml_rd.at(4)], [#ml_cg.at(4)],

    [*Gemini 3.5 Flash*], [#ml_tl.at(5)], [#ml_tr.at(5)],
    [#ml_bf.at(5)], [#ml_rd.at(5)], [#ml_cg.at(5)],

    [*Gemini 3.1 Pro*], [#ml_tl.at(6)], [#ml_tr.at(6)],
    [#ml_bf.at(6)], [#ml_rd.at(6)], [#ml_cg.at(6)],
  ),
  caption: "Median latency per model per task"
)<tab_lat>

@fig_boxplot_turn_left visualizes the latency per model for the Task #s_TL.
For comparison, @fig_boxplot_circle_green shows the same plot for the #s_CG task.

#figure(
  image("images/boxplot_Turn_left_90.png")
)<fig_boxplot_turn_left>

#figure(
  image("images/boxplot_Circle_green.png")
)<fig_boxplot_circle_green>

= Discussion

== Success Rate

== Latency

@tab_lat shows that the required inference time does not scale with out perceived complexity of the tasks, but rather the required number of commands to complete the task.
For example, the completion of the task "#s_BF" (4 commands in optimal solution) took significantly longer than that of the "#s_RD" task (2 commands in optimal solution).

= Conclusion
