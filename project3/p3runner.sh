#!/bin/sh
counter=0
while [[ $counter -lt $1 ]]; do
    #statements
    python3 "gen-gcp.py" "$2"
    python3 "backtracking.py" "map" "$4" "$5" "$6" #problem type, search method, fw check, ac count limit
    counter=$((counter+1))
done

echo "MAPPING FINISHED"

counter=0
while [[ $counter -lt $1 ]]; do
    #statements
    python3 "sudoku-generator.py" "$3"
    python3 "backtracking.py" "sudo" "$4" "$5" "$6" #problem type, search method, fw check, ac count limit
    counter=$((counter+1))
done
