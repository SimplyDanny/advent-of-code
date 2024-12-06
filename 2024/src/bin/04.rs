advent_of_code::solution!(4);

use advent_of_code::{Coordinate, Matrix, MatrixVisitor};
use itertools::Itertools;

pub fn part_one(input: &str) -> Option<u32> {
    let matrix = Matrix::new(input.lines().map(Vec::from).collect::<Vec<Vec<u8>>>());

    let mut xmas = Xmas::new([b'X', b'M', b'A', b'S']);
    let mut samx = Xmas::new([b'S', b'A', b'M', b'X']);

    matrix.visit_elements_row_wise(&mut xmas);
    matrix.visit_elements_row_wise(&mut samx);

    matrix.visit_elements_column_wise(&mut xmas);
    matrix.visit_elements_column_wise(&mut samx);

    matrix.visit_elements_diagonal_wise(&mut xmas);
    matrix.visit_elements_diagonal_wise(&mut samx);

    matrix.visit_elements_anti_diagonal_wise(&mut xmas);
    matrix.visit_elements_anti_diagonal_wise(&mut samx);

    Some(xmas.matches + samx.matches)
}

pub fn part_two(input: &str) -> Option<u32> {
    let matrix = Matrix::new(input.lines().map(Vec::from).collect::<Vec<Vec<u8>>>());

    let mut mas = Mas::new([b'M', b'A', b'S']);
    let mut sam = Mas::new([b'S', b'A', b'M']);

    matrix.visit_elements_diagonal_wise(&mut mas);
    matrix.visit_elements_diagonal_wise(&mut sam);

    matrix.visit_elements_anti_diagonal_wise(&mut mas);
    matrix.visit_elements_anti_diagonal_wise(&mut sam);

    mas.center_points.append(&mut sam.center_points);
    let result = mas
        .center_points
        .into_iter()
        .counts()
        .into_values()
        .filter(|count| count == &2)
        .count() as u32;
    Some(result)
}

struct Xmas {
    buffer: [u8; 4],
    index: usize,
    expectation: [u8; 4],
    matches: u32,
}

impl Xmas {
    fn new(expectation: [u8; 4]) -> Self {
        Self {
            buffer: [0; 4],
            index: 0,
            expectation,
            matches: 0,
        }
    }

    fn add(&mut self, c: u8) {
        self.buffer[self.index] = c;
        self.index += 1;
    }

    fn is_complete(&self) -> bool {
        self.buffer == self.expectation
    }
}

impl MatrixVisitor<u8> for Xmas {
    fn visit(&mut self, c: u8, _: Coordinate) {
        if c == self.expectation[0] {
            self.reset();
            self.add(c);
        } else if self.index == 1 && c == self.expectation[1] {
            self.add(c);
        } else if self.index == 2 && c == self.expectation[2] {
            self.add(c);
        } else if self.index == 3 && c == self.expectation[3] {
            self.add(c);
        } else {
            self.reset();
        }
        self.matches += self.is_complete() as u32
    }

    fn reset(&mut self) {
        self.index = 0;
        self.buffer.fill(0);
    }
}

struct Mas {
    buffer: [u8; 3],
    index: usize,
    expectation: [u8; 3],
    current_center: Coordinate,
    center_points: Vec<Coordinate>,
}

impl Mas {
    fn new(expectation: [u8; 3]) -> Self {
        Self {
            buffer: [0; 3],
            index: 0,
            expectation,
            current_center: (0, 0),
            center_points: Vec::new(),
        }
    }

    fn add(&mut self, c: u8) {
        self.buffer[self.index] = c;
        self.index += 1;
    }

    fn is_complete(&self) -> bool {
        self.buffer == self.expectation
    }
}

impl MatrixVisitor<u8> for Mas {
    fn visit(&mut self, c: u8, coordinate: Coordinate) {
        if c == self.expectation[0] {
            self.reset();
            self.add(c);
        } else if self.index == 1 && c == self.expectation[1] {
            self.add(c);
            self.current_center = coordinate;
        } else if self.index == 2 && c == self.expectation[2] {
            self.add(c);
        } else {
            self.reset();
        }
        if self.is_complete() {
            self.center_points.push(self.current_center);
        }
    }

    fn reset(&mut self) {
        self.index = 0;
        self.buffer.fill(0);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(18));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(9));
    }
}
