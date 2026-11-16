# Roadmap: learn Rust by building `rcnc` (2026-11-15)

## The project
`rcnc` is a small machine controller for a laser powder-bed metal printer, written from
zero in Rust. The real machine is being built on LinuxCNC (private notes in
`D:\project_linuxcnc`, not in this public repo). `rcnc` is the learning twin of that work:
the same axes, the same layer loop, the same drive state machine, but small enough to own
every line.

| Axis | Job | Travel |
|---|---|---|
| X | recoater | 0 to 500 mm |
| Z | build plate | 0 down to -200 mm |
| W | powder supplier | 0 to 85 mm |

One layer = plate down 0.04 mm, supplier up 0.08 mm, recoater out to 480 mm and back, wait
for HOME, scan, save. The real LinuxCNC simulator ends 5 layers at Z = -0.200, W = 0.400,
X = 0. `rcnc` must print the same numbers (boss M1).

What full LinuxCNC is, and why nobody rewrites it: about 135,000 lines of C/C++, 20 years
of G-code edge cases. A metal printer needs very little of it (slow point-to-point axes, a
layer loop, no contouring). That small part is what `rcnc` builds. The last boss (M9) plugs
Rust into the real LinuxCNC as a HAL component, which is the first real product piece.

Reference machine: reAM250 from TU Munich (open-source LPBF research platform, 2024). It
runs Autodesk's Machine Control Framework (C++, BSD-3) plus a PLC for the axes, with a
RAYLASE scan head. It is the closest published design: read its PLC I/O overview and
circuit diagram when S5-S7 need a real example.

## What you already know (no repeat; S1 L1-L2 re-use it on the machine)
| Rust | PLC picture | Where it returns in rcnc |
|---|---|---|
| `let`, `mut`, `const`, shadowing | VAR, VAR CONSTANT | axis limits as `const` |
| functions, tail expression | FC with a return value | `fn in_limits(..) -> bool` |
| `mod`, `pub`, `use`, lib + bin | library + program | `machine` lib, `console` bin |
| u8/u16/f64, tuples, arrays, `as` | BYTE/WORD/LREAL, WORD_TO_BYTE chops | positions in µm, drive words |
| `for`, ranges, `if` as value, `loop`/`break` | FOR, IF, WHILE | the layer loop |
| `String` vs `&str` | STRING vs constant text | axis names, messages |
| ownership, move, `clone`, Copy | one coil, one writer | who owns the drive |
| `&` and `&mut`, one writer or many readers | read-only HMI tag vs the writing task | `move_to(&mut self)` |
| `struct`, `impl`, `new`, `&self`, derive Debug | DUT + FB methods | `struct Axis` |
| traits (idea only) | 4-20 mA: the rule every transmitter keeps | `trait Status`, later `trait Drive` |

## How a session runs (built from the student's own pattern)
The old plan stalled 20 days on one abstract step (a trait on a toy struct, one type only),
re-given about 60 times. So:

1. **Every layer moves the machine.** A step ends with new terminal output, a new number,
   a fault, or something moving in the twin. No step exists only to practise syntax.
2. **A layer is 10 minutes.** One concept, one run, one commit. On a bad day one layer
   keeps the streak; on a good day stack them.
3. **Never the same step three times.** Not started after two sessions: the teacher shrinks
   it to fill-the-blank (teacher types the frame, student fills one line) or swaps the angle.
4. **Guess-only layer.** No time to type ("back in 1 hr"): the teacher shows 5 lines, the
   student guesses the output from the phone in one message. It counts as half a layer.
5. **Open with the machine, not with the task.** The teacher runs `rcnc`, shows the last
   output and one open question about it.
6. **Videos are separate from typing.** Watch on the phone at any time, say "watched 2.1.5".
   Videos have the hard deadline; building does not.
7. **Scoreboard after every layer:** layers printed, build height, chapters, streak, boss.
8. **Guess first** stays: predict, run, compare.

## Calendar (43 days, about 38 h of video left)
| Week | Dates | Stages | Video | Boss |
|---|---|---|---|---|
| 1 | 11-16 to 11-22 | S1 + S2 | 4.0 h + webinar | M1, M2 |
| 2 | 11-23 to 11-29 | S3 | 4.9 h + webinar | M3 |
| 3 | 11-30 to 12-06 | S4 + S5 | 5.4 h + webinar | M4, M5 |
| 4 | 12-07 to 12-13 | S6 | 5.7 h + webinar | M6 |
| 5 | 12-14 to 12-20 | S7 | 5.8 h + webinar | M7 |
| 6 | 12-21 to 12-27 | S8 | 6.2 h | M8 |

