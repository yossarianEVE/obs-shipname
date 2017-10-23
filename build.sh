#!/bin/bash

venv/bin/pyinstaller shipname.py
cp typeids.db dist/shipname/
