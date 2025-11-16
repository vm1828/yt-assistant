# Install local dependencies

sudo apt-get update && sudo apt-get install -y libpq-dev build-essential python3-dev

echo "Installing Python dependencies for yt_assistant_api..."
cd yt_assistant_api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
# Manually install torch without GPU
pip install torch==2.9.0+cpu --index-url https://download.pytorch.org/whl/cpu && pip install sentence-transformers==5.1.2
cd ..

echo "Installing Python dependencies for yt_assistant_emb..."
cd yt_assistant_emb
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
# Manually install torch without GPU
pip install torch==2.9.0+cpu --index-url https://download.pytorch.org/whl/cpu && pip install sentence-transformers==5.1.2
cd ..

echo "Instaling Node.js dependencies..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash # Download and install nvm
\. "$HOME/.nvm/nvm.sh"                                                          # in lieu of restarting the shell
nvm install 22
npm install --prefix yt_assistant_client/
