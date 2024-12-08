use std::fmt::Display;

use nom::{character::complete::digit1, combinator::map_res, error::FromExternalError, IResult};

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

pub struct ParseError {
    message: String,
}

impl ParseError {
    pub fn new(message: String) -> Self {
        Self { message }
    }
}

impl FromExternalError<&str, ParseError> for ParseError {
    fn from_external_error(input: &str, _: nom::error::ErrorKind, error: ParseError) -> Self {
        ParseError {
            message: format!("Unable to parse input {}: {}", input, error),
        }
    }
}

impl nom::error::ParseError<&str> for ParseError {
    fn from_error_kind(input: &str, _: nom::error::ErrorKind) -> Self {
        ParseError {
            message: format!("Unable to parse input {}", input),
        }
    }

    fn append(_: &str, _: nom::error::ErrorKind, other: Self) -> Self {
        let message = format!("{}: {}", other.message, other.message);
        Self { message }
    }
}

impl Display for ParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.message)
    }
}

pub type Coordinate = (usize, usize);

pub trait MatrixVisitor<T> {
    fn visit(&mut self, _: &mut T, _: Coordinate) {}
    fn post_visit(&mut self, _: &mut Matrix<T>) {}
    fn reset(&mut self) {}
}

pub struct Matrix<T> {
    data: Vec<Vec<T>>,
    rows: usize,
    columns: usize,
}

impl<T: Copy> Matrix<T> {
    pub fn new(data: Vec<Vec<T>>) -> Self {
        let rows = data.len();
        assert!(rows > 0);
        let columns = data[0].len();
        Self {
            data,
            rows,
            columns,
        }
    }

    pub fn size(&self) -> Coordinate {
        (self.rows, self.columns)
    }

    pub fn visit_elements_row_wise<V: MatrixVisitor<T>>(&mut self, visitor: &mut V) {
        for row in 0..self.rows {
            visitor.reset();
            for col in 0..self.columns {
                visitor.visit(&mut self.data[row][col], (row, col));
                visitor.post_visit(self);
            }
        }
    }

    pub fn visit_elements_column_wise<V: MatrixVisitor<T>>(&mut self, visitor: &mut V) {
        for col in 0..self.columns {
            visitor.reset();
            for row in 0..self.rows {
                visitor.visit(&mut self.data[row][col], (row, col));
            }
        }
    }

    pub fn visit_elements_diagonal_wise<V: MatrixVisitor<T>>(&mut self, visitor: &mut V) {
        for row in 0..self.rows {
            visitor.reset();
            let mut col = 0;
            let mut r = row;
            while r < self.rows {
                visitor.visit(&mut self.data[r][col], (r, col));
                r += 1;
                col += 1;
            }
        }
        for col in 1..self.columns {
            visitor.reset();
            let mut row = 0;
            let mut c = col;
            while c < self.columns {
                visitor.visit(&mut self.data[row][c], (row, c));
                row += 1;
                c += 1;
            }
        }
    }

    pub fn visit_elements_anti_diagonal_wise<V: MatrixVisitor<T>>(&mut self, visitor: &mut V) {
        for row in 0..self.rows {
            visitor.reset();
            let mut col = self.columns - 1;
            let mut r = row;
            while r < self.rows {
                visitor.visit(&mut self.data[r][col], (r, col));
                r += 1;
                col = col.saturating_sub(1);
            }
        }
        for col in (0..self.columns - 1).rev() {
            visitor.reset();
            let mut row = 0;
            let mut c = col as isize;
            while c >= 0 {
                visitor.visit(&mut self.data[row][c as usize], (row, c as usize));
                row += 1;
                c = c.saturating_sub(1);
            }
        }
    }

    pub fn get(&mut self, coordinate: Coordinate) -> Option<&mut T> {
        let (row, col) = coordinate;
        if row < self.rows && col < self.columns {
            Some(&mut self.data[row][col])
        } else {
            None
        }
    }

    pub fn find(&self, element: T) -> Option<Coordinate>
    where
        T: PartialEq,
    {
        for row in 0..self.rows {
            for col in 0..self.columns {
                if self.data[row][col] == element {
                    return Some((row, col));
                }
            }
        }
        None
    }
}
