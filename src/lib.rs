mod config;
pub use config::{DB_NAME, MAX_KEY};

pub fn can_add(count: usize) -> bool {
    count < MAX_KEY
}
pub fn show_banner(host: &str, port: u16) {
    println!("{} listening on {}:{}", DB_NAME, host, port);
}
