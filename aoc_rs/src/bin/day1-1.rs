use std::fs::File;
use std::io::prelude::*;

fn main() {
    let mut f = File::open("../input/1.txt").expect("file not found");
    let mut contents = String::new();
    f.read_to_string(&mut contents).unwrap();
    let trimmed = contents.trim();
    let numbers: Vec<u32> =  trimmed.chars().map(|x| x.to_digit(10).unwrap()).collect();
    let step = numbers.len() / 2;
    let mut total: u32 = 0;
    let mut n;

    for (i, &v) in numbers.iter().enumerate() {
        n = i + step;
        if n >= numbers.len() {
            n -= numbers.len()
        }
        if v == numbers[n] {
            total += v
        }
    }
    println!("{}", total);
}
