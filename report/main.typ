#import "@preview/charged-ieee:0.1.4": ieee
#import "functions/benchmark_results.typ": *

#show: ieee.with(
  title: [
From Global Coordinates to Robot-Centered Spatial Representations],
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

Up until recently, machine learning models for robotic control were highly specialized and required massive datasets for domain-specific tasks #red("[X]"). Recent advances in Large Language Models however, have enabled developers to leverage artificial intelligence for broad, open-ended tasks, without requiring training of specialized models.

#linebreak()

In the chain of reasoning about and acting inside unknown, physical environments, Vision Language Models (VLMs) provide the first step of reasoning about the environment through visual clues. VLMs like PaliGemma @beyerPaliGemmaVersatile3B2024 combine Large Language Models (LLMs) like Llama2 @touvronLlama2Open2023 or Gemma @teamGemmaOpenModels2024 with vision encoders like SigLIP @zhaiSigmoidLossLanguage2023 or CLIP @radfordLearningTransferableVisual2021 for tasks like image classification or answering natural language questions about images @beyerPaliGemmaVersatile3B2024. Audio Vision Language Models (AVLMs) @guzhovAudioCLIPExtendingCLIP2021 @lyuMacawLLMMultiModalLanguage2023 extend VLMs with reasoning capabilites about sound cues.

#linebreak()

To bridge the gap from reasoning to acting, Vision Language Action Models (VLAs) like RT-2 @brohanRT2VisionLanguageActionModels2023, OpenVLA @kimOpenVLAOpenSourceVisionLanguageAction2024 or SmolVLA @shukorSmolVLAVisionLanguageActionModel2025 further extend the idea of VLMs.
VLAs build on-top of VLMs and directly output robot control actions expressed as text tokens @brohanRT2VisionLanguageActionModels2023.
This way, VLAs can leverage the 'internet-scale' training data of LLMs to generate robot controls to fulfill natural language goals @kimOpenVLAOpenSourceVisionLanguageAction2024.
Still, VLAs require specific training and finetuning and are thus less accessible to developers than off-the-shelf Large Language Models.

For this reason, we are investigating the use of regular Large Language Models to generate robot control commands without specialized models.

#linebreak()

While related work @IntentionsActionsWorkflow2026 has shown that off-the-shelf LLMs can be used for robot navigation, grounding these models in physical space remains an ongoing challenge.
In similar work, perfect localization #footnote(cite(<HabitatChallenge2022>, form: "full")) @cartillierSemanticMapNetBuilding2021 or perfect control @henriquesMapNetAllocentricSpatial2018 of the robot are often assumed @raychaudhuriSemanticMappingIndoor2025.
While perfect actuation of the robot is more feasible, none of these assumption are realistic in real-world scenarios:
Localization via Global Navigation Satellite Systems (e.g. GPS) can not be guaranteed for e.g. indoor environments and even under open sky, consumer devices only have an accuracy of up to 4.9 meters #footnote(cite(<HowYouMeasure2025>, form: "full")).
Depending on ground conditions and incline, perfect actuation also cannot be assumed.

#linebreak()

With this work, we investigate the feasibility of using relative coordinates for robot navigation tasks through off-the-shelf Large Language Models.
We evaluate the performance of different general-purpose LLMs hosted on remote hardware and provide a comparison between them.

= Experiments

To assess the viability of relative coordinates for the use in robot navigation, we setup a series of benchmarking tasks. The tasks are ordered in the order of approximate complexity and are executed by multiple Large Language Models to abstract per-models specifics.
To ensure suitability of absolute coordinates and to provide a comparison between absolute and relative coordinates, we first execute the _most complex_ task with one of the LLMs to get a baseline.

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

To focus on the navigation of the robot, we also keep the environment very minimal and only formulate the tasks in regard to the color of the objects. Thus, we do not test the identification of specific items. Furthermore, all objects and the robot are located on the same, two dimensional plane, abstracting differences in elevation.

Because of the relatively simple nature of the tasks, the Large Language Models are given their initial task and sensor readings from the start of the robots position. The tasks are to be solved in a one-shot procedure, avoiding reprompting during the simulation.

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


= Methods

To assess the success rate of a model for a given task, each task is executed 20 times by each model.
The completion of tasks 1-3 is evaluated programatically while tasks 4-5 are judged manually.

As the inference speed of the employed models is highly relevant for real-world usecases, we also record the time from task input to control output for every task execution.

#linebreak()

To be able to judge the suitability of relative coordinate in the use of robot navigation, we first collect a baseline using absolute coordinates.
For this, we execute the "#s_CG" with the Gemini 3.1 Pro model 20 times, giving absolute coordinates for the robots and objects position.

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
As a baseline, we first executed the "#s_CG" task using absolute coordinates with the Gemini 3.1 Pro model.
For this task, the model achieved a 100% success rate with a median latency of #ml_baseline seconds.

