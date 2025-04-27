# Source environment variables

env_files=(
    "env/.client.env"
    "env/.db.env"
    "env/.api.env"
)

for env_file in "${env_files[@]}"; do
    echo "Sourcing $env_file"
    set -o allexport
    source "$env_file"
    set +o allexport
done
