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
    echo "License not accepted. Exiting..."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Python not found. Starting initial setup..."
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

cd src

if ! command -v pipenv &> /dev/null; then
    python3 -m pip install --user pipenv
    PATH="$PATH:$(python3 -m site --user-base)/bin"
fi

pipenv install --deploy --ignore-pipfile

export PYTHONPATH=$PYTHONPATH:$(pwd)
chmod +x "src/Brave-Browser/Contents/MacOS/Brave Browser"
pipenv run python3 app.py