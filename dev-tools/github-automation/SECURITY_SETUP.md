# GitHub API Security Configuration

## Quick Setup

1. **Copy the template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your actual values:
   ```bash
   GITHUB_TOKEN=ghp_your_actual_token_here
   GITHUB_OWNER=your_username
   GITHUB_REPO=DexBot
   ```

3. **Verify `.env` is in `.gitignore`** (already configured ✅)

## GitHub Token Setup

### Creating a Personal Access Token

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Set expiration and select scopes:
   - `repo` - Full repository access
   - `issues` - Issue management
   - `admin:repo_hook` - Webhook management (if needed)
4. Copy the token immediately (you won't see it again!)

### Token Security Best Practices

- ✅ **DO**: Store in `.env` file (not committed)
- ✅ **DO**: Use environment variables in CI/CD
- ✅ **DO**: Set appropriate expiration dates
- ✅ **DO**: Use minimal required scopes
- ❌ **DON'T**: Commit tokens to version control
- ❌ **DON'T**: Share tokens in chat/email
- ❌ **DON'T**: Use tokens with excessive permissions

## Usage Examples

### PowerShell (Recommended)
```powershell
# Loads token from .env file automatically
.\dev-tools\github-automation\github_auth_helper.ps1
Initialize-GitHubAuthentication
```

### Manual Token
```powershell
# For one-time use or testing
Initialize-GitHubAuthentication -Token "ghp_your_token_here"
```

### Environment Variable
```bash
# Set environment variable (Linux/macOS)
export GITHUB_TOKEN="ghp_your_token_here"

# Set environment variable (Windows CMD)
set GITHUB_TOKEN=ghp_your_token_here

# Set environment variable (Windows PowerShell)
$env:GITHUB_TOKEN = "ghp_your_token_here"
```

## Troubleshooting

### Common Issues

1. **"No GitHub token found!"**
   - Check `.env` file exists and has correct format
   - Verify token is not empty or quoted incorrectly
   - Ensure `.env` file is in project root directory

2. **"Authentication failed"**
   - Verify token is valid and not expired
   - Check token has required scopes (repo, issues)
   - Test token at https://api.github.com/user with your token

3. **"PowerShellForGitHub module not found"**
   - Run script as administrator or use `-Scope CurrentUser`
   - Install manually: `Install-Module PowerShellForGitHub -Force`

### Security Check

Run this to verify your setup:
```powershell
# Check if .env is properly ignored
git check-ignore .env  # Should return ".env"

# Check if .env.example is tracked
git ls-files .env.example  # Should return ".env.example"
```

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GITHUB_TOKEN` | Yes | Personal Access Token | `ghp_1234567890abcdef...` |
| `GITHUB_OWNER` | Yes | Repository owner/org | `your_username` |
| `GITHUB_REPO` | Yes | Repository name | `DexBot` |
| `GITHUB_API_URL` | No | Custom API URL | `https://api.github.com` |
| `DEV_MODE` | No | Enable dev features | `true` |
| `VERBOSE_LOGGING` | No | Extra logging | `false` |

---

**⚠️ Security Reminder**: Never commit your `.env` file or share your GitHub token. Keep tokens secure and rotate them regularly.
