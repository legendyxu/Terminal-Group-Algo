extern crate rustc_serialize;
use rustc_serialize::json::Json;

use std::process::{Command, Stdio};
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::env;
use std::sync::mpsc::{channel};
use std::thread;
use std::fs;
use std::time::{Duration, SystemTime};
use std::path::PathBuf;

fn to_millis(d: Duration) -> u64 {
    (d.as_secs() * 1000) + ((d.subsec_micros() / 1000) as u64)
}

fn main() -> Result<(), io::Error> {
    let is_windows = cfg!(windows);
    // println!("Running Windows: {:?}", is_windows);

    let exe_dir = env::current_exe()?;
    // println!("Exe dir: {}", exe_dir.display());

    let args: Vec<String> = env::args().collect();
    let mut algo_loc: &str;
    let mut replay_loc = PathBuf::from("test_replay.replay");
    //replay_loc = format!("{}{}", exe_dir.as_os_str(), replay_loc).as_str();
    replay_loc = exe_dir.join(replay_loc);

    // println!("Default replay: {:?}", replay_loc);

    match args.get(1) {
        Some(x) => {
            println!("Running algo at: {}", x);
            algo_loc = x;
        },
        None => {
            println!("Arguments: [algo folder location] [(Optional) replay location]");
            return Ok(());
        },
    }
    if args.get(2).is_some() {
        replay_loc = PathBuf::from(args.get(2).unwrap());
    }

    println!("Using replay: {:?}", replay_loc);

    // TODO: make algo_loc a PathBuf instead of dealing with string directly
    if algo_loc.chars().last().unwrap() == '\\' || algo_loc.chars().last().unwrap() == '/' {
        //algo_loc.to_string().truncate(algo_loc.len() - 1);
        algo_loc = &algo_loc[..algo_loc.len()-1];
        println!("removing trailing char {:?}", algo_loc);
    }

    let mut run_command = format!("{}{}", algo_loc, "/run.sh");
    if is_windows {
        run_command = format!("{}{}", algo_loc, "\\run.ps1");
    }

    println!("Running command: {}", run_command);

    let replay_string = fs::read_to_string(replay_loc)?;
    let replay = replay_string.split("\n").collect::<Vec<&str>>();

    //println!("Config: {:#?}", replay.get(0));
    let json_config = Json::from_str(&replay[0]).unwrap();
    let max_time = json_config.find_path(&["timingAndReplay", "waitTimeBotMax"]).unwrap().as_u64().unwrap();
    let max_time =  Duration::from_millis(max_time); // Duration::from_millis(max_time);
    let soft_time = json_config.find_path(&["timingAndReplay", "waitTimeBotSoft"]).unwrap().as_u64().unwrap();
    let soft_time = Duration::from_millis(soft_time);
    //println!("Wait Time Max: {:?}", to_millis(max_time));
    //println!("Wait Time Soft: {:?}", to_millis(soft_time));

    let mut child = Command::new(run_command)
        .stdin(Stdio::piped())
        .stderr(Stdio::inherit())
        .stdout(Stdio::piped())
        .spawn()?;

    let algo_in = child.stdin.take().unwrap();
    let mut algo_in = BufWriter::new(algo_in);

    let algo_out_read = child.stdout.take().unwrap();
    let (algo_out_send, algo_out) = channel();
    thread::spawn(move || {
        for line in BufReader::new(algo_out_read).lines() {
            let _ = algo_out_send.send(line);
        }
    });

    algo_in.write_all(format!("{}{}", replay.get(0).unwrap(), "\n").as_bytes())?;
    algo_in.flush()?;

    for (i, line) in replay.iter().enumerate() {
        if i == 0 {
            continue;
        }

        algo_in.write_all(format!("{}{}", line, "\n").as_bytes())?;
        algo_in.flush()?;

        if line.contains("\"turnInfo\":[0") {
            let now = SystemTime::now();

            match algo_out.recv_timeout(max_time) {
                Ok(Ok(_)) => {
                    // println!("Got Line: {}", line);
                },
                Ok(Err(e)) => {
                    eprintln!("Your algo had an io error: {:#?}", e);
                },
                Err(_) => {
                    eprintln!("Your algo has taken longer than {} milliseconds to submit its \
                     turn, making it lose the match", to_millis(max_time));
                    return Ok(());
                },
            }
            if max_time > now.elapsed().unwrap() {
                match algo_out.recv_timeout(max_time - now.elapsed().unwrap()) {
                    Ok(Ok(_)) => {
                        // println!("Got Line: {}", line);
                        if now.elapsed().unwrap() > soft_time {
                            println!("Warning your algo took {} milliseconds to submit its turn. \
                             It will 1 damage for every second over {} milliseconds.",
                                     to_millis(now.elapsed().unwrap()), to_millis(soft_time));
                        }
                    },
                    Ok(Err(e)) => {
                        eprintln!("Your algo had an io error: {:#?}", e);
                    },
                    Err(_) => {
                        eprintln!("Your algo has taken longer than {} milliseconds \
                          to submit its turn, making it lose the match", to_millis(max_time));
                        return Ok(());
                    },
                }
            }
        }
    }

    Ok(())

}
