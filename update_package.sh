#!/bin/bash

echo -e "\n\033[32mCheck outdated packages.\033[m"
uv tree --outdated

echo -e "\n\033[32mDry run update packages.\033[m"
uv sync -U --dry-run

echo -e "\n"
read -p "Update packages? (y/n) " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n\033[32mStart to update packages.\033[m"
    uv sync -U
    echo -e "\033[32mFinished to update packages.\033[m"

    echo -e "\n\033[32mConfirm the packages after update.\033[m"
    uv tree --outdated
fi

exit 0
