#!/bin/zsh
# Zip this week's FL Studio projects (+ their audio clips folder) to ~/Music/backups.
set -e
src="$HOME/Music/FL Projects"
dst="$HOME/Music/backups"
mkdir -p "$dst"
stamp=$(date +%Y-%m-%d)
cd "$src"
find . -name "*.flp" -mtime -7 -print0 | xargs -0 zip -q "$dst/flp-$stamp.zip"
echo "wrote $dst/flp-$stamp.zip ($(unzip -l "$dst/flp-$stamp.zip" | tail -1 | awk '{print $2}') files)"
