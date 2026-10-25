# Rust learning progress

The teacher updates this file. `[x]` = watched + exercise done, `[~]` = started.
Chapter numbers = Ardan "Ultimate Rust Bundle" course player
(full list: `D:\RustroverProjects\Rust_vedio\library\CURRICULUM.md`).

**Now:** Block 1 · watch 1.5.3 Traits (5:05), then minidb task 10 (own `Display` for Entery, so `{}` works)
**Next milestone:** M1 in-memory store (after Block 1)
**DB spec:** unknown. The original 52-line paste was lost on 2026-10-15, so the plan
below is a generic key-value database. When the spec arrives, save it as
`notes/db-spec.md` and re-tailor Blocks/milestones.

## Block 1 · Language basics · Part 1 Crash Course → M1
Exercises: `exercises/crash_course/<name>` (originals: `ardan/ultimate_rust_crash_course/exercise/`)

- [x] 1.1.1–1.1.4 Introduction, Exercises Overview, Installation, Editor/IDE (known, skipped)
- [x] 1.1.5–1.1.6 Module 1 Review + Quiz
- [x] 1.2.1 Cargo (video skipped; covered by practical quiz 2026-10-22: package name = library name)
- [x] 1.2.2–1.2.4 Variables, Scope, Memory Safety (all watched 2026-10-19)
- [x] 1.2.5 Exercise A - Variables → done as minidb task 1 instead (2026-10-20)
- [x] 1.2.6 Functions (2026-10-20)
- [x] 1.2.7 Exercise B - Functions → done as minidb task 2 instead (2026-10-20)
- [x] 1.2.8 Module System (re-watched 2026-10-22)
- [x] 1.2.9 Exercise C - Module System → done as minidb task 3 instead (2026-10-22)
- [x] 1.2.10–1.2.11 Module 2 Review + Quiz (PDF skipped by choice, course quiz done 2026-10-22)
- [x] 1.3.1–1.3.2 Scalar Types, Compound Types (2026-10-22)
- [x] 1.3.3 Exercise D - Simple Types → done as minidb task 4 instead (2026-10-22)
- [x] 1.3.4 Control Flow (watched 2026-10-23)
- [x] 1.3.5 Exercise E - Control Flow → done as minidb task 5 instead (2026-10-23)
- [x] 1.3.6–1.3.7 Strings, String Literals (2026-10-23)
- [x] 1.3.8 Exercise F - Strings → done as minidb task 6 instead (2026-10-23)
- [x] 1.3.9–1.3.10 Module 3 Review + Quiz (PDF skipped by choice, course quiz done 2026-10-25)
- [x] 1.4.1 Ownership (2026-10-25)
- [x] 1.4.2 References & Borrowing (2026-10-25)
- [x] 1.4.3 Exercise G - Ownership & References → done as minidb tasks 7 + 8 instead (2026-10-25)
- [x] 1.4.4–1.4.5 Module 4 Review + Quiz (PDF skipped by choice, course quiz done 2026-10-25)
- [x] 1.5.1 Structs (2026-10-25)
- [x] 1.5.2 Exercise H - Structs → done as minidb task 9 instead (2026-10-25)
- [ ] 1.5.3 Traits
- [ ] 1.5.4 Exercise I - Traits → `i_traits`
- [ ] 1.5.5 Collections
- [ ] 1.5.6 Exercise J - Collections → `j_collections`
- [ ] 1.5.7 Enums
- [ ] 1.5.8 Exercise K - Enums → `k_enums`
- [ ] 1.5.9–1.5.10 Module 5 Review + Quiz
- [ ] 1.6.1–1.6.2 Full Final Review + Final Exam
- [ ] (optional) `z_final_project`
- [ ] **M1** minidb: in-memory `set/get/delete/list` with `enum Value` + `HashMap<String, Value>`

## Block 2 · The course builds a mini database · Part 2 §1 → M2
Code-along projects go in `exercises/foundations/`.

- [ ] 2.1.1–2.1.4 Introduction, Setup & Update Rust, Setup Dev Environment, IDE Configuration
- [ ] 2.1.5 Rust Fundamentals (29 min)
- [ ] 2.1.6 Console Text Input
- [ ] 2.1.7 Create a Library
- [ ] 2.1.8 World's Simplest Login System
- [ ] 2.1.9–2.1.12 Enumerations, Structures, Vectors, HashMaps
- [ ] 2.1.13 Serialization/Deserialization
- [ ] 2.1.14 Hashing Passwords
- [ ] 2.1.15 Start a CLI App (41 min)
- [ ] 2.1.16–2.1.17 Module 1 Review + Quiz
- [ ] **M2** minidb: command prompt + CLI, data saved to `db.json`, reloaded at start

