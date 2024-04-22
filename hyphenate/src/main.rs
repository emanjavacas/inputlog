
extern crate xml_rpc;
extern crate serde;
extern crate hypher;

use xml_rpc::{Fault, Server};
use std::net::{IpAddr, Ipv4Addr, SocketAddr};
use serde::{Serialize, Deserialize};
use hypher::{hyphenate, Lang};
use dotenv::dotenv;


#[derive(Clone, Debug, Serialize, Deserialize)]
struct HyphenParams {
    pub word: String,
    pub lang: String,
    pub delimiter: String,
}

fn parse_lang(lang: &str) -> Lang {
    match lang {
        "en" => Lang::English,
        "nl" => Lang::Dutch,
        "es" => Lang::Spanish,
        "fr" => Lang::French,
        "de" => Lang::German,
        _ => Lang::English
    }
}

fn do_hyphenate(h: HyphenParams) -> Result<String, Fault> {
    let syllables = hyphenate(h.word.as_str(), parse_lang(&h.lang));
    Ok(syllables.join(h.delimiter.as_str()))
}

fn main() {
    dotenv().ok();
    let port = std::env::var("HYPHENATERPCPORT").expect("HYPHENATERPCPORT must be set");
    let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), port.parse::<u16>().unwrap());
    let mut server = Server::new();

    server.register_simple("hyphenate", &do_hyphenate);

    let bound_server = server.bind(&socket).unwrap();

    println!("Running server on port: {}", port);
    bound_server.run();
}