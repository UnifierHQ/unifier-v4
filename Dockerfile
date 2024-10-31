FROM python:3.12

# Add install data from .install.json
COPY .install.json /app/.install.json

# Add Unifier core
ADD ./src /app/src

# Add requirements and installation files
COPY ./requirements*.txt ./.install.* /app/

# Add configurations and data
ADD ./config /app/config
ADD ./data /app/data

# Install dependencies
RUN python3 /app/src/boot/dep_installer.py

# Set working directory
WORKDIR /app

# Run bootloader
RUN python3 /app/src/boot/bootloader.py