## Block 3 · Clean code · Part 5 §2 (Ultimate Rust 2) → M3
Exercises: `exercises/ur2/<name>` (originals: `ardan/ultimate_rust2/exercise/`)

- [ ] 5.1.1–5.1.2 Introduction, Exercises Overview
- [ ] 5.2.1–5.2.2 Idiomatic Code + Exercise → `idiomatic`
- [ ] 5.2.3–5.2.4 Documentation + Exercise → `docs`
- [ ] 5.2.7–5.2.9 Iterators, Closures + Exercise → `closures_iterators`
- [ ] 5.2.10–5.2.11 Common Traits + Exercise → `traits`
- [ ] 5.2.12–5.2.14 Creating Errors, Handling Errors + Exercise → `errors`
- [ ] 5.2.15–5.2.18 Unit Tests, Integration Tests, Benchmarks + Exercise → `testing`
- [ ] 5.2.19–5.2.20 Logging + Exercise → `logging`
- [ ] **M3** minidb: `DbError` enum, no `unwrap()`, a test for every command

## Block 4 · On-disk format (the real database core) → M4
- [ ] 2.4.4 The Drop Trait & RAII
- [ ] 2.4.12 Packing, Reordering & Mangling
- [ ] 2.4.13 From Bytes to Types
- [ ] 2.5.1 Introduction & Planning Our Project
- [ ] 2.5.2 Shared Data Structures
- [ ] 2.5.9 Let's Use Less Bandwidth
- [ ] 2.3.8 File I/O
- [ ] **M4** minidb: append-only log file; each SET/DEL = one framed record (magic, version, length, payload, CRC32); re-read at start; stop at a bad CRC

## Block 5 · Concurrency → M5
- [ ] 2.2.1–2.2.8 Threads: overview → scoped threads
- [ ] 2.2.9 Sharing Data with Atomics
- [ ] 2.2.10 Sharing Data with Mutexes
- [ ] 2.2.11 Read/Write Locks
- [ ] 2.2.12 Deadlocks, Panics and Poisoning
- [ ] 2.2.15–2.2.17 Channels, Worker Threads, Thread Pool
- [ ] 2.4.5 Reference Counting
- [ ] 2.4.6 Lifetimes
- [ ] 2.4.7–2.4.8 Traits, Generics
- [ ] (short version) 5.2.21–5.2.23 Multithreading, Channels + Exercise → `ur2/threads_channels`
- [ ] **M5** minidb: `Arc<RwLock<Db>>`, `Storage` trait, one writer thread owns the log file

## Block 6 · Network server → M6
- [ ] 2.3.1–2.3.5 Async Overview, Hello Async/Await, Tokio, Tokio Futures, Blocking Tasks
- [ ] 2.3.6 Unit Testing Tokio
- [ ] 2.3.7 Handling Errors (42 min)
- [ ] 2.3.9 Basic Network I/O
- [ ] 2.3.10–2.3.12 Async Channels, Shared State, Selecting Futures
- [ ] 2.3.14 Tokio Tracing
- [ ] 2.5.3–2.5.5 Collection Daemon Mk 1, Collection Server Mk 1, Error Handling in the Collector
- [ ] 3.1.1 Bi-Directional Communication
- [ ] 3.1.2 Sending Commands & Prevent Unbounded Growth
- [ ] 7.1.1 Webinar: Introducing Rust into your Company Ecosystem (see `ardan/ArdanLabs_RustInYourEnterprise/tcp_server`)
- [ ] **M6** minidb: TCP server + CLI client; Ctrl-C saves to disk, then exits

## Block 7 · HTTP API + operations (optional) → M7
- [ ] 2.3.16 Axum
- [ ] 6.1.1, 6.2.1–6.2.16 REST service: minimal server → error handling with IntoResponse
- [ ] 6.2.19–6.2.21 Header auth + middleware
- [ ] 6.3.1–6.3.4 Tracing, Timing Spans
- [ ] 6.5.1–6.5.5 Configuration (.env, config crate, Clap)
- [ ] 6.7.1–6.7.4 WebSockets
- [ ] **M7** minidb: GET/PUT/DELETE `/kv/<key>`, token auth, `--data-dir` / `--port`

