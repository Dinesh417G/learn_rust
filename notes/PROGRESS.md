# Rust learning progress

The teacher updates this file. `[x]` = watched + layer done, `[~]` = started.
Chapter numbers = Ardan "Ultimate Rust Bundle" player. Every chapter with title and length:
`notes/CHAPTERS.md`. Plan, rules and calendar: `notes/ROADMAP.md`. Old minidb tracker and
log: `notes/archive/PROGRESS-minidb.md`.

**Target (changed 2026-11-15):** `rcnc/`, a small machine controller in Rust for a laser
metal printer (3 axes, layer loop, drives, HMI), built stage by stage with the videos.
**Now:** S1 · pull step 3 (ROADMAP): order the recoater to 900, nothing stops it, then a guarded `move_to`
**Hook:** state: `rcnc` builds and prints `x travels 600` / `x at 480` (step 2 done; name is "x" since the student's line 8, max was moved to 600) · open closing (Gap, size 1, after "What should I need to do"): line 10 `x.pos = 480.0;` shown, new line 11 `x.pos = ____;` for the order 900 (answer `900.0`; it goes, nothing stops it → wish for a guard, `fn move_to(axis: &mut Axis, target: f64) -> bool`) · pocket (2026-11-15): "The recoater's wall is at 500 mm. In your program, what is stopping it from going to 900?" (answer: nothing yet) · last forms: Your move, Gap
**Deadline:** Ardan access ends **2026-12-28**. Videos first; a boss may finish later.
**Debt:** due 39 by end of 2026-11-16, 65 by 2026-11-22 (table in the `rust-teacher` skill).

| Scoreboard | |
|---|---|
| Chapters | 35 / 301 (12 %) |
| Pace needed | 7 chapters + about 55 min of video a day |
| Layers printed | 0 (build height 0.00 mm; 1 layer = 0.04 mm) |
| Bosses beaten | 0 / 9 |
| Streak | 0 days |

PDF = open it, scroll, mark complete (1 min, no reading). Quiz = do it, it is the level check.

## S1 · The machine in memory · Part 1 (rest) · week 1
- [x] 1.0.1–1.5.2 Modules 1-4 + Structs (done on minidb, 2026-10-16 to 10-25)
- [ ] L1-L2 warm-up, no video: `struct Axis`, `new`, `move_to(&mut self)` with a limit check
- [ ] 1.5.3–1.5.4 Traits + Exercise I → L3: `trait Status` for `Axis` AND `Laser`, one `report()` for both
- [ ] 1.5.5–1.5.6 Collections + Exercise J → L4: `Vec<Axis>` (X, Z, W) + `HashMap` pin table (mini HAL)
- [ ] 1.5.7–1.5.8 Enums + Exercise K → L5: `enum DriveState` (CiA 402) + `enum Command` + `match`
- [ ] 1.5.9–1.5.10, 1.6.1–1.6.2, 0.0.1 Review, quiz, final exam, Start Here
- [ ] **BOSS M1** 5-layer build in the terminal. End state must match the real LinuxCNC sim: Z = -0.200, W = 0.400, X = 0

## S2 · Operator console · Part 2 §1 · week 1
- [ ] 2.0.1, 2.1.1–2.1.4 Intro, setup, IDE (known: skim)
- [ ] 2.1.5 Rust Fundamentals (29 min) → spot 3 things you already built
- [ ] 2.1.6–2.1.7 Console input, Create a library → `rcnc>` prompt; split into `machine` lib + `console` bin
- [ ] 2.1.8–2.1.12 Login, Enums, Structs, Vectors, HashMaps → operator login with roles (Operator / Service / Admin)
- [ ] 2.1.13–2.1.14 Serde, Hashing passwords → `machine.json` (limits, layer height), `users.json` with hashes
- [ ] 2.1.15 Start a CLI App (41 min) → `rcnc home`, `rcnc jog x 10`, `rcnc run --layers 5`
- [ ] 2.1.16–2.1.17 Review + quiz
- [ ] **BOSS M2** log in, home, jog, run a job from `job.json`; restart keeps the settings

## S3 · Shop-floor quality · Part 5 §1-2 + Part 4 · week 2
- [ ] 5.0.1, 5.1.1–5.1.4 Intro, review, quiz
- [ ] 5.2.1–5.2.6 Idiomatic, Docs, Publishing → fmt + clippy clean, `cargo doc`, licence in Cargo.toml
- [ ] 5.2.7–5.2.9 Iterators, Closures → hatch-line generator for one layer
- [ ] 5.2.10–5.2.11 Common traits → Debug / Display / Default / PartialEq / From on `Axis`, `Position`
- [ ] 5.2.12–5.2.14 Errors → `MachineError` (LimitExceeded, NotHomed, DriveFault, OxygenHigh), no `unwrap()`
- [ ] 5.2.15–5.2.18 Tests, Benchmarks → a test per command, bench the layer loop
- [ ] 5.2.19–5.2.20 Logging → event log lines
- [ ] 5.2.21–5.2.25 Threads, Channels, review, quiz → recoater thread reports "home reached"
- [ ] 4.0.1–4.1.10 Tooling → fmt, clippy, doc, audit, outdated, `cargo deny` licence allowlist
- [ ] 4.2.1–4.2.9 Code practices → floats: 5000 × 0.04 mm drift, count in whole µm; `cfg` for Linux-only parts
- [ ] 4.3.1–4.5.2 General practices, outro, final exam
- [ ] **BOSS M3** every fault is a typed error, every command has a test, clippy and deny pass

## S4 · Digital twin · Part 5 §3-6 (Rusty Engine) · week 3 · PC only (needs a window)
- [ ] 5.3.1–5.3.7 Engine, state, sprites, colliders → recoater, plate and powder as sprites
- [ ] 5.3.8–5.3.15 Keyboard, mouse, text, audio, timer → jog keys, position readout, alarm beep, layer timer
- [ ] 5.4.1–5.4.4 Road Race → code along, then reskin: the recoater sweep
- [ ] 5.5.1–5.5.6 Car Shoot → code along, then reskin: the laser spot hits scan targets
- [ ] 5.6.1–5.6.2 Review + final exam
- [ ] **BOSS M4** a window shows the 5-layer build: recoater sweeps, plate drops, laser draws

## S5 · The servo thread · Part 2 §2 · week 3
- [ ] 2.2.1–2.2.8 Threads → a 1 ms cycle thread moves the axes
- [ ] 2.2.9 Atomics → pins as atomics (how HAL pins behave)
- [ ] 2.2.10–2.2.14 Mutex, RwLock, deadlocks, lock-free, parking → shared status; "no locks in the realtime loop"
- [ ] 2.2.15–2.2.17 Channels, workers, thread pool → command queue into the motion thread
- [ ] 2.2.18–2.2.19 Affinity, Priority → what LinuxCNC does to its servo thread
- [ ] 2.2.20–2.2.23 Rayon, review, quiz → hatch all layers in parallel
- [ ] **BOSS M5** 10,000 cycles, jitter histogram printed, console stays live while axes move

## S6 · The machine on the network · Part 2 §3 · week 4
- [ ] 2.3.1–2.3.6 Async, Tokio, futures, blocking, tests → virtual drives as their own process
- [ ] 2.3.7 Handling Errors (42 min) → `thiserror` / `anyhow` on `MachineError`
- [ ] 2.3.8–2.3.9 File I/O, Network I/O → controller ⇄ drives over TCP
- [ ] 2.3.10–2.3.13 Channels, state, select, pinning → `select!` on command / tick / E-stop
- [ ] 2.3.14–2.3.15 Tracing, Databases → SQLite alarm and event log
- [ ] 2.3.16–2.3.17 Axum, Thumbnail server (72 min) → layer-preview server: each layer as a PNG
- [ ] 2.3.18–2.3.19 Review + quiz
- [ ] **BOSS M6** kill the drive process mid-build: controller faults cleanly, the event is in SQLite

## S7 · Bits on the wire · Part 2 §4-6 + Part 3 · week 5
- [ ] 2.4.1–2.4.4 unsafe, memory, Drop → laser off + drives disabled when the controller drops
- [ ] 2.4.5–2.4.8 Rc/Arc, Lifetimes, Traits, Generics → `trait Drive`, `Axis<D: Drive>` (sim ⇄ EtherCAT swap)
- [ ] 2.4.9–2.4.11 Iterators, lists, arenas → fixed buffers, no allocation in the cycle
- [ ] 2.4.12–2.4.13 Packing, From Bytes to Types → CiA 402 controlword 0x6040 / statusword 0x6041 as bytes
- [ ] 2.4.14–2.4.16 Other languages (FFI), review, quiz → one `extern "C"` function, called from C
- [ ] 2.5.1–2.5.11 Build a network service → telemetry collector: O₂ ppm, layer time, positions
- [ ] 2.6.1–2.6.2 Final review + Foundations final exam
- [ ] 3.0.1, 3.1.1–3.1.7 Next Steps → server sends "pause build" back; smaller frames
- [ ] **BOSS M7** drive words decoded bit by bit; telemetry of a whole build arrives at the server

## S8 · The machine as a service · Part 6 · week 6
- [ ] 6.0.1–6.2.17 REST service → `GET /axes`, `POST /job`, proper status codes
- [ ] 6.2.18–6.2.24 Static files, auth, layers → browser HMI page, operator token
- [ ] 6.3.1–6.3.8 Tracing → a span per layer, JSON log, OpenTelemetry
- [ ] 6.4.1 OpenAPI → API docs for the HMI
- [ ] 6.5.1–6.5.5 Configuration → `.env`, config crate, Clap
- [ ] 6.6.1–6.6.12 gRPC → command channel HMI ⇄ controller
- [ ] 6.7.1–6.7.4 WebSockets → live positions to the browser and the twin
- [ ] 6.8.1–6.10.1 Deployment, design, wrap up → Docker image beside the LinuxCNC sim
- [ ] **BOSS M8** start a build from the browser and watch it live

## S9 · Graduation · Part 7 (one webinar each Sunday)
- [ ] 7.4.1 Foundations Highlights (63 min) · Sunday 2026-11-22
- [ ] 7.1.1 Rust into your Company (56 min) · Sunday 2026-11-29
- [ ] 7.2.1 Fearless Concurrency (97 min) · Sunday 2026-12-06
- [ ] 7.3.1 1 Hour Async (74 min) · Sunday 2026-12-13
- [ ] 7.5.1 Debugging & Optimizing (61 min) · Sunday 2026-12-20
- [ ] **BOSS M9** (no video, may finish after 12-28) a Rust HAL component runs inside the real LinuxCNC Docker sim

## Tools (checked 2026-10-15)
Rust 1.96 stable + clippy + rustfmt, sqlx-cli, cargo-deny, cargo-audit, cargo-outdated,
bacon, cargo-watch, protoc 36, Docker, VS Code.

## Log
- 2026-11-15 Roadmap changed: minidb → `rcnc` (machine controller for the LinuxCNC metal-printer project). All 301 Ardan chapters mapped to 9 stages, deadline 2026-12-28. Task 10 step 1a (20 days stalled) dropped; traits come back in S1 L3 with two types. `rcnc/` created (hello world runs). Next: S1 L1.
- 2026-11-15 `rust-teacher` skill built, then rebuilt as a fixed procedure after the student's feedback (hooks must not be visible, one thing per question). Memory graph `notes/GRAPH.md`, cloud compiler setup `tools/cloud-setup.sh`, release track (Rust 1.100.0) added. First answers on `rcnc`: `{}` of 500.0 (miss), assign without `mut` (hit, named the fix), `600` into `f64` (miss). Machine left broken on line 8.
