
# Install rust
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

# Install hyphenation server
cd ./hyphenate
cargo build
cd ..

# Install python environment and requirements
python -m venv venv
source venv/bin/activate
pip install pip --upgrade
pip install poetry
poetry install

# Run RPC server for hyphenation
cargo run --manifest-path hyphenate/Cargo.toml &

# Run API
python main.py
