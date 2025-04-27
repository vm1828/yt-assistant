# Install local dependencies

echo "Installing Python dependencies..."
cd yt_assistant_api
poetry install --no-root
cd ..

echo "Instaling Node.js dependencies..."
npm install --prefix yt_assistant_client/
