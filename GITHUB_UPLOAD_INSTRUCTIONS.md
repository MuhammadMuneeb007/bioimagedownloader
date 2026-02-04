# GitHub Upload Instructions

Follow these steps to upload your BioImageDownloader repository to GitHub.

## Prerequisites

- GitHub account (username: `muhammadmuneeb007`)
- Git installed on your computer
- Terminal/Command Prompt access

## Step-by-Step Instructions

### Step 1: Create a New Repository on GitHub

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `bioimagedownloader`
   - **Description**: `A Python package to download biology and science icons/images from multiple websites`
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 2: Navigate to Your Github Folder

Open your terminal/command prompt and navigate to the Github folder:

```bash
cd C:\Users\munee\Desktop\Projects\Project20-BioImageDownlaoder\Github
```

### Step 3: Initialize Git Repository

Initialize a new git repository in the Github folder:

```bash
git init
```

### Step 4: Add All Files

Add all files to git staging area:

```bash
git add .
```

### Step 5: Create Initial Commit

Create your first commit:

```bash
git commit -m "Initial commit: BioImageDownloader package"
```

### Step 6: Add Remote Repository

Add your GitHub repository as the remote origin:

```bash
git remote add origin https://github.com/muhammadmuneeb007/bioimagedownloader.git
```

### Step 7: Push to GitHub

Push your code to GitHub:

```bash
git branch -M main
git push -u origin main
```

**Note:** If you're prompted for credentials:
- **Username**: `muhammadmuneeb007`
- **Password**: Use a **Personal Access Token** (not your GitHub password)
  - See "GitHub Authentication" section below for how to create one

---

## Complete Command Sequence

Here's the complete sequence of commands to run:

```bash
# Navigate to Github folder
cd C:\Users\munee\Desktop\Projects\Project20-BioImageDownlaoder\Github

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: BioImageDownloader package"

# Add remote repository
git remote add origin https://github.com/muhammadmuneeb007/bioimagedownloader.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## GitHub Authentication

If you're asked for credentials when pushing, you need a Personal Access Token:

### Create Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **"Generate new token (classic)"**
3. Give it a name: `bioimagedownloader-upload`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

### Use Token:

When prompted for password during `git push`, paste your Personal Access Token (not your GitHub password).

---

## Alternative: Using GitHub Desktop

If you prefer a graphical interface:

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Sign in with your GitHub account
3. Click **"File" → "Add Local Repository"**
4. Browse to: `C:\Users\munee\Desktop\Projects\Project20-BioImageDownlaoder\Github`
5. Click **"Publish repository"**
6. Name: `bioimagedownloader`
7. Click **"Publish Repository"**

---

## Verify Upload

After pushing, verify your repository:

1. Go to: `https://github.com/muhammadmuneeb007/bioimagedownloader`
2. You should see all your files including:
   - README.md
   - setup.py
   - scrapers/ folder
   - All other files

---

## Troubleshooting

### Error: "remote origin already exists"

If you get this error, remove the existing remote first:

```bash
git remote remove origin
git remote add origin https://github.com/muhammadmuneeb007/bioimagedownloader.git
```

### Error: "Authentication failed"

- Make sure you're using a Personal Access Token, not your password
- Check that the token has `repo` scope enabled
- Try creating a new token

### Error: "Repository not found"

- Make sure you created the repository on GitHub first
- Verify the repository name is exactly: `bioimagedownloader`
- Check that you're signed in to the correct GitHub account

### Error: "Failed to push some refs"

If you initialized the GitHub repo with a README, you need to pull first:

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## Future Updates

To update your repository after making changes:

```bash
# Navigate to Github folder
cd C:\Users\munee\Desktop\Projects\Project20-BioImageDownlaoder\Github

# Add changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

---

## Repository URL

Once uploaded, your repository will be available at:

**https://github.com/muhammadmuneeb007/bioimagedownloader**

Users can install your package with:

```bash
pip install git+https://github.com/muhammadmuneeb007/bioimagedownloader.git
```

---

## Next Steps After Upload

1. ✅ Verify all files are uploaded correctly
2. ✅ Check that README.md displays properly on GitHub
3. ✅ Test installation: `pip install git+https://github.com/muhammadmuneeb007/bioimagedownloader.git`
4. ✅ Consider adding topics/tags to your repository
5. ✅ Add a repository description on GitHub
6. ✅ Consider creating releases for version tags

---

**Need Help?** If you encounter any issues, check the troubleshooting section above or refer to [GitHub's documentation](https://docs.github.com/en/get-started).
