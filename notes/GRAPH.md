# Memory graph

What the student knows, how firmly, and which question shapes get answers. The teacher
updates it after every answer (rules: `rust-teacher` skill, §8). Colours: green = firm
(3), amber = used and mostly right (2), red = shaky (1), grey = not met yet (0).

```mermaid
graph LR
  var["let / mut / const"]:::s3 --> own["ownership: move"]:::s2
  var --> num["number types: no silent conversion"]:::s2
  num --> cast["as casts"]:::s2
  num --> fmt["printing floats with {}"]:::s2
  var --> fnn["functions, tail value"]:::s2
  fnn --> flow["if as value, loop, for, ranges"]:::s2
  var --> strs["String vs &str"]:::s1
  own --> clone["clone"]:::s3
  own --> copy["Copy types"]:::s2
  own --> bor["& borrow"]:::s2
  bor --> bmut["&mut: one writer"]:::s2
  var --> st["struct, fields"]:::s3
  st --> impl["impl, new, &self, &mut self"]:::s2
  bmut --> impl
  st --> dbg["derive Debug"]:::s2
  impl --> tr["traits"]:::s1
  st --> vec["Vec"]:::s0
  vec --> map["HashMap"]:::s0
  st --> en["enum + match"]:::s0
  en --> opt["Option / Result"]:::s0
  fnn --> modu["mod, pub, use"]:::s2
  classDef s3 fill:#2e7d32,color:#fff
  classDef s2 fill:#f9a825,color:#000
  classDef s1 fill:#c62828,color:#fff
  classDef s0 fill:#9e9e9e,color:#fff
```

## Nodes
| Node | Strength | Last | Evidence, in order | Bring it back as |
|---|---|---|---|---|
| let / mut / const | 3 | 11-15 | E0384 on 10-20; on 11-15 called the E0594 error before the run and named `mut` on the `let` line | every new axis |
| number types | 2 | 11-16 | 10-25 ran `u8 + u16` before guessing; 11-15 expected `x.max = 600` to work on an `f64` ("a"). CODESYS habit: INT to LREAL is automatic; 11-16 wrote `600.0` unaided from the gap | layer counter (u32) times 0.04 |
| as casts | 2 | 10-25 | `port as u8` gave 202, then widened the right way | µm to mm |
| printing floats | 2 | 11-16 | expected `500.0`, got `500`; 11-16 predicted `480` for `{}` of 480.0 | Z after one layer |
| functions | 2 | 10-20 | tail value, E0308 when `;` added | `in_limits` |
| if / loop / for | 2 | 11-16 | `1..=len` off by one found at runtime; 11-16 wrote the guard in ST shape: `if x.pos=<480.0 then {println!(..) else(println!(..)` (`then`, `=<`, `else(`, first `{` never closed). Idea right: accept / reject message; repaired it in four single steps, all hits (`else{}`, `}`, `<=`, "Remove then") | layer loop |
| String vs &str | 1 | 10-25 | asked again what a string literal is | axis names, fault text |
| ownership: move | 2 | 10-25 | thought a moved value is "empty", then predicted E0382 correctly | who owns the drive |
| clone | 3 | 10-25 | predicted the output exactly | copy of a position |
| Copy | 2 | 10-25 | missed on u8, got it in the quiz | passing `pos` |
| & borrow | 2 | 10-25 | `save(&stored)` unaided | `report(&axis)` |
| &mut | 2 | 10-25 | E0499 right after changing the guess; E0502 without a guess | `move_to(&mut axis)` |
| struct | 3 | 11-16 | wrote one on 10-25; read a struct literal on 11-15; 11-16 called E0609 before the run: "We are not having pos variable" | Axis, Laser |
| impl / methods | 2 | 10-25 | wrote `set(&mut self)` unaided | `move_to` |
| derive Debug | 2 | 10-25 | E0774 when put above `use` | print an Axis |
| traits | 1 | 10-26 | idea only (4-20 mA rule); no code; a one-type trait step stalled for 20 days | two types, one `report` |
| mod / pub / use | 2 | 10-22 | E0603 on a private `use` | S2 lib + bin split |
| Vec, HashMap, enum, Option | 0 | | not met | S1 pull sequence |

## How this student thinks
- Types first in the CODESYS way: `NAME : TYPE := value`, implicit numeric conversion, `LEN(x)`.
- Runs before guessing about half the time. A guess asked as one short thing gets given.
- Offers their own fix or variation when the step is concrete. That is the moment to follow.
- Words do not land for layout or abstract ideas; a run or a picture does.
- Analogies that worked: one coil one writer; read-only HMI tag; the 4-20 mA rule; CASE state machine. CODESYS INTERFACE did not.

## Closing forms tried
| Date | Form | Outcome | Note |
|---|---|---|---|
| 11-15 | Predict, three lettered options (`{}` of 500.0) | answered | miss |
| 11-15 | Predict, three lettered options (assign without `mut`) | answered | hit |
| 11-15 | Two-part ask ("which word, which line") | answered with their own idea | gave the fix plus a second variant |
| 11-15 | Teacher ran a variant the student did not mean (`let x = 600`) | turned aside | "not like that": run their idea as typed |
| 11-15 | Predict, two lettered options (`600` into `f64`) | answered | miss |
| 11-15 | Fork with three lettered options incl. "both", right after a miss, on a thing not seen yet (`as f64`) | turned aside | left the step, wrote feedback instead. Said: "some parts of the question turn me aside", "I still know I am hooked" |
| 11-16 | Gap (`x.max = ____;`), repair after a miss | answered | float right (`600.0`); typed `X.max` (phone capital) → E0425, names are case-sensitive |
| 11-16 | Why, size 0 ("Which letter does line 8 need?") | answered | hit: `x`; machine runs, prints `X travels 600` |
| 11-16 | Bet (`x.pos = 480.0;` builds or not) | answered with their own idea | hit, gave the reason: "We are not having pos variable" |
| 11-16 | Your move ("Write the line that gives it one.") | answered | hit: sent the whole struct with `pos:f64,` |
| 11-16 | Broken ("What does line 8 need between its braces?") | answered | hit on the field (`pos:450.0`, own start value, name changed to "x"); sent the line without `;` → syntax error |
| 11-16 | Why, size 0 ("What is missing at the caret?") | answered | hit: "; needed to be there" |
| 11-16 | Predict (`{} at {}` of name, pos) | answered | hit on the value: "X at 480" (real: `x at 480`; the name is lowercase since their own line 8, phone capital in the answer) |
| 11-16 | Your move, size 3, wrapped in a story ("operator slips a digit ... Send it there.") | turned aside | "What should I need to do": the order was not clear enough as a task. Shrunk to a Gap on the same line |
| 11-16 | Gap (`x.pos = ____;` for 900) | answered | hit: `x.pos=900.0` (float unaided again; sent the whole line, no `;`, taken as the gap in the given frame) |
| 11-16 | Why ("What in the program checked that move?") | answered with their own idea | skipped "nothing" and went to the fix: "Weather we need an if condition" |
| 11-16 | Your move with a frame ("Write the `if` line") | answered with their own idea | miss on syntax, wrote a full if/else with two messages instead of the framed line; compares against 480.0, not `x.max` |
| 11-16 | Broken, size 0 ("What replaces the `(` after `else`?") | answered | hit: `else{}` |
| 11-16 | Gap, size 0 (closing `}` before `else`) | answered | hit: `}` |
| 11-16 | Fork, two lines (`=<` / `<=`) | answered | hit: "2" |
| 11-16 | Broken, size 0 ("Which word on line 12 does Rust not know?") | answered | hit: "Remove then" |
