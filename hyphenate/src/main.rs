
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


fn do_hyphenate(h: HyphenParams) -> Result<String, Fault> {
    let _english = String::from("en");
    let _dutch = String::from("nl");

    let syllables = 
        if h.lang == _english {
            hyphenate(h.word.as_str(), Lang::English)
        } else if h.lang == _dutch {
            hyphenate(h.word.as_str(), Lang::Dutch)
        } else { // default to english
            hyphenate(h.word.as_str(), Lang::English)
    };
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