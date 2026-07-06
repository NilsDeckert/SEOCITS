#import "@preview/definitely-not-isec-slides:1.0.1": *

#let primary_color = rgb("#C50E1F")

#show: definitely-not-isec-theme.with(
  aspect-ratio: "16-9",
  slide-alignment: top,
  progress-bar: true,
  institute: [TU Berlin],
  logo: [],
  config-info(
    title: [From Global Coordinates to \ Robot-Centered Representations],
    subtitle: [Assessing Spatial Reasoning in General-Purpose LLMs],
    authors: ([*Nils Decker*]),
    extra: [Seminar Operating Complex IT Systems],
    footer: [Nils Deckert],
    download-qr: "",
  ),
  config-common(
    handout: false,
  ),
  config-colors(
      primary: primary_color,
  ),
)

#let cite_bottom(lbl: "") = {
  place(
      bottom + right,
      dx: -5pt,
      cite(label(lbl))
    )
}

// -------------------------------[[ CUT HERE ]]--------------------------------
//
// === Available slides ===
//
// #title-slide()
// #standout-slide(title)
// #section-slide(title,subtitle)
// #blank-slide()
// #slide(title)
//
// === Available macros ===
//
// #quote-block(body)
// #color-block(title, body)
// #icon-block(title, icon, body)
//
// === Presenting with pdfpc ===
//
// Use #note("...") to add pdfpc presenter annotations on a specific slide
// Before presenting, export all notes to a pdfpc file:
// $ typst query slides.typ --field value --one "<pdfpc-file>" > slides.pdfpc
// $ pdfpc slides.pdf
//
// -------------------------------[[ CUT HERE ]]--------------------------------
 
#title-slide()

#slide(title: [Motivation])[
  - Models for robot-control require specialized training
  - LLMs promise multi-purpose, strong generalisation
  - How can we leverage LLMs for tasks in the real world?
]

#slide(title: [Vision Language Models (VLMs)])[
  - Image classification
  - Answer questions about images
  - Example: PaliGemma
]

#slide(title: [Vision Language Action Models (VLAs)])[
  - Output robot control tokens
  - Fulfil natural-language tasks
]

#slide(title: [Using off-the-shelf LLMs])[
  - Typical assumptions:
    - Perfect localization
    - Perfect control
]

#slide(title: [Assuming perfect localization])[
  Insert video here using global coordinates and solving task
]

#section-slide(title: [Experiments])

#slide(title: [Experiments])[
  #grid(
    columns: (1fr, 1fr),
    column-gutter: 1em,
    [
      == Environment
      - PyBullet Simulation
      - Open space
      - Three colored cubes

      == Tasks
      1. Turn Left 90°
      2. Turn Right 90°
      3. Walk 3m, Turn around, come back
      4. Touch the red object
      5. Walk around the green object

    ],
    [
      #figure(
        image("../report/images/SimEnvironment.png"))
    ]
  )
]

#slide(title: [Robot API])[
  - `move_forward(distance_in_meters)`
  - `turn_left(angle_in_degrees)`
  - `turn_right(angle_in_degrees)`
  - `finish(reason)`
]

#slide(title: [Tested Models])[
  #align(center)[
    #table(
      columns: (1fr, 1fr, 1fr),
      align: left,
      [*OpenAI*], [*Open Source*], [*Google*],
      [
       - GPT 5 Mini
       - GPT 5.3 Chat
      ],
      [
       - Deepseek V3.2
       - Kimi K2.5
      ],
      [
       - Gemini 3.1 Flash Lite
       - Gemini 3.5 Flash
       - Gemini 3.1 Pro Preview
      ]
    )
  ]
]

#let models = (
  "GPT 5 Mini",
  "GPT 5.3 Chat",
  "Deepseek V3.2",
  "Kimi K2.5",
  "Gemini 3.1 Flash Lite",
  "Gemini 3.5 Flash",
  "Gemini 3.1 Pro Preview"
)

// The following variables are the short forms for the benchmarked tasks
#let s_TL = "Turn Left"
#let s_TR = "Turn Right"
#let s_BF = "Walk Back and Forth"
#let s_RD = "Touch Red"
#let s_CG = "Circle Green"

#section-slide(title: [Results])

#slide(title: [Results])[
  #table(
    columns: 8,
    [*Task*],
      [*#models.at(0)*],
      [*#models.at(1)*],
      [*#models.at(2)*],
      [*#models.at(3)*],
      [*#models.at(4)*],
      [*#models.at(5)*],
      [*#models.at(6)*],
    [#s_TL],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
    [#s_TR],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
    [#s_BF],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
      [20/20],
    [#s_RD],
      [20/20],
      [20/20],
      [19/20],
      [20/20],
      [19/20],
      [19/20],
      [19/20],
  )
]

#slide(title: [Bibliography])[
  #bibliography("bibliography.bib")
]
