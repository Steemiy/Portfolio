---
title: Tegameno Iyambo Portfolio
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Tegameno Iyambo Portfolio

This repository includes a Docker setup for Hugging Face Spaces. The app is built as a Flet web app and served as static files from `build/web`.

## Local Setup
## Hugging Face Spaces

1. Create a new Space on Hugging Face and choose `Docker` as the SDK.
2. Push this repository to the Space or upload the files through the web UI.
3. The Space will build the Flet web app during the Docker image build and serve it on port `7860`.
4. Your public link will be in this format:

	`https://huggingface.co/spaces/<your-username>/<your-space-name>`

<!-- rebuild-trigger -->

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install -r requirements-dev.txt
```

## Run Locally

```powershell
py main.py
```

## Build For Firebase Hosting

```powershell
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
flet build web . --yes --no-rich-output
```

The first build can take several minutes because Flet downloads the required Flutter SDK. The Firebase config serves the generated static site from `build/web`.

If PowerShell says `flet` is not recognized, use the executable from your Python Scripts folder:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\Scripts\flet.exe" build web . --yes --no-rich-output
```

## Firebase Deploy

Install the Firebase CLI if you do not already have it:

```powershell
npm install -g firebase-tools
firebase login
```

Create a Firebase project in the Firebase console, then either deploy with the project id:

```powershell
firebase deploy --only hosting --project your-firebase-project-id
```

Or copy `.firebaserc.example` to `.firebaserc`, replace `your-firebase-project-id`, and run:

```powershell
firebase deploy --only hosting
```

## GitHub Push

```powershell
git init
git add .
git commit -m "Prepare portfolio for Firebase hosting"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```
