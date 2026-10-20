const DB_NAME: &str = "minidb";
const MAX_KEY: usize = 1000;
fn main() {
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
}
fn show_banner(host: &str, port: u16) {
    println!("{} listening on {}:{}", DB_NAME, host, port);
}
fn can_add(count: usize) -> bool {
    count < MAX_KEY
}
