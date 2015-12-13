#!/bin/sh
ymltojson () {
        python -c 'import sys,yaml,json; print(json.dumps(yaml.load(sys.stdin)))'
}
