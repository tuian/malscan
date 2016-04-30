/// Testing file for the Malscan updater

extern crate hyper;
extern crate time;
extern crate term_painter;

use std::env;
use std::error::Error;
use std::io::prelude::*;
use std::fs::File;
use std::path::Path;
use term_painter::ToStyle;
use term_painter::Color::*;
use hyper::Client;
use hyper::header::Connection;

fn main() {

    for argument in env::args() {
        println!("{}", argument);
    }

    // Setting the current Malscan version
    let malscan_version: &str = "0.0.1";

    // Setting the current Malscan signature version
    let signature_version: &str = "Never";

    // Outputting our status information to the terminal
    BrightBlue.with(|| {
        print!("Malscan Version: {} | Signatures Version: {}",
               malscan_version,
               signature_version);
    });

    println!("");
    println!("");

    updater();
}

// The updater function is called whenever the update argument is passed to it.
fn updater() {

    // Starting the Malscan signature update portion.
    println!("{}",
             BrightYellow.paint("  * Update: Downloading the latest Malscan malware definitions."));

    // Pulling in the RFXN databases
    updater_malscan_signatures("https://www.rfxn.org/rfxn.hdb",
                               "/var/lib/malscan/malscan.hdb",
                               "RFXN Signature Database I");
    updater_malscan_signatures("https://www.rfxn.org/rfxn.ndb",
                               "/var/lib/malscan/malscan.ndb",
                               "RFXN Signature Database II");
    updater_freshclam();

    // Completing the Malscan signature update portion
    println!("{}",
             BrightGreen.paint("  * Update: All Malscan signatures updated successfully."));
    println!("");

}

// This function invokes freshclam to update the clamav files.
fn updater_freshclam() {

    use std::process::Command;

    let output = Command::new("/usr/bin/freshclam")
                     .arg("--datadir=/var/lib/malscan")
                     .output()
                     .unwrap_or_else(|e| panic!("failed to execute process: {}", e));
    println!("  * Update: ClamAV Signature Databases Updated. {}",
             output.status);
}

// This function manually fetches and updates malscan custom signatures
fn updater_malscan_signatures(url: &str, file_name: &str, signature_database_name: &str) {

    // Creating our HTTP Client
    let client = Client::new();

    // Creating the outgoing request
    let mut response = client.get(url)
                             .header(Connection::close())
                             .send()
                             .unwrap();

    // Reading the response
    let mut body = String::new();
    response.read_to_string(&mut body).unwrap();

    // Setting up our file path
    let path = Path::new(file_name);
    let display = path.display();

    // Creating the signatures file
    let mut file = match File::create(&path) {
        Err(why) => panic!("couldn't create {}: {}", display, Error::description(&why)),
        Ok(file) => file,
    };

    // Writing the signatures to the file
    match file.write_all(body.as_bytes()) {
        Err(why) => {
            panic!("couldn't write to {}: {}",
                   display,
                   Error::description(&why))
        }
        Ok(_) => {
            println!("  * Update: {} updated. Continuing...",
                     signature_database_name)
        }
    }

}