Daily: about 55 min of video (phone) + 20 to 40 min of building. There is no spare week.
If a week slips, keep the videos on schedule and let the boss slip: bosses need no
subscription. Weekly check every Sunday: chapters done against the table.

## S1 job queue (teacher's notes; the student writes the code; skill §12)
Each job exists because the machine misbehaved in the job before. The card is shown
openly; the twist in brackets is not. DONE WHEN lines are targets: the exact wording
follows what the student's code prints, the fact it states must hold.
1. ~~`Axis` has `name`, `max`; `600` is not an `f64`~~ done 2026-11-16 (cloud).
2. ~~Add `pos`, send the recoater to 480~~ done 2026-11-16 (cloud).
3. JOB: the recoater must refuse any order past its wall. DONE WHEN: an order to 900
   prints a refusal naming the 500 limit, and X still stands where it was. Path: the move
   goes inside the accepting branch, compare with `x.max`, then
   `fn move_to(axis: &mut Axis, target: f64) -> bool`, then the same as a method.
   (Twist: after their first fix the position print still says 900, because the
   assignment above the check already ran.)
4. JOB: the plate (Z) runs from 0 down to -200; refuse both ends. DONE WHEN: Z refuses
   -250 and +10 and accepts -0.04. (Twist: a guard that only checks `max` lets -250 through.)
5. JOB: bring up all three axes, X, Z, W, one line each. DONE WHEN: three lines with name
   and travel. `Axis::new`. (Twist: copy-paste of the struct literal with one wrong field.)
6. JOB (after 1.5.3-1.5.4): one status report for an axis and the laser. DONE WHEN: one
   `report()` call per thing prints `X at 0.0` and `LASER off`. `trait Status`, two types.
7. JOB (after 1.5.5-1.5.6): home every axis in one loop, then list the pins like
   `halcmd show pin`. DONE WHEN: `x.pos-cmd 0.0`, `z.pos-cmd 0.0`, `w.pos-cmd 0.0`.
   `Vec<Axis>`, `HashMap<String, f64>`.
8. JOB (after 1.5.7-1.5.8): an axis must not move while its drive is off. DONE WHEN: a
   move with the drive off prints a refusal with the drive state. `enum DriveState` +
   `match`; orders as `enum Command`. (Twist: a `match` with one state left out does not build.)
9. BOSS M1: the layer loop, 5 layers. DONE WHEN: Z = -0.200, W = 0.400, X = 0, the same
   as the real LinuxCNC sim. (Twist: ask for 2000 layers; W runs dry at layer 1063.)

Later stages get their pull sequence when they start, so it fits what happened before.

## Planted discoveries (all true; the student runs into them, the teacher never announces them)
- `{}` hides the `.0` of a whole float. (found 2026-11-15)
- Assigning to `pos` ignores every limit. Only code that checks can stop an axis.
- Ask for 2000 layers: W refuses at layer 1063 (85 / 0.08 = 1062.5). The powder supplier
  is empty long before the build plate is (200 / 0.04 = 5000 layers).
- Add 0.04 five thousand times and compare with 200.0. Run it first and show what it
  really prints. It leads to counting in whole µm (S3, 4.2.6 Floating Point Numbers).
- A `match` on `DriveState` with one state left out does not build.
Add more at the start of each stage. Every one must be checked by a real run first.

## Release track (Rust beyond Ardan)
Installed on the PC: 1.96.0. Newest stable: **1.100.0** (2026-11-12),
https://blog.rust-lang.org/2026/11/12/Rust-1.100.0/. The student updates in 2.1.2
"Setup & Update Rust" (S2), which jumps four releases at once.

Items the 1.100.0 announcement lists. Read the post before using any of them; this table
is only where they would fit:
| Item | Fits |
|---|---|
| never type `!` stable | S1, `loop` / `match` arms that never return |
| Cargo reports unused dependencies; min-publish-age resolution | S3, tooling (4.1.3-4.1.7) |
| `DropGuard` | S7, Drop and RAII (2.4.4): laser off on drop |
| core of the Allocator API | S7, allocators and arenas (2.4.11) |

| Date | Release | What the student ran into on `rcnc` |
|---|---|---|
| | | |
