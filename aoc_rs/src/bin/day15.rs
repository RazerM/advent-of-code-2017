const LOW16: u64 = 0xFFFF;


struct Generator {
    current: u64,
    factor: u64,
    multiples_of: Option<u64>,
}

impl Iterator for Generator {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            self.current *= self.factor;
            self.current %= 2147483647;

            if let Some(mo) = self.multiples_of {
                if self.current % mo != 0 {
                    continue
                }
            }

            return Some(self.current & LOW16);
        }
    }
}

fn generator(start: u64, factor: u64, multiples_of: Option<u64>) -> Generator {
    Generator { current: start, factor, multiples_of }
}


fn sum_equal(gen_a: Generator, gen_b: Generator, limit: usize) -> usize {
    gen_a
        .zip(gen_b)
        .take(limit)
        .filter(|&(x, y)| x == y)
        .count()
}


fn part1(start_a: u64, start_b: u64, factor_a: u64, factor_b: u64) {
    let gen_a = generator(start_a, factor_a, None);
    let gen_b = generator(start_b, factor_b, None);
    println!("Part 1: {}", sum_equal(gen_a, gen_b, 40_000_000));
}


fn part2(start_a: u64, start_b: u64, factor_a: u64, factor_b: u64) {
    let gen_a = generator(start_a, factor_a, Some(4));
    let gen_b = generator(start_b, factor_b, Some(8));
    println!("Part 2: {}", sum_equal(gen_a, gen_b, 5_000_000));
}


fn main() {
    let start_a = 679;
    let start_b = 771;

    let factor_a = 16807;
    let factor_b = 48271;

    part1(start_a, start_b, factor_a, factor_b);
    part2(start_a, start_b, factor_a, factor_b);
}
