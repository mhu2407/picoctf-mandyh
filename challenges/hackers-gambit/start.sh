#!/bin/sh
set -e

PORT=3000

exec socat TCP-LISTEN:${PORT},reuseaddr,fork EXEC:/app/server,pty,stderr
