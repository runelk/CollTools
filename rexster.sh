#!/usr/bin/env sh

DIR="$( cd "$( dirname "$0" )" && pwd )"
$DIR/tools/rexster-server-2.6.0/bin/rexster.sh -s -d -c $DIR/config/rexster.xml
