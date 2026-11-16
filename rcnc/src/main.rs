struct Axis {
name: String,
max:f64,
pos:f64,
}

fn main() {
    let mut x= Axis {name:"x".to_string(),max:500.0,pos:450.0};
    x.max=600.0;
    x.pos = 480.0;
    x.pos = 900.0;
    if x.pos=<480.0 then {println!("The value accepted") else{println!("Enter the value below 480.0")}
    println!("{} travels {}", x.name, x.max);
    println!("{} at {}", x.name, x.pos);
}
