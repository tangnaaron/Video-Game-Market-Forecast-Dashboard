#!/usr/bin/env bash
pip --no-cache-dir install --root-user-action=ignore igdb-api-v4
pip --no-cache-dir install --root-user-action=ignore pandas 

echo $CLIENT_SECRET
python backend/data_refresh.py
echo "Running"

p=$(pwd)
git config --global --add safe.directory $p

if [[ "$(git status --porcelain)" != "" ]]; then 
    git config --global user.name $USER_NAME
    git config --global user.email $USER_EMAIL
    git add .
    git commit -m "Updating data"
    git push origin main
    echo "Executed and commited"
else
    echo "Nothing to commit"
fi 
