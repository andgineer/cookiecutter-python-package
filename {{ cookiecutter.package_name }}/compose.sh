#! /usr/bin/env bash
# run docker compose with an arguments
#
# Examples:
# compose.sh logs tests
docker compose \
  "$@"
