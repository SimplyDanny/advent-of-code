advent_of_code::solution!(2);

use advent_of_code::{parse_as_int, parse_lines};
use itertools::Itertools;
use nom::{character::complete::space1, multi::separated_list1};

pub fn part_one(input: &str) -> Option<u32> {
    let result = parse_lines(input, &line_parser).fold(0, |acc, report| {
        acc + (is_safe(&report, None) == Safety::Safe) as u32
    });
    Some(result)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut number_of_safe_reports = 0;
    for report in parse_lines(input, &line_parser) {
        match is_safe(&report, None) {
            Safety::Safe => number_of_safe_reports += 1,
            Safety::Unsafe(index) => {
                number_of_safe_reports += (is_safe(&report, Some(index)) == Safety::Safe
                    || is_safe(&report, Some(index.saturating_sub(1))) == Safety::Safe
                    || is_safe(&report, Some(index + 1)) == Safety::Safe)
                    as u32;
            }
        }
    }
    Some(number_of_safe_reports)
}

#[derive(PartialEq)]
enum Safety {
    Safe,
    Unsafe(usize),
}

fn is_safe(report: &Vec<u32>, skip: Option<usize>) -> Safety {
    let filtered_reports = report
        .iter()
        .enumerate()
        .filter_map(|(i, level)| match skip {
            Some(index) if i == index => None,
            _ => Some(level),
        })
        .tuple_windows();
    let mut first_unsafe_index = 0 as usize;
    let mut is_increasing = true;
    let mut is_decreasing = true;
    let mut safe_difference = true;
    for (first, second) in filtered_reports {
        is_increasing &= first < second;
        is_decreasing &= first > second;
        safe_difference &= first.abs_diff(*second) <= 3;
        if !(is_increasing || is_decreasing) || !safe_difference {
            return Safety::Unsafe(first_unsafe_index);
        }
        first_unsafe_index += 1;
    }
    Safety::Safe
}

fn line_parser(line: &str) -> Vec<u32> {
    match separated_list1(space1, parse_as_int)(line) {
        Ok(("", list)) => list,
        _ => panic!("Unexpected input line '{}'", line),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(2));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(4));
    }
}
