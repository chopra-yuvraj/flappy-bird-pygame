# Flappy Bird Game
[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Pygame](https://img.shields.io/badge/Game-Pygame-00D4AA?style=for-the-badge&logo=python&logoColor=white)](https://pygame.org/)

A premium web-hosted version of Flappy Bird, powered by Pygame, Pygbag, and Flask.

## 🚀 Deployment Guide (Run EVERYTHING on Render)

You do **NOT** need to run anything locally. We will configure Render to build the game for us.

### Step 1: Push to GitHub
1.  Ensure you have this repository pushed to your GitHub account.

### Step 2: Create Web Service on Render
1.  Go to [Render.com Dashboard](https://dashboard.render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect this repository.

### Step 3: Configure Settings (Critical!)
Fill these in EXACTLY.

| Setting | Value |
| :--- | :--- |
| **Name** | `flappy-bird-web` (or anything you like) |
| **Runtime** | **Python 3** |
| **Build Command** | `pip install -r requirements.txt && python -m pygbag --build game/main.py && mkdir -p website/static/game && cp -r game/build/web/* website/static/game/` |
| **Start Command** | `gunicorn website.app:app` |

*> **Troubleshooting**: If deployment fails, try clearing the build cache on Render (Manual Deploy -> Clear Build Cache & Deploy).*

---

## Why Flappy Bird Game?
As a B.Tech CSE student at VIT and B.S Data Science student at IIT Madras, 
I wanted to understand game development fundamentals and physics simulation.

### Key Features
- **Red "Angry Bird" Design** - Custom programmatic art.
- **Physics Engine** - Realistic heavy gravity and jump mechanics.
- **Collision Detection** - Precise pipe and ground collision system.
- **Score Tracking** - Points for each pipe successfully passed.
- **Auto-Restart** - Quick restart functionality.

---

## About the Developer
**Yuvraj Chopra**  
B.Tech Computer Science Engineering - VIT Vellore  
B.S. Data Science - IIT Madras  

[ **View on GitHub**](https://github.com/chopra-yuvraj/flappy-bird-pygame)
