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

## S1 layer plan (teacher's notes; the student writes all code)
- L1 `struct Axis { name, pos, min, max }`, recoater 0..500, print it. Known material.
- L2 `impl Axis`: `new`, `move_to(&mut self, target) -> bool` refusing moves past a limit.
  Break it: jog to 600.
- L3 `trait Status { fn status(&self) -> String; }` for `Axis` and for a new `Laser`
  struct, then `fn report(item: &impl Status)`. Two types is the point: one `report` for both.
- L4 `Vec<Axis>` for X, Z, W and a loop; `HashMap<String, f64>` as the pin table
  (`recoater.pos-cmd`), like `halcmd show pin`.
- L5 `enum DriveState { NotReady, ReadyToSwitchOn, SwitchedOn, OperationEnabled, Fault }`
  and `match`; `enum Command { Home, Jog { axis, dist }, RunLayers(u32) }`.
- Boss M1: the layer loop, 5 layers, end state equals the LinuxCNC sim.

Later stages get their layer plan when they start, so it fits what happened before.
