#!/bin/bash
watchmedo auto-restart --patterns="*.py" --recursive -- python main.py
