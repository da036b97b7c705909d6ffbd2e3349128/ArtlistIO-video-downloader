#!/bin/bash

if [ -f "readme.txt" ]; then
    cat "readme.txt"
    echo ""
fi

echo "LICENSE AGREEMENT:"
if [ -f "src/LICENSE" ]; then
    cat "src/LICENSE"
else
    echo "Standard Non-commercial use only."
fi
echo ""

read -p "Do you accept these terms? (yes/no): " choice
if [ "$choice" != "yes" ]; then
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    if ! command -v brew &> /dev/null; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        if [[ $(uname -m) == "arm64" ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        else
            eval "$(/usr/local/bin/brew shellenv)"
        fi
    fi
    brew install python
fi

if ! command -v pipenv &> /dev/null; then
    python3 -m pip install --user pipenv
    export PATH="$PATH:$(python3 -m site --user-base)/bin"
fi

chmod -R +x "ffmpeg" 2>/dev/null
chmod -R +x "Brave-Browser" 2>/dev/null

pipenv install
pipenv run python3 src/app.py