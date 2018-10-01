#! /bin/sh

while true; do
  gributils index --database="$DATABASE" add-dir --basedir="$BASEDIR" 1>&2
    
  now="$(date +%s)"
  nextScrape="$((($now / (3600*4) + 1) * 3600*4))"
  waitTime="$(($nextScrape - $now))"
  sleep "$waitTime"
done
