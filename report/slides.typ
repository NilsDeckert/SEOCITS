#import "@preview/definitely-not-isec-slides:1.0.1": *

// Package to split slides into steps
#import "@preview/touying:0.7.4": *

// Own functions and shared variables
#import "functions/benchmark_results.typ": *
#import "functions/variables.typ": *

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

      #uncover("2-")[
        == Tasks
      ]
        #uncover("3-")[1. Turn Left 90°]
        #uncover("4-")[2. Turn Right 90°]
        #uncover("5-")[3. Walk 3m, Turn around, come back]
        #uncover("6-")[4. Touch the red object]
        #uncover("7-")[5. Walk around the green object]
    ],
    [
      #figure(
        image("images/SimEnvironment.png"))
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

#section-slide(title: [Results])

#slide(title: [Success Rate])[
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

    ..([#s_TL], 
       [#srs_tl.at(0)], 
       [#srs_tl.at(1)], 
       [#srs_tl.at(2)], 
       [#srs_tl.at(3)], 
       [#srs_tl.at(4)], 
       [#srs_tl.at(5)], 
       [#srs_tl.at(6)]
    ).map(cell => uncover("2-", cell)),

  ..([#s_TR], 
     [#srs_tr.at(0)], 
     [#srs_tr.at(1)], 
     [#srs_tr.at(2)], 
     [#srs_tr.at(3)], 
     [#srs_tr.at(4)], 
     [#srs_tr.at(5)], 
     [#srs_tr.at(6)]
  ).map(cell => uncover("3-", cell)),

  ..([#s_BF], 
     [#srs_bf.at(0)], 
     [#srs_bf.at(1)], 
     [#srs_bf.at(2)], 
     [#srs_bf.at(3)], 
     [#srs_bf.at(4)], 
     [#srs_bf.at(5)], 
     [#srs_bf.at(6)]
  ).map(cell => uncover("4-", cell)),

  ..([#s_RD], 
     [#srs_rd.at(0)], 
     [#srs_rd.at(1)], 
     [#srs_rd.at(2)], 
     [#srs_rd.at(3)], 
     [#srs_rd.at(4)], 
     [#srs_rd.at(5)], 
     [#srs_rd.at(6)]
  ).map(cell => uncover("5-", cell)),

  ..([#s_CG], 
     [#srs_cg.at(0)], 
     [#srs_cg.at(1)], 
     [#srs_cg.at(2)], 
     [#srs_cg.at(3)], 
     [#srs_cg.at(4)], 
     [#srs_cg.at(5)], 
     [#srs_cg.at(6)]
  ).map(cell => uncover("6-", cell)),

  )
]

#slide(title: [Latency])[
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

    ..([#s_TL], 
       [#ml_tl.at(0)], 
       [#ml_tl.at(1)], 
       [#ml_tl.at(2)], 
       [#ml_tl.at(3)], 
       [#ml_tl.at(4)], 
       [#ml_tl.at(5)], 
       [#ml_tl.at(6)]
    ).map(cell => uncover("2-", cell)),

    ..([#s_TR], 
       [#ml_tr.at(0)], 
       [#ml_tr.at(1)], 
       [#ml_tr.at(2)], 
       [#ml_tr.at(3)], 
       [#ml_tr.at(4)], 
       [#ml_tr.at(5)], 
       [#ml_tr.at(6)]
    ).map(cell => uncover("3-", cell)),

    ..([#s_BF], 
       [#ml_bf.at(0)], 
       [#ml_bf.at(1)], 
       [#ml_bf.at(2)], 
       [#ml_bf.at(3)], 
       [#ml_bf.at(4)], 
       [#ml_bf.at(5)], 
       [#ml_bf.at(6)]
    ).map(cell => uncover("4-", cell)),

    ..([#s_RD], 
       [#ml_rd.at(0)], 
       [#ml_rd.at(1)], 
       [#ml_rd.at(2)], 
       [#ml_rd.at(3)], 
       [#ml_rd.at(4)], 
       [#ml_rd.at(5)], 
       [#ml_rd.at(6)]
    ).map(cell => uncover("5-", cell)),

    ..([#s_CG], 
       [#ml_cg.at(0)], 
       [#ml_cg.at(1)], 
       [#ml_cg.at(2)], 
       [#ml_cg.at(3)], 
       [#ml_cg.at(4)], 
       [#ml_cg.at(5)], 
       [#ml_cg.at(6)]
    ).map(cell => uncover("6-", cell)),

  )
]

#slide(title: [Bibliography])[
  #bibliography("refs.bib")
]
