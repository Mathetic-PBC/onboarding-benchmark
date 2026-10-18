# TutorTrace

Classifying learner states from telemetry in AI-assisted programming

David Barron · Virginia Tech

Note: 15 min + 5 Q&A. Session "Learning & Tutoring", chair Tomás Reyes.

---

## Outline

1. Why learner states
2. Telemetry
3. Labeling
4. Model
5. Results + limits

---

## Students stall silently

- In CS1 labs with an AI assistant, students who are stuck often *don't* ask
- TAs see a room of busy screens

Note: open with the lab anecdote: 87 students, 3 TAs.

---

## Six learner states (from telemetry, 30 s windows)

productive · exploring · help-seeking · stalled · stalled-after-error · off-task

---

## What a stall looks like

<div class="r-stack">
  <img class="fragment fade-in" data-fragment-index="0" src="img/p07_step1.svg">
  <img class="fragment fade-in" data-fragment-index="1" src="img/p07_step2.svg">
  <img class="fragment fade-in" data-fragment-index="2" src="img/p07_step3.svg">
  <img class="fragment fade-in" data-fragment-index="3" src="img/p07_step4.svg">
</div>

Note: P07, CS1, 22 minutes. Step 2 = first compiler error at 8:12; the stall runs 8:12–16:50.


---

## Labeling

- 2,340 windows, 3 raters, guide v3
- Fleiss κ = 0.71

![](img/kappa_by_state.svg)

---

## How states follow each other

![](img/transitions.svg)

---

## Model

- Gradient boosting on window features
- Grouped 5-fold by student

---

## Results

Note: say the numbers slowly; point at the stall bars.

- Macro-F1 0.75 within CS1
- 0.66 on an unseen course (CS2)
- Stall states transfer worst

---

## Limits

- One institution, two courses
- CS2 labels from one rater
- Telemetry is sensitive: opt-in, no keystroke content stored

---

## Thanks

Paper + dataset: tutortrace.github.io (camera-ready)

---

## Backup: privacy

- Opt-in consent per lab
- No source code or keystroke content stored, only event types + timing
- Student ids pseudonymized before analysis

---

## Backup: κ per state

off-task 0.84 · help-seeking 0.79 · productive 0.74 · exploring 0.66 · stalled 0.61 · stalled-after-error 0.58
