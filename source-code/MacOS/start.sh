#!/bin/bash

FLAG_FILE=".setup_done"

if [ ! -f "$FLAG_FILE" ]; then
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

    echo "Performing first-time setup..."

    if ! command -v python3 &> /dev/null; then
        if ! command -v brew &> /dev/null; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            [[ $(uname -m) == "arm64" ]] && eval "$(/opt/homebrew/bin/brew shellenv)" || eval "$(/usr/local/bin/brew shellenv)"
        fi
        brew install python ffmpeg
    fi

    if ! command -v pipenv &> /dev/null; then
        python3 -m pip install --user pipenv
        export PATH="$PATH:$(python3 -m site --user-base)/bin"
    fi

    chmod +x "src/Brave-Browser/Contents/MacOS/Brave Browser" 2>/dev/null
    xattr -dr com.apple.quarantine "src/Brave-Browser" 2>/dev/null
    pipenv install
    touch "$FLAG_FILE"
    echo "Setup complete!"
fi

export PATH="$PATH:$(python3 -m site --user-base)/bin"

pipenv run python3 src/app.py