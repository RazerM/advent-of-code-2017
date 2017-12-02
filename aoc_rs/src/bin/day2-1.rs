use std::cmp::{max, min};
use std::fs::File;
use std::io::{BufReader, BufRead};

fn main() {
    let f = File::open("../input/2.txt").expect("file not found");
    let file = BufReader::new(&f);

    let mut checksum = 0;

    for line in file.lines() {
        let line = line.unwrap();
        let mut split = line.split("\t");

        let mut n_min: i32 = split.next().unwrap().parse().unwrap();
        let mut n_max = n_min;

        for s in split {
            let n: i32 = s.parse().unwrap();
            n_min = min(n_min, n);
            n_max = max(n_max, n);
        }
        checksum += n_max - n_min;
    }
    println!("{}", checksum);
}
