#!/bin/sh
counter=0
while [[ $counter -lt $1 ]]; do
    #statements
    python3 "gen-gcp.py" "$2"
    python3 "backtracking.py" "map" "0" "$4" "$5" #problem type, search method, fw check, ac count limit
    python3 "backtracking.py" "map" "1" "$4" "$5"
    python3 "backtracking.py" "map" "2" "$4" "$5"
    counter=$((counter+1))
done

echo "MAPPING FINISHED"

counter=0
while [[ $counter -lt $1 ]]; do
    #statements
    python3 "sudoku-generator.py" "$3"
    python3 "backtracking.py" "sudo" "0" "$4" "$5" #problem type, search method, fw check, ac count limit
    python3 "backtracking.py" "sudo" "1" "$4" "$5"
    python3 "backtracking.py" "sudo" "2" "$4" "$5"
    counter=$((counter+1))
done
