#!/bin/bash
source env_build/bin/activate
cd spring-launcher/spring_launcher
pyinstaller --windowed launcher.spec -y