== Success Rate

@tab_succ shows the success rates of each model for each task.
The tasks "#s_TL", "#s_TR" and "#s_BF" were sucessfully solved by all models on every try. 
The task "#s_RD" was solved with 100% success rate by `GPT 5 Mini`, `GPT 5.3 Chat` and `Kimi K2`.
`DeepSeek` and the Gemini models `3.1 Flash Lite`, `3.1 Pro Preview` and `3.5 Flash` each touched the green instead of the required red object once.

Notably, the last task of circling the green object shows a sudden drop in success rate for all tested models.
The models `GPT 5 Mini` and `DeepSeek` showed the best success rate, successfully circling the green object 9 out of 20 times. Though only with a margin of one run compared to `GPT 5.3 Chat`, `Kimi K2` and `Gemini 3.5 Flash`.
The two Gemini models `3.5 Flash Lite` and `3.1 Pro` performed worst, only succeeding 6/20 and 5/20 times respectively.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    table.header(
      [*Model*],
      [#s_TL],
      [#s_TR],
      [#s_BF],
      [#s_RD],
      [#s_CG],
    ),
    [*GPT 5 Mini*], [#srs_tl.at(0)], [#srs_tr.at(0)], [#srs_bf.at(0)], [#srs_rd.at(0)], [#srs_cg.at(0)],
    [*GPT 5.3 Chat*], [#srs_tl.at(1)], [#srs_tr.at(1)], [#srs_bf.at(1)], [#srs_rd.at(1)], [#srs_cg.at(1)],
    [*Deepseek*], [#srs_tl.at(2)], [#srs_tr.at(2)], [#srs_bf.at(2)], [#srs_rd.at(2)], [#srs_cg.at(2)],
    [*Kimi K2*], [#srs_tl.at(3)], [#srs_tr.at(3)], [#srs_bf.at(3)], [#srs_rd.at(3)], [#srs_cg.at(3)],
    [*Gemini 3.5 Flash Lite*], [#srs_tl.at(4)], [#srs_tr.at(4)], [#srs_bf.at(4)], [#srs_rd.at(4)], [#srs_cg.at(4)],
    [*Gemini 3.5 Flash*], [#srs_tl.at(5)], [#srs_tr.at(5)], [#srs_bf.at(5)], [#srs_rd.at(5)], [#srs_cg.at(5)],
    [*Gemini 3.1 Pro*], [#srs_tl.at(6)], [#srs_tr.at(6)], [#srs_bf.at(6)], [#srs_rd.at(6)], [#srs_cg.at(6)],
  ),
  caption: "Success rate per model per task"
)<tab_succ>

== Latency

@tab_lat shows the median latency per model for each task.
The recorded latencies for the tasks "#s_TL" and "#s_TR" are very similar, with a maximum difference of $0.59s$ ($~15%$) for the DeepSeek model.
The latency for the "#s_RD" task is slightly higher than that of the first two tasks.
The task "#s_BF" shows another increase in latency and "#s_CG" showed the highest median latency across models.


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

The results of the first tasks seem very promising and show that the Large Language Models are capable of basic robot control and understanding of the environment.
Nevertheless, none of the tested models were able to solve the "#s_CG" task reliably and even in the best cases only succeeded 45% of the time.

Looking at the problems that occured during the experiments, the models most commonly (44/91) "turned too far" i.e. away from the target object after moving into its vicinity. In 20 of 44 cases the model would have correctly chosen the turn direction afterwards, but circled in empty space following the initially described mistake. In 9 cases, it did so even after aligning correctly with the objects axis.
In our final experiments, we provided the model with directions in degrees, though we also tested using radian measure, which did not improve the models sense of direction.

In 18/91 cases, the model did not correctly handle the distance information it was provided and moved the target object.

#linebreak()


While the baseline shows that the Large Language Model itself is capable of controlling the robot satisfactorily, the results suggest that the use of relative coordinates is not suitable for navigation by unspecialized Large Language Models.

== Latency

@tab_lat shows that the required inference time does not scale with out perceived complexity of the tasks, but rather the required number of commands to complete the task.
For example, the completion of the task "#s_BF" (4 commands in optimal solution) took significantly longer than that of the "#s_RD" task (2 commands in optimal solution).

Overall, the required inference time scaled relatively fast with an increasing number of output commands. Even though our benchmarking tasks were relatively simple, the task "#s_CG" required a median inference time of $14.31$ seconds.
For more complex tasks that would require more control commands, this would likely increase even further. Even disregarding the success rate, the required latency could restrict acceptance in real life scenarios, depending on the use case.

= Conclusion 
