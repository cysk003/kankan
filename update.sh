#! /usr/bin/env bash

search=${SEARCH_CONTENT-"raw.githubusercontent.com"}
replace=${REPLACE_CONTENT-"cdn.staticaly.com\/gh"}
echo "REPO_URL：${REPO_URL}"
echo "SEARCH_CONTENT：${search}"
echo "REPLACE_CONTENT: ${replace}"
command -v curl >/dev/null 2 >&1 || { echo >&2 "需要安装CURL命令。";exit 1; }
curl -s -X GET -H "Content-Type: application/json" ${REPO_URL} >tmp.json
if [ $? -ne 0 ]; then
    echo "获取源内容失败。"
    exit 1
fi
sed -i "s/${search}/${replace}/g" tmp.json
cat tmp.json >tvbox.json
rm -rf tmp.json
git config user.email "bellong@vip.qq.com"
git config user.name "fanite"
git add tvbox.json
git commit -m "cron task update on ${date}"
git push -f origin main