struct Axis {
    name: String,
    max: f64,
}

fn main() {
    let mut x = Axis { name: "X".to_string(), max: 500.0 };
    X.max=600.0;
    println!("{} travels {}", x.name, x.max);
}
