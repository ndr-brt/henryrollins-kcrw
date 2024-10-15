#!/bin/bash
FROM=$1
TO=$2

for ((i=$FROM; i<=$TO; i++)); do
    echo "Episode $i"
    URL=$(curl https://www.kcrw.com/music/shows/henry-rollins/kcrw-broadcast-$i/player.json | jq '.media[0].url' --raw-output)
    echo "from URL: $URL"
    curl ${URL} --output rollins-$1.mp3
done
