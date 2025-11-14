# Environment Variables

## Currently Used

The project uses **one environment variable**:

### `PORT` (Optional)
- **Used in:** `api/data_api.py`
- **Default:** `5000`
- **Purpose:** Sets the port for the Flask API server
- **Usage:** `port = int(os.environ.get('PORT', 5000))`
- **When needed:** Automatically set by hosting platforms (Render, Heroku, Railway)
- **Local development:** Not required (defaults to 5000)

## Not Currently Used (But Available)

The project has `python-dotenv` in requirements.txt, but it's not actively used. The API keys are currently hardcoded in `api/data_api.py`.

## For Production Deployment

### Render.com / Heroku / Railway
These platforms automatically set the `PORT` environment variable. No action needed.

### Manual Setup
If you want to use environment variables locally:

1. **Install python-dotenv** (already in requirements.txt)
2. **Create `.env` file:**
   ```
   PORT=5000
   ```
3. **Load in code** (would need to add to `api/data_api.py`):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Summary

**Current status:** 
- ✅ `PORT` env var is used (for hosting platforms)
- ❌ No `.env` file needed for local development
- ❌ API keys are hardcoded (fine for demo, but could be moved to env vars for production)

**For your interview:** You can mention that the project is set up to use environment variables (PORT) and could easily be extended to use env vars for API keys and database connections in production.

