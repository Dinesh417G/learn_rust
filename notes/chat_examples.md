# Examples taught in chat

Every example the teacher shows only in chat lands here in the same turn, with date,
code and the real output, then commit and push. Chat is not in git; a cloud chat is gone
for the next session otherwise (2026-11-18: the vehicle trait example existed only in a
cloud chat and had to be pasted back by the student).

## ~2026-11-17 (cloud) · traits: the vehicle
Pasted back by the student on 2026-11-18.

```rust
trait Controls {
    fn honk(&self);
    fn lights(&self);
}
impl Controls for Car {
    fn honk(&self)   { println!("car: beep"); }
    fn lights(&self) { println!("car: headlights on"); }
}

fn inspect(v: &impl Controls) {   // "any vehicle that keeps Controls"
    v.honk();
    v.lights();
}
inspect(&Car);
inspect(&Truck);
```
Output given in that chat: `car: beep` / `car: headlights on` / `truck: HOOONK` /
`truck: beacon flashing`. `inspect(&5)`: `error[E0277]: the trait bound {integer}: Controls is not satisfied`.
What landed: `fn show(pos: f64)` next to `fn inspect(v: &impl Controls)`: `v` is the
parameter name, `&` lends it read-only, `impl Controls` is the gate.

## 2026-11-18 (PC) · traits: the wiring (`impl` block)
Student: "the trait is the button the implementaion block is the wiring we want to cover
the wiring i needed to understand it fully explain me easily".

```rust
struct Car { name: String }
struct Truck { name: String }

trait Controls {
    fn honk(&self);
}

impl Controls for Car {
    fn honk(&self) {
        println!("{}: beep", self.name);
    }
}

impl Controls for Truck {
    fn honk(&self) {
        println!("{}: HOOONK", self.name);
    }
}

impl Car {
    fn fuel(&self) {
        println!("{}: tank 40 l", self.name);
    }
}

fn inspect(v: &impl Controls) {
    v.honk();
}

fn main() {
    let swift = Car { name: "Swift".to_string() };
    let tata = Truck { name: "Tata".to_string() };
    inspect(&swift);
    inspect(&tata);
    swift.fuel();
}
```
Real run: `Swift: beep` / `Tata: HOOONK` / `Swift: tank 40 l`.

Corners, each a real compiler stop (rustc 2021 edition, this session):
1. Every button wired: Bike with only `honk` -> `E0046 not all trait items implemented, missing: lights` (`exercises/vehicle`).
2. Plug matches the button letter for letter: `fn honkk(&self)` -> `E0407 method honkk is not a member of trait Controls`.
3. `self` = the vehicle whose button was pressed: Swift's wiring prints `Swift`, Tata's prints `Tata`.
4. The bay sees only panel buttons: `impl Car { fn fuel }` (no `for`) is Car's own switch; `swift.fuel()` works, `v.fuel()` inside `inspect` -> `E0599 no method named fuel found for reference &impl Controls`.
Held back for the closing question: `fn honk(&self, loud: bool)` in Truck's wiring -> `E0050 method honk has 2 parameters but the declaration in trait Controls::honk has 1`.
Open question: "Truck wires its horn as `fn honk(&self, loud: bool)`: does it still get into the bay?"

## 2026-11-18 (PC, evening) · the `impl` block, no code
Student, after the Truck question was shown with code: "Wait no code i still don't
understand the concept the impl i don't till now so teach me". Taught in words only:

- **Body (struct)**: a Car leaves the line as a body with a name plate ("Swift"). It holds
  things, it does nothing. Nothing is wired yet.
- **Workshop (impl)**: the impl block is the workshop visit. Every wire laid there becomes
  something this vehicle can do, and only this vehicle: Car's workshop wires Cars.
- Two kinds of job in the workshop: **own switch** (`impl Car`: the fuel gauge, only Car
  has it, no rule asked for it) and **panel job** (`impl Controls for Car`: the rulebook
  says every vehicle needs a horn button; Car's workshop connects it to a beeper, Truck's
  to an air horn; same button, different wire).
- **Bay** (`inspect`): reads only the rulebook, presses the horn, does not care what is
  behind it. No panel job, no entry (E0277, seen with `inspect(&5)`).
- PLC picture: struct + impl together = one function block. Struct = the VAR part
  (data only, like a UDT), impl = the code part. Trait = the 4-20 mA rule; panel job =
  "this transmitter is wired to meet the rule".

Open question: "A Bus arrives with a body and a name plate, but it never went to the
workshop: what can it do?" (real answer to show after: nothing; `bus.honk()` -> E0599,
`inspect(&bus)` -> E0277. Run it before showing.)
