# Q&A prep

- **Is κ 0.71 good enough?** Substantial by Landis & Koch; stall states lower (0.58–0.61), which is why we report per-state numbers.
- **Does it generalize?** CS1 → CS2 drops macro-F1 0.75 → 0.66; stall detection is the course-sensitive part (paper §7).
- **Privacy?** Opt-in, no code content, event types + timing only; pseudonymized ids.
- **Why not just ask students?** Self-report interrupts the stall we want to see; we compared with end-of-lab surveys in the paper.
- **Real-time?** Features are computable per 30 s window; latency is the window length.
- **Could TAs act on it?** Next step: TA dashboard study (with the VizPI deployments).

## Asked at the talk (Oct 7)

- Whether the AI assistant itself could use the state (e.g. hold back a hint while "productive") — yes, that is the obvious next study.
- How labels were adjudicated for CS1 (majority vote, then discussion for 3-way splits).
- One question on cost of the telemetry pipeline in large courses (it ran on a single small VM for 87 students).
