advent_of_code::solution!(5);

use std::{cmp::Ordering, num::ParseIntError};

use advent_of_code::{parse_as_int, parse_lines};
use itertools::{Either, Itertools};
use nom::{
    branch::alt, bytes::complete::tag, combinator::map_res, multi::separated_list1,
    sequence::separated_pair,
};

pub fn part_one(input: &str) -> Option<u32> {
    solve(input).map(|result| result.0)
}

fn solve(input: &str) -> Option<(u32, u32)> {
    let lines = parse_lines(input, &line_parser);
    let (relations, mut page_lines): (Vec<(u32, u32)>, Vec<Vec<u32>>) = lines
        .filter_map(|line| line)
        .partition_map(|input| match input {
            Input::Relation(a, b) => Either::Left((a, b)),
            Input::Pages(pages) => Either::Right(pages),
        });
    let mut ordered_pages = 0;
    let mut corrected_pages = 0;
    'page_loop: for pages in page_lines.iter_mut() {
        for relation in relations.iter() {
            if let Some(first_index) = pages.iter().position(|page| *page == relation.0) {
                if let Some(second_index) = pages.iter().position(|page| *page == relation.1) {
                    if first_index <= second_index {
                        continue;
                    }
                    pages.sort_by(|a, b| {
                        match relations
                            .iter()
                            .find(|(x, y)| *x == *a && *y == *b || *x == *b && *y == *a)
                        {
                            Some((left, _)) => {
                                if *left == *a {
                                    Ordering::Less
                                } else {
                                    Ordering::Greater
                                }
                            }
                            None => Ordering::Equal,
                        }
                    });
                    corrected_pages += pages[pages.len() / 2];
                    continue 'page_loop;
                }
            }
        }
        ordered_pages += pages[pages.len() / 2];
    }
    Some((ordered_pages, corrected_pages))
}

pub fn part_two(input: &str) -> Option<u32> {
    solve(input).map(|result| result.1)
}

enum Input {
    // xx|yy
    Relation(u32, u32),
    // xx,yy,zz
    Pages(Vec<u32>),
}

fn line_parser(line: &str) -> Option<Input> {
    if line.is_empty() {
        return None;
    }
    let relation_parser = map_res(
        separated_pair(parse_as_int, tag("|"), parse_as_int),
        |pair| Ok::<_, ParseIntError>(Input::Relation(pair.0, pair.1)),
    );
    let pages_parser = map_res(separated_list1(tag(","), parse_as_int), |list| {
        Ok::<_, ParseIntError>(Input::Pages(list))
    });
    match alt((relation_parser, pages_parser))(line) {
        Ok(("", input)) => Some(input),
        _ => panic!("Unexpected input line '{}'", line),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(143));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(123));
    }
}
