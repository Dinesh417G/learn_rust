# minidb

The database you build while learning Rust. Each milestone uses what the matching
block of videos taught (see `../notes/PROGRESS.md`).

| Milestone | What it can do |
|---|---|
| M1 | In-memory `set / get / delete / list` (`enum Value`, `HashMap<String, Value>`) |
| M2 | Command prompt + CLI; data saved to `db.json` and reloaded at start |
| M3 | Proper errors (`DbError`), no `unwrap()`, tests for every command |
| M4 | Append-only log file with CRC32-checked records; survives a crash |
| M5 | Safe to use from many threads (`Arc<RwLock<..>>`, one writer thread) |
| M6 | TCP server + client |
| M7 | HTTP API with token auth and config (optional) |
| M8 | Benchmarked against SQLite, one proven speed-up |

Start: at M1 the teacher walks you through `cargo init` in this folder.
Commit after every milestone.
