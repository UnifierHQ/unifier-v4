FROM python:3.12

# Add Unifier core
ADD ./src /app/src

# Add requirements and installation files
COPY ./requirements*.txt ./.install.* /app/

# Add configurations and data
ADD ./config /app/config
ADD ./data /app/data

# Set working directory
WORKDIR /app

# Install dependencies
RUN python3 ./src/boot/dep_installer.py

# Run bootloader
RUN python3 ./src/boot/bootloader.py
