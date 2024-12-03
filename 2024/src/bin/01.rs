advent_of_code::solution!(1);

use advent_of_code::{parse_as_int, parse_lines};
use itertools::{multiunzip, Itertools};
use nom::{character::complete::space1, sequence::separated_pair};

pub fn part_one(input: &str) -> Option<u32> {
    let (lhs, rhs): (Vec<u32>, Vec<u32>) = multiunzip(parse_lines(input, &line_parser));
    let result = lhs
        .iter()
        .sorted()
        .zip(rhs.into_iter().sorted())
        .map(|(l, r)| l.abs_diff(r))
        .sum();
    Some(result)
}

pub fn part_two(input: &str) -> Option<u32> {
    let (lhs, rhs): (Vec<u32>, Vec<u32>) = multiunzip(parse_lines(input, &line_parser));
    let number_count = rhs.iter().counts_by(|x| x);
    let result = lhs.into_iter().fold(0, |acc, num| {
        acc + num * *number_count.get(&num).unwrap_or(&0) as u32
    });
    Some(result)
}

fn line_parser(line: &str) -> (u32, u32) {
    match separated_pair(parse_as_int, space1, parse_as_int)(line) {
        Ok(("", (lhs, rhs))) => (lhs, rhs),
        _ => panic!("Unexpected input line '{}'", line),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(11));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(31));
    }
}
