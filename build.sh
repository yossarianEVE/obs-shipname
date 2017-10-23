#!/bin/bash

venv/bin/pyinstaller --onefile --clean shipname.spec
cp typeids.db dist/
