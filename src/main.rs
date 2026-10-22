use minidb::{DB_NAME, MAX_KEY, can_add, show_banner};

fn main() {
    let key_len: u8 = 4;
    // let temp:f64=23.5;
    //   let  online:bool=true;
    //   let  grade:char='A';
    let entry: (f64, bool, char) = (23.5, true, 'A');
    let (temp, online, grade) = entry;
    let keys: [&str; 3] = ["temperature", "pressure", "level"];

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
    println!(
        "the key.0={},the key.1={},the key.2={}",
        keys[0], keys[1], keys[2]
    );
    println!("the key length is={}", keys.len());
    println!(
        "key_length {} ,temp {}, is_it_online {}, what_is_the_grade {}",
        key_len, temp, online, grade
    );
}
