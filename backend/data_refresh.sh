#!/usr/bin/env bash
python data_refresh.py
echo "Running"

if [["$(git status --porcelain)" != ""]]; then 
    git config --global user.name $USER_NAME
    git config --global user.email $USER_EMAIL
    git add csv/games_cleaned1.csv
    git commit -m "Updating data"
    git push origin main
    echo "Executed and commited"
else
    echo "Nothing to commit"
fi 