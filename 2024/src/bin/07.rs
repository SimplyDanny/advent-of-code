advent_of_code::solution!(7);

use advent_of_code::{parse_as_big_int, parse_lines, ParseError};
use itertools::Itertools;
use nom::{
    bytes::complete::tag, character::complete::space1, combinator::map_res, multi::separated_list1,
    sequence::separated_pair,
};

pub fn part_one(input: &str) -> Option<u64> {
    let operators = [Operation::Add, Operation::Multiply];
    let result = parse_lines(input, &line_parser)
        .filter_map(|equation| equation.can_be_solved(&operators).then(|| equation.result))
        .sum();
    Some(result)
}

pub fn part_two(input: &str) -> Option<u64> {
    let operators = [Operation::Add, Operation::Multiply, Operation::Concatenate];
    let result = parse_lines(input, &line_parser)
        .filter_map(|equation| equation.can_be_solved(&operators).then(|| equation.result))
        .sum();
    Some(result)
}

enum Operation {
    Add,
    Multiply,
    Concatenate,
}

impl Operation {
    fn apply(&self, a: u64, b: u64) -> u64 {
        match self {
            Self::Add => a + b,
            Self::Multiply => a * b,
            Self::Concatenate => format!("{}{}", a, b).parse().unwrap(),
        }
    }
}

struct Equation {
    result: u64,
    operands: Vec<u64>,
}

impl Equation {
    fn new(result: u64, operands: Vec<u64>) -> Self {
        Self { result, operands }
    }

    fn can_be_solved(&self, operators: &[Operation]) -> bool {
        let operators = (0..self.operands.len() - 1)
            .map(|_| operators)
            .multi_cartesian_product();
        for combination in operators {
            let mut result = self.operands[0];
            for (next_operand, operation) in self.operands.iter().skip(1).zip(combination) {
                result = operation.apply(result, *next_operand);
            }
            if result == self.result {
                return true;
            }
        }
        false
    }
}

fn line_parser(line: &str) -> Equation {
    let mut parser = map_res(
        separated_pair(
            parse_as_big_int,
            tag(": "),
            separated_list1(space1, parse_as_big_int),
        ),
        |(result, operands)| Ok::<_, ParseError>(Equation::new(result, operands)),
    );
    match parser(line) {
        Ok(("", equation)) => equation,
        _ => panic!("Unexpected input line '{}'", line),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(3749));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(11387));
    }
}
