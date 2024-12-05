#!/bin/sh
## substitutes for URIs in $1 with the prefixes in prefixes.ttl
riot --syntax=ttl --formatted=ttl prefixes.ttl $1 