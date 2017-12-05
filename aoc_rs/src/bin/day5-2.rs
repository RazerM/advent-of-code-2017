use std::fs::File;
use std::io::{BufReader, BufRead};

fn main() {
    let f = File::open("../input/5.txt").expect("file not found");
    let file = BufReader::new(&f);

    let mut pos: i32 = 0;
    let mut upos: usize = 0;
    let mut steps: i32 = 0;

    let mut instructions: Vec<_> = file
        .lines()
        .filter_map(|l| l.unwrap().parse::<i32>().ok())
        .collect();

    let mut jump;

    while 0 <= pos && upos < instructions.len() {
        jump = instructions[upos];
        instructions[upos] += if jump >= 3 {-1} else {1};
        pos += jump;
        upos = pos as usize;
        steps += 1;
    }

    println!("{}", steps);
}
