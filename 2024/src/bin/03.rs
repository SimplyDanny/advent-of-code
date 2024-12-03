advent_of_code::solution!(3);

use std::num::ParseIntError;

use regex::Regex;

pub fn part_one(input: &str) -> Option<u32> {
    sum_up_multiplications(input, true).ok()
}

pub fn part_two(input: &str) -> Option<u32> {
    sum_up_multiplications(input, false).ok()
}

fn sum_up_multiplications(line: &str, all: bool) -> Result<u32, ParseIntError> {
    let operations_regex =
        Regex::new(r"do\(\)|don't\(\)|mul\((?<lhs>\d{1,3}),(?<rhs>\d{1,3})\)").unwrap();
    let mut sum = 0;
    let mut enabled = true;
    for capture in operations_regex.captures_iter(line) {
        let operation = &capture[0];
        if operation == "do()" {
            enabled = true;
        } else if operation == "don't()" {
            enabled = false;
        } else if enabled || all {
            sum += capture["lhs"].parse::<u32>()? * capture["rhs"].parse::<u32>()?;
        }
    }
    Ok(sum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file_part(
            "examples", DAY, 1,
        ));
        assert_eq!(result, Some(161));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file_part(
            "examples", DAY, 2,
        ));
        assert_eq!(result, Some(48));
    }
}
