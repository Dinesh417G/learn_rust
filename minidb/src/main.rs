use minidb::{DB_NAME, MAX_KEY, can_add, show_banner};

fn main() {
    let key_len: u8 = 4;
    // let temp:f64=23.5;
    //   let  online:bool=true;
    //   let  grade:char='A';
    let entry: (f64, bool, char) = (23.5, true, 'A');
    let (temp, online, grade) = entry;
    let keys: [&str; 3] = ["temperature", "pressure", "level"];
    // let total = key_len * 100;
    // println!("{}",total);
    let port: u16 = 7878;
    let mut count = 0;
    count += 1;
    let (host, p) = ("127.0.0.1", port);
    println!("Hello, world iam in!");
    println!("{}", DB_NAME);
    println!("{}", MAX_KEY);
    println!("{}", port);
    show_banner(host, p);
    println!("{}", can_add(count));
    for x in keys.iter() {

        println!("the keys ={}", x);
    }
    for y in 0..keys.len() {
        println!("the keys{}={}", keys[y],y);
    }
    let stauts = if  online { "online"} else { "ofline" };
    let mut slots=0;
    let filled =loop{
        slots+=1;
        println!("slots={}", slots);
        if slots==2{
            break slots;
        }

    };

    let mut key = String::new();
    key.push_str("Pressure");
    let help ="Commands:\n  set\n  get\n  delete";
    println!("{}", help);
    if key !=""{
        println!("the string is ={}", key);
    }
    else {
        println!("nothing yet");
    }
    let ok = "\u{2714} saved";
    println!("{}",ok);
println!("the length is {}",ok.len());
    println!("the char is {}",ok.chars().last().unwrap());
    println!("the count is {}",ok.chars().count());
    println!("{}",filled);
    println!("stauts={}", stauts);
    println!("the key length is={}", keys.len());
    println!(
        "key_length {} ,temp {}, is_it_online {}, what_is_the_grade {}",
        key_len, temp, online, grade
    );
}
