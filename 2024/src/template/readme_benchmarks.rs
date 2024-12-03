/// Module that updates the readme me with timing information.
/// The approach taken is similar to how `aoc-readme-stars` handles this.
use std::{fs, io};

use crate::template::timings::Timings;
use crate::template::Day;

static MARKER: &str = "<!--- benchmarking table --->";

#[allow(dead_code)]
#[derive(Debug)]
pub enum Error {
    Parser(String),
    IO(io::Error),
}

impl From<std::io::Error> for Error {
    fn from(e: std::io::Error) -> Self {
        Error::IO(e)
    }
}

pub struct TablePosition {
    pos_start: usize,
    pos_end: usize,
}

#[must_use]
pub fn get_path_for_bin(day: Day) -> String {
    format!("./src/bin/{day}.rs")
}

fn locate_table(readme: &str) -> Result<TablePosition, Error> {
    let matches: Vec<_> = readme.match_indices(MARKER).collect();

    if matches.len() > 2 {
        return Err(Error::Parser(
            "{}: too many occurences of marker in README.".into(),
        ));
    }

    let pos_start = matches
        .first()
        .map(|m| m.0)
        .ok_or_else(|| Error::Parser("Could not find table start position.".into()))?;

    let pos_end = matches
        .last()
        .map(|m| m.0 + m.1.len())
        .ok_or_else(|| Error::Parser("Could not find table end position.".into()))?;

    Ok(TablePosition { pos_start, pos_end })
}

fn construct_table(prefix: &str, timings: Timings, total_millis: f64) -> String {
    let header = format!("{prefix} Benchmarks");

    let mut lines: Vec<String> = vec![
        MARKER.into(),
        header,
        String::new(),
        "| Day | Part 1 | Part 2 |".into(),
        "| :---: | :---: | :---:  |".into(),
    ];

    for timing in timings.data {
        let path = get_path_for_bin(timing.day);
        lines.push(format!(
            "| [Day {}]({}) | `{}` | `{}` |",
            timing.day.into_inner(),
            path,
            timing.part_1.unwrap_or_else(|| "-".into()),
            timing.part_2.unwrap_or_else(|| "-".into())
        ));
    }

    lines.push(String::new());
    lines.push(format!("**Total: {total_millis:.2}ms**"));
    lines.push(MARKER.into());

    lines.join("\n")
}

fn update_content(s: &mut String, timings: Timings, total_millis: f64) -> Result<(), Error> {
    let positions = locate_table(s)?;
    let table = construct_table("##", timings, total_millis);
    s.replace_range(positions.pos_start..positions.pos_end, &table);
    Ok(())
}

pub fn update(timings: Timings) -> Result<(), Error> {
    let path = "README.md";
    let mut readme = String::from_utf8_lossy(&fs::read(path)?).to_string();
    let total_millis = timings.total_millis();
    update_content(&mut readme, timings, total_millis)?;
    fs::write(path, &readme)?;
    Ok(())
}
