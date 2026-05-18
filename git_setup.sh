#!/bin/bash
# ============================================================
# Phase 1 — Git Setup Script
# Run this ONCE after cloning or creating the repo
# ============================================================

echo "🔧 Initializing Git repository..."
git init
git add .
git commit -m "init: project scaffold with folder structure"

echo "🌿 Creating team branches..."
git branch frontend
git branch backend
git branch database

echo ""
echo "✅ Git setup complete!"
echo ""
echo "Team workflow:"
echo "  Frontend dev  →  git checkout frontend"
echo "  Backend dev   →  git checkout backend"
echo "  Database dev  →  git checkout database"
echo ""
echo "To merge all into main when done:"
echo "  git checkout main"
echo "  git merge frontend"
echo "  git merge backend"
echo "  git merge database"
