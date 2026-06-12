#!/bin/bash
set -e

TARGET_DIR="/home/app/frontend"
cd "$TARGET_DIR"

echo "📥 Installing dependencies..."
npm install

echo "✅ Setup complete"

echo "🚀 Starting the app..."
npm run dev