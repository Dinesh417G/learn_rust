// The vehicle example from the cloud chat (notes/chat_examples.md), as a real project.
struct Car;
struct Truck;
struct Bike;

trait Controls {
    fn honk(&self);
    fn lights(&self);
}

impl Controls for Car {
    fn honk(&self)   { println!("car: beep"); }
    fn lights(&self) { println!("car: headlights on"); }
}

impl Controls for Truck {
    fn honk(&self)   { println!("truck: HOOONK"); }
    fn lights(&self) { println!("truck: beacon flashing"); }
}

impl Controls for Bike {
    fn honk(&self)   { println!("bike: ring ring"); }
}

fn inspect(v: &impl Controls) {   // the bay: any vehicle that keeps Controls
    v.honk();
    v.lights();
}

fn main() {
    inspect(&Car);
    inspect(&Truck);
    inspect(&Bike);
}
