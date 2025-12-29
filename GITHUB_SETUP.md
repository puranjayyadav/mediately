# GitHub Setup Guide for Streamlit Cloud Deployment

Your repository is now initialized and ready to be pushed to GitHub! Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name:** `mediately-dashboard` (or your preferred name)
   - **Description:** "FY2024 Campaign Analytics Dashboard - Streamlit App"
   - **Visibility:** Choose Public (required for free Streamlit Cloud) or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your terminal:

```bash
cd C:\Users\PURANJAY\Mediately
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**Replace:**
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with the repository name you created

## Step 3: Push Your Code

If you haven't already, run:
```bash
git push -u origin main
```

You may be prompted to authenticate. Use your GitHub username and a Personal Access Token (not your password).

## Step 4: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in the deployment details:
   - **Repository:** Select your newly created repository
   - **Branch:** `main` (or `master` if that's your default branch)
   - **Main file path:** `dashboard.py`
   - **App URL:** (optional) Choose a custom subdomain
5. Click **"Deploy"**

## Step 5: Wait for Deployment

Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Run your dashboard
- Provide you with a public URL (e.g., `https://your-app.streamlit.app`)

## Troubleshooting

### Authentication Issues
If you get authentication errors when pushing:
1. Generate a Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` permissions
   - Use this token as your password when pushing

### Branch Name Issues
If your default branch is `master` instead of `main`:
```bash
git branch -M main
```
Or use `master` in Streamlit Cloud settings.

### Files Not Showing
Make sure all files are committed:
```bash
git status
git add .
git commit -m "Add all files"
git push
```

## Next Steps

Once deployed:
- Your dashboard will be accessible via a public URL
- Updates: Just push changes to GitHub and Streamlit Cloud will auto-deploy
- Monitor logs in the Streamlit Cloud dashboard if issues occur

---

**Need help?** Check the [Streamlit Cloud documentation](https://docs.streamlit.io/streamlit-community-cloud)

