struct Axis {
name: String,
max:f64,
pos:f64,
}

fn main() {
    let mut x= Axis {name:"x".to_string(),max:500.0,pos:450.0};
x.max =480.0;
    x.pos = 480.0;
    println!("{} travels {}", x.name, x.max);
pos=900.0;
if pos<=x.max {
x.pos=pos;
}
else
{
println!("Refused");
}
println!("{} Moves at {}",x.name,x.pos);
}
