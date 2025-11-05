# Install local dependencies

echo "Installing Python dependencies for yt_assistant_api..."
cd yt_assistant_api
sudo apt-get update
sudo apt-get install -y libpq-dev build-essential python3-dev python3-poetry
sudo ln -s /usr/bin/python3 /usr/bin/python
poetry install --with dev --no-interaction
cd ..

echo "Installing Python dependencies for yt_assistant_emb..."
cd yt_assistant_emb
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
# Manually install torch without GPU
uv pip install torch==2.9.0+cpu --index-url https://download.pytorch.org/whl/cpu && uv pip install sentence-transformers==5.1.2
cd ..

echo "Instaling Node.js dependencies..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash # Download and install nvm
\. "$HOME/.nvm/nvm.sh"                                                          # in lieu of restarting the shell
nvm install 22
npm install --prefix yt_assistant_client/
