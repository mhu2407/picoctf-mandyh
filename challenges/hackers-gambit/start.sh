#!/bin/sh

set -e

socat tcp-listen:3000,reuseaddr,fork SYSTEM:"go run challenge.go"

