advent_of_code::solution!(6);

use advent_of_code::{parse_lines, Coordinate, Matrix, MatrixVisitor, ParseError};
use itertools::Itertools;
use nom::{character::complete::one_of, combinator::map_res, multi::many1, IResult};
use std::collections::HashSet;

pub fn part_one(input: &str) -> Option<u32> {
    let mut grid = Matrix::new(parse_lines(input, &line_parser).collect());
    let guard_position = grid.find(Field::Guard).expect("Guard not found on the map");
    run_guard(guard_position, &mut grid)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut grid = Matrix::new(parse_lines(input, &line_parser).collect());
    let guard_position = grid.find(Field::Guard).expect("Guard not found on the map");
    let mut visitor = Visitor {
        guard_origin: guard_position,
        changed_coordinate: None,
        successfully_placed_obstacles: 0,
    };
    grid.visit_elements_row_wise(&mut visitor);
    Some(visitor.successfully_placed_obstacles)
}

fn run_guard(guard_origin: Coordinate, grid: &mut Matrix<Field>) -> Option<u32> {
    let mut guard = Guard::new(guard_origin, grid.size());
    let mut visited_fields = HashSet::new();
    loop {
        if guard.is_out_of_grid() {
            return Some(
                visited_fields
                    .into_iter()
                    .unique_by(|x: &((isize, isize), _)| x.0)
                    .count() as u32,
            );
        }
        if !visited_fields.insert((guard.position, guard.direction)) {
            // Guard is stuck in a loop.
            return None;
        }
        guard.step(grid);
    }
}

struct Visitor {
    guard_origin: Coordinate,
    changed_coordinate: Option<Coordinate>,
    successfully_placed_obstacles: u32,
}

impl MatrixVisitor<Field> for Visitor {
    fn visit(&mut self, element: &mut Field, coordinate: Coordinate) {
        if element == &Field::Free {
            *element = Field::Obstacle;
            self.changed_coordinate = Some(coordinate);
        }
    }

    fn post_visit(&mut self, grid: &mut Matrix<Field>) {
        if run_guard(self.guard_origin, grid).is_none() {
            self.successfully_placed_obstacles += 1;
        }
        if let Some(coordinate) = self.changed_coordinate {
            if let Some(field) = grid.get(coordinate) {
                *field = Field::Free;
                self.changed_coordinate = None;
            }
        }
    }
}

struct Guard {
    position: (isize, isize),
    direction: Direction,
    grid_size: Coordinate,
}

impl Guard {
    fn new(position: Coordinate, grid_size: Coordinate) -> Self {
        let position = (position.0 as isize, position.1 as isize);
        Self {
            position,
            direction: Direction::Up,
            grid_size,
        }
    }

    fn step(&mut self, grid: &mut Matrix<Field>) {
        let next = match self.direction {
            Direction::Up => (self.position.0 - 1, self.position.1),
            Direction::Down => (self.position.0 + 1, self.position.1),
            Direction::Left => (self.position.0, self.position.1 - 1),
            Direction::Right => (self.position.0, self.position.1 + 1),
        };
        if grid.get((next.0 as usize, next.1 as usize)) == Some(&mut Field::Obstacle) {
            self.turn();
            self.step(grid);
            return;
        }
        self.position = next;
    }

    fn turn(&mut self) {
        self.direction = match self.direction {
            Direction::Up => Direction::Right,
            Direction::Right => Direction::Down,
            Direction::Down => Direction::Left,
            Direction::Left => Direction::Up,
        }
    }

    fn is_out_of_grid(&self) -> bool {
        self.position.0 < 0
            || self.position.1 < 0
            || self.position.0 >= self.grid_size.0 as isize
            || self.position.1 >= self.grid_size.1 as isize
    }
}

#[derive(Copy, Clone, PartialEq, Eq, Hash)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Copy, Clone, PartialEq)]
enum Field {
    Free,
    Obstacle,
    Guard,
}

impl Field {
    fn from_char(c: char) -> Result<Self, ParseError> {
        match c {
            '.' => Ok(Field::Free),
            '#' => Ok(Field::Obstacle),
            '^' => Ok(Field::Guard),
            _ => Err(ParseError::new(c.to_string())),
        }
    }
}

fn line_parser(line: &str) -> Vec<Field> {
    let result: IResult<&str, Vec<Field>, ParseError> =
        many1(map_res(one_of(".#^"), Field::from_char))(line);
    match result {
        Ok(("", fields)) => fields,
        _ => panic!("Unexpected input line '{}'", line),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(41));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(6));
    }
}
