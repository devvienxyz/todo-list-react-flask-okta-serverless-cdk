#!/bin/bash

# Display usage instructions
usage() {
  echo "Usage: $0 <DB_NAME> <DB_USER> <DB_PASS>"
  echo ""
  echo "Environment Variables:"
  echo "  MONGO_HOST         MongoDB host (required)"
  echo "  MONGO_PORT         MongoDB port (required)"
  echo "  MONGO_ADMIN_USER   MongoDB admin username (required)"
  echo "  MONGO_ADMIN_PASS   MongoDB admin password (required)"
  echo ""
  echo "Example:"
  echo "  export MONGO_HOST='localhost'"
  echo "  export MONGO_PORT=27017"
  echo "  export MONGO_ADMIN_USER='root'"
  echo "  export MONGO_ADMIN_PASS='securepass'"
  echo "  $0 mydatabase myuser mypassword"
  exit 0
}

# Check for --help flag
if [[ "$1" == "--help" ]]; then
  usage
fi

# Ensure required environment variables are set
: "${MONGO_HOST:?Error: MONGO_HOST is not set. Use --help for guidance.}"
: "${MONGO_PORT:?Error: MONGO_PORT is not set. Use --help for guidance.}"
: "${MONGO_ADMIN_USER:?Error: MONGO_ADMIN_USER is not set. Use --help for guidance.}"
: "${MONGO_ADMIN_PASS:?Error: MONGO_ADMIN_PASS is not set. Use --help for guidance.}"

# Read from environment variables or command-line arguments
DB_NAME=${1:-$MONGO_DB_NAME}
DB_USER=${2:-$MONGO_DB_USER}
DB_PASS=${3:-$MONGO_DB_PASS}

# Ensure required database credentials are provided
if [[ -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASS" ]]; then
  echo "Error: Missing required parameters."
  echo "Run '$0 --help' for usage instructions."
  exit 1
fi

# Check if the database exists
EXISTING_DB=$(mongosh --host "$MONGO_HOST" --port "$MONGO_PORT" -u "$MONGO_ADMIN_USER" -p "$MONGO_ADMIN_PASS" --authenticationDatabase "admin" --quiet --eval "db.getMongo().getDBNames().indexOf('$DB_NAME') >= 0")

if [[ "$EXISTING_DB" == "true" ]]; then
  echo "Database '$DB_NAME' already exists. Skipping creation."
  exit 0
fi

# Create the database and user
mongosh --host "$MONGO_HOST" --port "$MONGO_PORT" -u "$MONGO_ADMIN_USER" -p "$MONGO_ADMIN_PASS" --authenticationDatabase "admin" <<EOF
use $DB_NAME;
db.createUser({
  user: "$DB_USER",
  pwd: "$DB_PASS",
  roles: [{ role: "readWrite", db: "$DB_NAME" }]
});
EOF

echo "Database '$DB_NAME' created successfully with user '$DB_USER'."
