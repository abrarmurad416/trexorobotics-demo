# How to Host Trexo Robotics Platform Online

## 🚀 Quick Options (Pick One)

### Option 1: ngrok (Easiest - 5 minutes)
Expose your local API to the internet instantly.

1. **Download ngrok:** https://ngrok.com/download
2. **Start your API locally:**
   ```bash
   python api/data_api.py
   ```
3. **In a new terminal, run:**
   ```bash
   ngrok http 5000
   ```
4. **Copy the ngrok URL** (e.g., `https://abc123.ngrok.io`)
5. **Update dashboard:** Change API URL in `dashboard/index.html` to use the ngrok URL
6. **Host dashboard on GitHub Pages** (see below) or use the ngrok URL directly

**Pros:** Free, instant, no setup  
**Cons:** URL changes each time, requires your computer to be on

---

### Option 2: Render.com (Free Tier - Best for Interview)

#### Deploy API to Render:

1. **Create account:** https://render.com
2. **Create new Web Service**
3. **Connect your GitHub repo** (push code to GitHub first)
4. **Settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python api/data_api.py`
   - **Environment:** Python 3
5. **Deploy!** Get your API URL (e.g., `https://your-api.onrender.com`)

#### Deploy Dashboard:

1. **Create new Static Site** on Render
2. **Connect GitHub repo**
3. **Build Command:** (leave empty)
4. **Publish Directory:** `dashboard`
5. **Update API URL** in `dashboard/index.html` to your Render API URL
6. **Deploy!**

**Pros:** Free, permanent URL, professional  
**Cons:** Takes 10-15 minutes to set up

---

### Option 3: Railway.app (Free Trial)

1. **Sign up:** https://railway.app
2. **New Project → Deploy from GitHub**
3. **Add service for API:**
   - Start command: `python api/data_api.py`
4. **Add service for Dashboard:**
   - Static files from `dashboard/` folder
5. **Get URLs and update dashboard API endpoint**

**Pros:** Easy, modern platform  
**Cons:** Free trial limited

---

### Option 4: GitHub Pages (Dashboard Only)

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Go to repo Settings → Pages**
3. **Source:** Deploy from `dashboard/` folder
4. **Update API URL** in `dashboard/index.html` to your hosted API
5. **Access at:** `https://yourusername.github.io/repo-name/`

**Note:** GitHub Pages only hosts static files. You'll still need to host the API separately (Render, Railway, etc.)

---

## 📝 Step-by-Step: Render.com (Recommended)

### Part 1: Deploy API

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Trexo Robotics Data Platform"
   # Create repo on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/trexo-robotics.git
   git push -u origin main
   ```

2. **On Render.com:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Name: `trexo-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python api/data_api.py`
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your API URL (e.g., `https://trexo-api.onrender.com`)

### Part 2: Update Dashboard for Production

3. **Update dashboard API URL:**
   - Open `dashboard/index.html`
   - Find: `const API_BASE_URL = 'http://localhost:5000/api';`
   - Change to: `const API_BASE_URL = 'https://YOUR-API-URL.onrender.com/api';`

4. **Deploy Dashboard:**
   - On Render: "New +" → "Static Site"
   - Connect same GitHub repo
   - Name: `trexo-dashboard`
   - Build Command: (leave empty)
   - Publish Directory: `dashboard`
   - Click "Create Static Site"
   - Get your dashboard URL

### Part 3: Test

5. **Visit your dashboard URL** - it should work!

---

## 🔧 Quick Fix: Make API Work in Production

Update `api/data_api.py` to work on Render:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

And add at the top:
```python
import os
```

---

## 🎯 For Interview: Simplest Approach

**Use ngrok for instant hosting:**

1. Start API: `python api/data_api.py`
2. Start ngrok: `ngrok http 5000`
3. Copy ngrok URL
4. Update dashboard `index.html` API URL to ngrok URL
5. Upload dashboard to GitHub Pages or just share the ngrok URL

**Total time: 5 minutes**

---

## 📋 Checklist

- [ ] API deployed and accessible
- [ ] Dashboard deployed and accessible  
- [ ] Dashboard API URL updated to production URL
- [ ] Test both work together
- [ ] Have URLs ready for interview

---

## 💡 Pro Tips

1. **For interview:** Have both URLs ready and tested beforehand
2. **Backup plan:** Keep local version running as backup
3. **Test CORS:** Make sure API allows requests from dashboard domain
4. **Update CORS in API** if needed:
   ```python
   CORS(app, resources={r"/api/*": {"origins": ["https://your-dashboard-url.com"]}})
   ```

Good luck! 🚀

