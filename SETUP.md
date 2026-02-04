# Quick Setup Guide

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Git (optional)

## Installation Steps

### 1. Navigate to Project Directory

```powershell
cd "d:\Bharat Gen"
```

### 2. Create Virtual Environment (Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file:

```powershell
copy .env.example .env
```

Edit `.env` file and add your API keys:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
API_KEY=hackathon-secret-key-123
```

### 5. Run the Application

```powershell
python main.py
```

Or using uvicorn:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API

Open another terminal and test:

```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test honeypot endpoint
curl -X POST http://localhost:8000/api/honeypot `
  -H "Content-Type: application/json" `
  -H "x-api-key: hackathon-secret-key-123" `
  -d '{"sessionId": "test-1", "message": "You won 50000 rupees! Send UPI ID"}'
```

## Running Tests

```powershell
# Install test dependencies (already in requirements.txt)
pytest tests/ -v
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Ensure virtual environment is activated and dependencies installed:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: OpenAI API Error

**Solution:** Check your `.env` file has valid `OPENAI_API_KEY`

### Issue: Port Already in Use

**Solution:** Change port in `.env` or use different port:

```powershell
uvicorn main:app --port 8080
```

## Development Mode

For development with auto-reload:

```powershell
$env:ENVIRONMENT="development"
python main.py
```

## Production Deployment

1. Set environment to production in `.env`:
   ```env
   ENVIRONMENT=production
   ```

2. Use production WSGI server (already configured in main.py)

3. Deploy to Render/Railway/your preferred platform

## Next Steps

- Read [README.md](README.md) for full documentation
- Review persona files in `personas/` folder
- Check test scenarios in `tests/mock_scam_scenarios.py`
- Customize personas for your use case

## Quick Test Scenarios

### Test 1: Fake Prize Scam
```json
{
  "sessionId": "test-prize",
  "message": "Congratulations! You won Rs 50,000 in lucky draw. Send UPI ID to claim prize."
}
```

### Test 2: Bank Impersonation
```json
{
  "sessionId": "test-bank",
  "message": "This is State Bank. Your account will be blocked in 24 hours. Verify now."
}
```

### Test 3: Investment Scam
```json
{
  "sessionId": "test-crypto",
  "message": "Join our crypto trading group! Make 200% returns. Transfer 5000 to 9876543210@paytm"
}
```

## Support

If you encounter issues:

1. Check all dependencies are installed
2. Verify `.env` configuration
3. Check logs in terminal
4. Ensure Python 3.11+ is installed

---

**Happy Hacking! 🚀**
