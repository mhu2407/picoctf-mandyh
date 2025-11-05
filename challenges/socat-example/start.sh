#!/bin/bash

set -e

socat tcp-listen:5555,reuseaddr,fork SYSTEM:"go run yolosign.go"