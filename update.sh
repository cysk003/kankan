#! /usr/bin/env bash

search=${SEARCH_CONTENT-"raw.githubusercontent.com"}
replace=${REPLACE_CONTENT-"cdn.staticaly.com\/gh"}
echo "REPO_URL：${REPO_URL}"
echo "SEARCH_CONTENT：${search}"
echo "REPLACE_CONTENT: ${replace}"
command -v curl >/dev/null 2 >&1 || { echo >&2 "需要安装CURL命令。";exit 1; }
repo_content=$(curl -s -X GET -H "Content-Type: application/json" ${REPO_URL})
if [ $? -ne 0 ]; then
    echo "获取源内容失败。"
    exit 1
fi
repo_content=$(echo $repo_content | sed -e "s/${search}/${replace}/g")
echo $repo_content >tvbox.json
git config user.email "bellong@vip.qq.com"
git config user.name "fanite"
git add tvbox.json
git commit -m "update ${date}"
git push -f origin main