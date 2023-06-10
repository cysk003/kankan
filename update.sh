#! /usr/bin/env bash

search=${SEARCH_CONTENT-"raw.githubusercontent.com"}
replace=${REPLACE_CONTENT-"cdn.staticaly.com\/gh"}
command -v curl >/dev/null 2 >&1 || { echo >&2 "需要安装CURL命令。";exit 1; }
repo_content=$(curl -s -X GET -H "Content-Type: application/json" ${REPO_URL})
repo_content=$(echo $repo_content | sed -e "s/${search}/${replace}/g")
echo $repo_content >tvbox.json
git config user.email "bellong@vip.qq.com"
git config user.name "fanite"
git add tvbox.json
git commit -m "update ${date}"
git push -f origin main