# Full Automation Suite Quick-Start Guide

This quick-start guide provides the essential steps to get the GitHub Issues Workflow Automation Suite up and running in your repository in under 10 minutes.

## Prerequisites

- GitHub repository with admin access
- PowerShell 7.0+ installed
- GitHub Personal Access Token with repo scope

## 5-Minute Setup

### Step 1: Clone and Configure

```powershell
# Clone the repository
git clone https://github.com/DexBot/DexBot.git
cd DexBot

# Install required module
Install-Module -Name PowerShellForGitHub -Scope CurrentUser -Force

# Set up GitHub authentication
$token = "<YOUR-GITHUB-TOKEN>"
Set-GitHubAuthentication -Token $token

# Run the quick setup wizard
.\scripts\full_automation_suite.ps1 -Action quicksetup -Repository "owner/repo"
```

### Step 2: Configure GitHub Repository

1. Go to your repository settings on GitHub
2. Navigate to "Webhooks" and click "Add webhook"
3. Use the values from the setup wizard output:
   - Payload URL: (from wizard output)
   - Content type: application/json
   - Secret: (from wizard output)
   - Events: Issues, Issue comments
4. Click "Add webhook"

### Step 3: Add GitHub Actions Workflow

1. Create `.github/workflows/` directory in your repository if it doesn't exist
2. Copy the generated workflow file:
   ```powershell
   Copy-Item -Path ".\output\issue-automation.yml" -Destination ".github\workflows\"
   ```
3. Commit and push to your repository:
   ```powershell
   git add .github/workflows/issue-automation.yml
   git commit -m "Add issue automation workflow"
   git push
   ```

## That's it! Your repository now has:

- ✅ Intelligent issue routing
- ✅ Automated priority assignment
- ✅ Predictive analytics
- ✅ Self-optimizing workflow

## Verification

Test your setup by creating a new issue in your repository. The automation should:

1. Analyze the issue content
2. Assign appropriate component and priority labels
3. Route to the correct team members (if configured)

## Next Steps

- Customize component categories in `config/automation_config.json`
- Set up scheduled reporting
- Integrate with additional external systems
- Configure self-optimization settings

For detailed configuration and usage, see the [Full Documentation](FULL_AUTOMATION_SUITE_USAGE_GUIDE.md).

## Common Customizations

### Custom Component Categories

Edit your `config/automation_config.json` file:

```json
{
  "intelligent_routing": {
    "component_categories": [
      "frontend",
      "backend",
      "database",
      "documentation",
      "devops"
    ]
  }
}
```

### Adjust Confidence Threshold

```json
{
  "intelligent_routing": {
    "confidence_threshold": 0.65
  }
}
```

### Enable Auto-Assignment

```json
{
  "intelligent_routing": {
    "auto_assign": true,
    "team_members": {
      "frontend": ["user1", "user2"],
      "backend": ["user3", "user4"],
      "database": ["user5"]
    }
  }
}
```

## Troubleshooting

**Issue**: Webhook is not triggering automation
**Solution**: Check webhook delivery logs in GitHub repository settings

**Issue**: Authentication errors
**Solution**: Verify token has not expired and has correct permissions

**Issue**: Incorrect routing results
**Solution**: Adjust confidence threshold or customize component keywords

## Support

For additional help:
- Check the [Full Documentation](FULL_AUTOMATION_SUITE_USAGE_GUIDE.md)
- See [Example Scenarios](FULL_AUTOMATION_SUITE_EXAMPLES.md)
- Create an issue in the DexBot repository
