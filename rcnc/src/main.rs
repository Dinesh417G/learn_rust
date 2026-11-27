struct Axis {
name: String,
max:f64,
pos:f64,
}

trait Status {
    fn report(&self);
}

impl Status for Axis {
    fn report(&self) {

    }
}

fn main() {
    let mut x= Axis {name:"x".to_string(),max:500.0,pos:450.0};
x.max =500.0;
    x.pos = 480.0;
    println!("{} travels {}", x.name, x.max);
let pos=900.0;
if pos<=x.max {
x.pos=pos;
}
else
{
println!("{} The entered value is greater than the it {}",pos,x.max);
}
println!("{} Moves at {}",x.name,x.pos);
x.report();

    // Z: the build plate. It drops one layer (0.04 mm) after every layer.
    let mut z = Axis {name:"z".to_string(),max:0.0,pos:0.0};
    for layer in 1..=4 {
        z.pos = z.pos - 0.04;
        println!("layer {} {} at {}", layer, z.name, z.pos);
    }
}
