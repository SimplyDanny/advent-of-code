use nom::{character::complete::digit1, combinator::map_res, IResult};

pub mod template;

pub fn parse_as_int(input: &str) -> IResult<&str, u32> {
    map_res(digit1, |s: &str| s.parse::<u32>())(input)
}

pub fn parse_lines<'a, LineParser, Result>(
    input: &'a str,
    line_parser: &'a LineParser,
) -> impl Iterator<Item = Result> + 'a
where
    LineParser: Fn(&'a str) -> Result,
{
    input.lines().map(line_parser)
}
