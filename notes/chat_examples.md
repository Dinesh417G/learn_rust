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
