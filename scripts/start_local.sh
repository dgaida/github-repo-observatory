#!/bin/bash
# Start the application locally
export GITHUB_TOKEN=your_token_here
uvicorn app.main:app --reload
