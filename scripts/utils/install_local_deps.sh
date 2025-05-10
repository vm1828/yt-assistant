# Install local dependencies

echo "Installing Python dependencies..."
cd yt_assistant_api
sudo apt-get update
sudo apt-get install -y libpq-dev build-essential python3-dev
sudo ln -s /usr/bin/python3 /usr/bin/python
poetry install --no-root
cd ..

echo "Instaling Node.js dependencies..."
npm install --prefix yt_assistant_client/