## Block 8 · Compare with a real DB + speed → M8
- [ ] 2.3.15 Working with Databases (sqlx + SQLite)
- [ ] 3.1.3–3.1.5 Giving the Collector a Diet, Optimizing File Reading, Adapting Files In Flight
- [ ] 2.4.9–2.4.11 Iterators, Linked Lists, Allocators & Arenas
- [ ] 2.2.20–2.2.21 Rayon
- [ ] 7.5.1 Webinar: Debugging & Optimizing Rust
- [ ] **M8** minidb: benchmark against SQLite; one speed-up proven with numbers

Any time: Part 4 Best Practices (start with 4.1.1 fmt and 4.1.2 clippy).
Skipped for the DB: 5.3–5.5 (game engine), 2.2.13–2.2.14, 2.2.18–2.2.19, 2.3.13, 2.3.17,
2.4.1–2.4.3, 2.4.14, 6.6 (gRPC), 6.8–6.9.

## Tools (installed/checked 2026-10-15)
Rust 1.96 stable + clippy + rustfmt, sqlx-cli, cargo-deny, cargo-audit, cargo-outdated,
bacon, cargo-watch, protoc 36 (for 6.6 gRPC), Docker, VS Code. The courses say
`rustup update`; that is done during lesson 2.1.2 (it updates Rust for all projects).

