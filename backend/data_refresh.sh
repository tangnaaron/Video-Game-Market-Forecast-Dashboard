#!/usr/bin/env bash
pip --no-cache-dir --root-user-action=ignore install igdb-api-v4
pip --no-cache-dir --root-user-action=ignore install pandas 

python backend/data_refresh.py
echo "Running"

p=$(pwd)
git config --global --add safe.directory $p

if [[ "$(git status --porcelain)" != "" ]]; then 
    git config --global user.name $USER_NAME
    git config --global user.email $USER_EMAIL
    git add csv/games_cleaned1.csv
    git commit -m "Updating data"
    git push origin main
    echo "Executed and commited"
else
    echo "Nothing to commit"
fi 