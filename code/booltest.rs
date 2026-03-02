#![allow(warnings)]
use std::cmp::{max, min};
use std::io::{stdin, stdout, BufWriter, Write};

#[derive(Default)]
struct boolcirc {
    buffer: Vec<bool>,
    prob: f32,
}

impl boolcirc {
    fn new(qubit: &u32, prob: &f32) -> boolcirc {
        boolcirc {
            buffer: Vec::new(),
            prob: prob,
        }
    }
}

fn main() {
    let out = &mut BufWriter::new(stdout());

    let mut values: Vec<u64> = (0..n).map(|_| scan.next::<u64>()).collect();

    for i in 1..n {
        values[i] += values[i - 1];
    }

    for _ in 0..q {
        let a = scan.next::<usize>();
        let b = scan.next::<usize>();
        if a == 1 {
            writeln!(out, "{}", values[b - 1]);
        } else {
            writeln!(out, "{}", values[b - 1] - values[a - 2]);
        }
    }
}
