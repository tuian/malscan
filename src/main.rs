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
    let malscan_version: &str = "1.8.0";

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
             BrightYellow.paint("  * Update: Downloading the latest malscan malware definitions."));

    // Pulling in the RFXN databases
    signatures_updater("https://repo.malscan.org/signatures/rfxn.hdb.",
                    "/var/lib/malscan/malscan.hdb",
                    "Updating the malscan HEX signature database.");
    signatures_updater("https://repo.malscan.org/signatures/rfxn.ndb",
                    "/var/lib/malscan/malscan.ndb",
                    "Updating the malscan MD5/SHA signature database.");

    // Running the freshclam updater
    clamav_updater();

    // Completing the Malscan signature update portion
    println!("{}",
             BrightGreen.paint("  * Update: All malscan signatures updated successfully."));
    println!("");

}

// This function invokes freshclam to update the clamav files.
fn clamav_updater() {

    use std::process::Command;

    Command::new("/usr/bin/freshclam")
        .arg("--datadir=/var/lib/malscan")
        .arg("--config-file=/etc/malscan/freshclam.conf")
	.output()
        .unwrap_or_else(|e| panic!("failed to execute process: {}", e));
    println!("  * Update: ClamAV Signature Databases Updated.");
}

// This function manually fetches and updates malscan custom signatures
fn signatures_updater(url: &str, file_name: &str, signature_database_text: &str) {

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
        Ok(_) => println!("  * Update: {}", signature_database_text),
    }

}
