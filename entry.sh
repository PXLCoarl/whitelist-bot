#!/bin/bash

# Update and upgrade packages, install git, clean up
apt-get update && apt-get upgrade -y && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
git clone https://github.com/PXLCoarl/whitelist-bot.git .

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Run the main Python script
python main.py