## Log
- 2026-10-15 Setup: folders, exercise copies, tools, teacher mode, boot launcher.
- 2026-10-16 Skipped 1.1.1–1.1.4 (student already knows it). Next: Module 1 quiz.
- 2026-10-16 Module 1 quiz passed (fixed: cargo run = build + run; both use debug profile, --release for optimized).
- 2026-10-16 Built focus coach + phone push + Pixel Instagram block (rust_learn). Opened 2.1 Cargo 3 s, watched ~2 min of 2.2 Variables; Cargo skip-quiz unanswered. Next: the quiz.
- 2026-10-16 18:56 Break 2h (other application). Cargo skip-quiz asked, unanswered. Next: answer it.
- 2026-10-19 Watched 1.2.2 Variables. Asked where variables show up in minidb; got samples (const, let, mut, shadowing, type annotation). Next: 1.2.3-1.2.4.
- 2026-10-19 Watched 1.2.3 Scope + 1.2.4 Memory Safety. Next: Exercise A.
- 2026-10-19 Student chose minidb over Exercise A. `cargo init` in minidb done (hello world runs). Task 1 given (const DB_NAME/MAX_KEYS, port: u16, mut key_count, tuple unpack, println). Due tomorrow.
- 2026-10-20 Task 1 re-given; not started. Student on another task all day (coach paused until 18:00). Next: task 1.
- 2026-10-20 minidb task 1 done: const DB_NAME/MAX_KEY, port: u16, mut count, tuple unpack (host, p), println. Errors met: CODESYS-style `:`/`:=`, `&STR` case, unquoted text (`minidb`, `127.0.0.1` read as float), E0384 without mut. Next: 1.2.6 Functions.
- 2026-10-20 Watched 1.2.6. minidb task 2 done: show_banner(host: &str, port: u16), can_add(count: usize) -> bool as tail expression; saw E0308 when adding `;`. Learned: const is global (no need to pass), return value must be used by caller. clippy clean. Next: 1.2.8 Module System.
- 2026-10-21 08:03 Morning check-in; 1.2.8 given. Student studies in the evening, coach paused until 18:00. Next: 1.2.8 Module System, then minidb task 3.
- 2026-10-21 22:08 Evening: 1.2.8 opened (coach saw lesson-2-8, lesson 24m today) but student says it did not sink in, tired. 4 pauses 19:12-20:11 (other task). Next: re-watch 1.2.8, then minidb task 3.
- 2026-10-22 Re-watched 1.2.8. minidb task 3 done: src/lib.rs with pub const DB_NAME/MAX_KEY + pub fn can_add/show_banner; main.rs `use minidb::{...}`. Asked if it's `cargo new --lib` (no: same package, Cargo auto-finds src/lib.rs). Run same output, clippy clean. Next: 1.2.10–1.2.11 Module 2 Review + Quiz.
- 2026-10-22 Task 3b: asked about glob/qualified imports and mod vs use. Created src/config.rs (consts), `mod config;` + `pub use config::{MAX_KEY, DB_NAME};` re-export in lib.rs, main.rs unchanged. Met E0425 (needs path/use) and E0603 (private use shortcut); needed the `pub use` fragment. Open: rename Config.rs -> config.rs, cargo fmt. Next: 1.2.10 review PDF + 1.2.11 quiz, then 3-question module quiz (incl. Cargo).
- 2026-10-22 Module 2 done. Course quiz taken (score not given); review PDF skipped (student learns by doing, not reading). Practical quiz 3/3: rename package -> E0432 (lib name = Cargo.toml name, not folder); private `use` -> lib ok, main E0603; no `mod` -> file ignored. Next: 1.3.1-1.3.2.
- 2026-10-22 Watched 1.3.1-1.3.2. minidb task 4 done: u8/f64/bool/char vars, typed tuple `entry: (f64, bool, char)` + destructure + `.0/.1/.2`, array `keys: [&str; 3]`, `keys.len()`, u8 = 300 -> `literal out of range` (0..=255). Errors met: `["A"]` for char (needs 'A'), unpack backwards `let entry = (temp, ..)`, C-style `let keys[]`, missing `:` before type, `key_len(keys)` / `keys_len()` (CODESYS LEN() habit; Rust = `keys.len()`), printed key_len instead of keys.len(). Shadowed key_len by accident (unused warning). Next: 1.3.4 Control Flow.
- 2026-10-23 Watched 1.3.4. minidb task 5 steps 1-2 done: `for x in keys.iter()` prints each key; `for y in 0..keys.len()` with `keys[y]`. Errors met: `{}` with no value (+ unused `x`), `x.len()` = letter count not index (11/8/5), CODESYS `if count=3;` (needs `==` + `{}`), `loop` with no `break` inside -> unreachable, nested loops -> 9 lines, `y,y` instead of `y, keys[y]`; learned slots fill left to right. Break 09:14-10:30. Next: step 3 if-expression.
- 2026-10-23 Evening: step 3 done: `let stauts = if online { "online" } else { "ofline" };` prints `online`. Errors met: ran cargo from `learn_rust\` (no Cargo.toml; use `--manifest-path minidb/Cargo.toml`), `if { online }` (missing condition), `if online { true } else { false }` (= copy of the bool), E0308 bool vs &str branches. Typos `stauts`/`ofline` left. Clippy: needless_range_loop on the step-2 index loop (kept on purpose). Next: step 4 `loop` + `break count`.
- 2026-10-23 Step 4 done: `let filled = loop { slots += 1; if slots == 100 { break slots; } };` prints 100 (predicted 100, right). Errors met: bare `break` -> `filled` is `()` + unused warning; E0425 printing `filled` inside its own loop (not assigned until `};`). Next: step 5 break it.
- 2026-10-23 Step 5 done, task 5 complete. `;` after `}` -> E0317 (if without else = `()`) + orphan `else`; `"online";` inside branch -> E0308 `()` vs `&str` ("consider removing this semicolon"). Learned: last line without `;` = the value. Reverted, builds. Next: 1.3.6–1.3.7 Strings.
- 2026-10-23 Repo pushed to github.com/Dinesh417G/learn_rust (public); minidb's own .git merged in, backup at `D:\RustroverProjects\_backup\minidb.git`.
- 2026-10-23 Watched 1.3.6–1.3.7. minidb task 6 step 1 done: `.to_string()` first, then `let mut key = String::new(); key.push_str("Pressure");` + `if key != "" {..} else { "nothing yet" }`. Predicted the guard right; met `unused_mut` when push_str was commented out (nothing writes it). Needed the `if ___ != ""` fragment. Next: step 2 `\n` help text.
- 2026-10-23 Step 2 done: `let help = "Commands:\n  set\n  get\n  delete";` (a `&str`, fixed text). Errors met: put help into `key` via push_str, spaces before `\n` (trailing) instead of after (indent) 3x, edit not saved (no `Compiling` line = unchanged file). Needed the `·` space diagram. Next: step 3 unicode.
- 2026-10-23 Step 3 done: `let ok = "\u{2714} saved";` prints ✔; `ok.len()` = 9 (bytes: ✔ is 3 in UTF-8), `ok.chars().count()` = 7; found `ok.chars().last().unwrap()` = 'd' on their own. Errors met: `ok.char()` (E0599, it's `chars`), `ok.count()` on a &str (not an iterator), printing `ok.chars()` (E0277, Chars has no Display). Learned: chars() = conveyor, count() = counter, chain them. Next: step 4 multiline literal.
- 2026-10-23 Step 4 skipped by choice: predicted right (code indent becomes part of a multiline literal) and asked to move on; `\` line continuation not practised. Task 6 complete. Next: Module 3 quiz.
- 2026-10-25 1.3.10 Module 3 course quiz done (score not given), review PDF skipped. Next: 3-question practical quiz.
- 2026-10-25 Practical quiz Q1 given (`let total = key_len + port;`, u8 + u16, predict first) but unanswered: edit unsaved, session ended. Old `key_len * 100` lines 11-12 left uncommented. Next: Q1 prediction, then Q2-Q3.
- 2026-10-25 Practical quiz Q1 done (ran before predicting): `key_len + port` -> E0308 + E0277 (no u8 + u16). Fixed first by changing key_len to u16; then with `as`: wrote `port as u8` -> 202 (7878 = 0x1EC6, low byte 0xC6 = 198, silent truncation, like WORD_TO_BYTE), then `key_len as u16 + port` -> 7882. Learned: widen small->big, `as` down chops. Next: Q2 control flow (1..=len off-by-one).
- 2026-10-25 Q2 done: predicted `1..=keys.len()` prints 1 and 2 only (half right); it printed pressure=1, level=2 then panicked at runtime (index out of bounds: len 3, index 3). Learned `..=` includes the end, compiles fine, checked while running. Revert slip: wrote `1..keys.len()` (skipped temperature), then fixed to `0..`. Next: Q3 strings (`ok[0]`).
- 2026-10-25 Q3 done: predicted `ok[0]` won't build (right, no reason given) -> E0277 str cannot be indexed (byte 0 vs char 0 ambiguous). Fix took 3 tries: `ok[0].last()` (index still there), `ok.chars(0)` (E0061, chars takes no arg), then `ok.chars().nth(0).unwrap()` prints ✔. Clippy suggests `.next()` for `.nth(0)`. Module 3 practical quiz closed (predictions ~2/3, often ran before guessing). Next: 1.4.1 Ownership.
- 2026-10-25 Watched 1.4.1 Ownership (coach saw lesson-4-1, 10m). minidb task 7 step 1-2 done: `let stored = key;` -> E0382 borrow of moved value (predicted error right, but said key becomes "empty"; it is gone, any use refused). Thought receiving a move needs `mut` (no: mut only on whoever changes it); `stored.push_str` -> E0596 + unused_mut on key. Final order: `let mut key` -> `key.push_str` -> `let stored = key;` -> read `stored`; prints Pressure. Next: step 3 `.clone()`.
- 2026-10-25 Step 3 done: `let stored = key.clone();` + `key.push_str("!")` -> `key=Pressure! stored=Pressure` (predicted exactly right). Typo `key.clone` -> E0615 method, not a field. Learned: clone = separate copy, two owners. Next: step 4 Copy types (u8).
- 2026-10-25 Step 4 done: `let k2 = key_len;` (u8) -> both print 4. Predicted wrong (thought key_len moves like key): u8 is Copy, String moves (heap pointer, one owner frees it). Next: step 5 passing a String into a fn moves it.
- 2026-10-25 Step 5 done, task 7 complete: `fn save(k: String)` + `save(stored);` -> E0382 (predicted right): passing a String into a fn moves it, dropped at save's `}`. Met "unclosed delimiter" (missing `}`). Compiler note: borrow instead if owning isn't necessary. Error LEFT IN PLACE on purpose: fix it with `&` after 1.4.2. Exercise G replaced by task 7.
- 2026-10-25 Watched 1.4.2 (coach saw lesson-4-2). Task 8 step 1 done unaided: `save(&stored)` + `fn save(k: &String)` -> builds, stored still usable, main still owns/frees it. Ran before predicting (again). Next: step 2 `&str` param accepts literals too.
- 2026-10-25 Step 2 done: `save("level")` with `k: &String` -> E0308 expected &String found &'static str (predicted right). Re-explained string literal (baked into exe, `&str`, like VAR CONSTANT). Changed to `fn save(k: &str)`: both `save(&stored)` and `save("level")` work (&String -> &str auto, not reverse). Next: step 3 `&mut`.
- 2026-10-25 Session ended ~19:30 by power cut. Step 3 (`&mut` fn mark) given, not started. Next: step 3, then step 4 two `&mut` at once (E0499), then 1.4.4-1.4.5 Module 4 quiz.
- 2026-10-25 Step 3 done: `fn mark(k: &mut String) { k.push('*'); }` + `mark(&mut key);` -> `key=Pressure!* stored=Pressure`. Errors met: missing `;` after `mark(&mut key)`, `*k.push('!')` -> E0614 (`*` applies to push's `()` result; methods auto-deref through `&mut`, no `*` needed); read "add *" as the deref operator. Ran before predicting (3rd time today). Next: step 4 E0499.
- 2026-10-25 Step 4 done, task 8 complete. Predicted "error" (right) but thought `a` takes ownership and needs `let mut a` (no: borrow only; `&mut` already allows writing through it). Two live `&mut key` -> E0499 at the second borrow, because `a` is used later. Reordered so `a` finishes before `let b` -> builds, `key=Pressure!*12`. Learned: a borrow ends at its last use, not at `}`. Ran 4b before predicting. Next: 1.4.4–1.4.5 Module 4 quiz.
- 2026-10-25 Module 4 course quiz done (score not given), PDF skipped; student annoyed the PDF was mentioned again. Next: 3-question practical quiz.
- 2026-10-25 Q1 done: first typed `b.push('3')` (builds, predicted A right), then `a.push('3')` after `b.push('2')` -> predicted error, first said line 53 (the late `a` use), changed to the `let b` line before running: E0499 lands on line 51 `let b`, line 53 only "first borrow later used here". Learned: a later use stretches the borrow back over the new one. Teacher misnumbered `let b` as 50. Next: Q2 `&` while `&mut` live (E0502).
- 2026-10-25 Q2 done (no guess, ran first twice, once with the file unchanged): `save(&key);` between `let b` and `b.push('2')` -> E0502 (read while writer live). Fixed alone by moving `save(&key);` up between `a.push('1')` and `let b` -> prints `Pressure!*1`, then `key=Pressure!*12`. Rule: many `&` or one `&mut`, never both. Next: Q3 Copy into fn.
- 2026-10-25 Q3 done: `fn show_len(n: u8)` + `show_len(key_len);` then print key_len -> builds, `length = 4` / `still have 4`. Predicted A before running, reason "it's u8" (Copy; was wrong on this in task 7 step 4, now right). Module 4 practical quiz closed: Q1 right after a changed guess, Q2 no guess, Q3 right. Next: 1.5.1 Structs.
- 2026-10-25 Watched 1.5.1 (coach saw lesson-5-1). minidb task 9 step 1 done: `struct Entery { key: String, value: f64 }` (typo kept, used the same both times), instance + `println!("Entery {}={}", e.key, e.value)` -> `Entery Pressure=2.5`, no warnings. Errors met: CODESYS-style `key="Pressure";,` (needs `key: value,`), missing `;` after the instance `}`, printed `e.value` twice -> dead_code "field `key` is never read". Found `"Pressure".to_string()` (&str -> String) unaided. Next: step 2 print whole struct.
- 2026-10-25 Step 2 done: `println!("{}", e)` -> E0277 no Display (predicted B right, recalled `{:#?}` but wrote `{#?}` without colon); `{:?}` -> E0277 no Debug (ran before guessing); `#[derive(Debug)]` first put on line 1 above `use` -> E0774 (attribute applies to the item right below it); moved above struct -> `Entery { key: "Pressure", value: 2.5 }`. Next: step 3 `impl` + `fn new`.
- 2026-10-25 Step 3 done: `impl Entery { fn new(key: &str, value: f64) -> Self { Self { key: key.to_string(), value } } }`, `Entery::new("din", 2.55)` -> `Entery { key: "din", value: 2.55 }`. Used field-init shorthand `Self{key,value}` from the video. Errors met: param `key: String` + literal call -> E0308; switched to `&str` -> shorthand E0308 (shorthand only when types match); tried `Self{&key,value}` (parse error, & = borrow not own). Asked for the answer: given `key: key.to_string()`. Guess was `Entry{key=level.value=7.0}` (format: `:` not `=`, quotes on String, `,` between fields). Next: step 4 `&self` method.
- 2026-10-25 22:13 Back from a 10m break. Step 4 done (from mobile, teacher pasted their code verbatim): `fn show(&self) { println!(.., self.key, self.value) }` + `e2.show();` then `{:?}` of e2 still works -> `The key isdin and the value is2.55`. Predicted A with the right reason (`&self` only borrows). Typos: `Println!` (case), `selfvalue` (missing `.`); missing space after "is" (same as task 6). Next: step 5 `&mut self`.
- 2026-10-25 22:34 Step 5 done, task 9 complete: wrote `fn set(&mut self, value: f64) { self.value = value; }` unaided, called `e2.set(9.9)`. Predicted before running that a non-mut `e2` fails (E0596, right), added `let mut e2` -> show prints 2.55 then 9.9, Debug shows 9.9. Space after "is" still missing. Next: 1.5.3 Traits.
