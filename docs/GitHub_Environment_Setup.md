# GitHub Environment Setup Guide

This document explains how to configure the production environment for the DexBot CI/CD pipeline.

## Production Environment Configuration

The CI/CD workflow now requires a `production` environment to be configured in GitHub for releases and documentation updates.

### Setting Up the Production Environment

1. **Navigate to Repository Settings**
   - Go to your GitHub repository
   - Click on "Settings" tab
   - Select "Environments" from the left sidebar

2. **Create Production Environment**
   - Click "New environment"
   - Name it `production`
   - Click "Configure environment"

3. **Configure Protection Rules (Recommended)**
   - **Required reviewers**: Add 1-2 reviewers who must approve releases
   - **Wait timer**: Optional - add a delay before deployment
   - **Deployment branches**: Restrict to `main` branch only
   - **Environment secrets**: Add any production-specific secrets if needed

### Protection Rule Examples

#### Basic Setup (Recommended)
- ✅ **Required reviewers**: Add yourself and/or team members
- ✅ **Deployment branches**: Selected branches → `main`
- ⚠️ **Wait timer**: 0 minutes (or add delay if desired)

#### Advanced Setup (High Security)
- ✅ **Required reviewers**: 2+ reviewers
- ✅ **Wait timer**: 5-10 minutes  
- ✅ **Deployment branches**: Selected branches → `main`
- ✅ **Environment secrets**: Production API keys, tokens, etc.

## Workflow Behavior

### Without Production Environment
If the production environment doesn't exist, the release and docs jobs will fail with an environment error.

### With Production Environment
- **Development**: CI/CD runs normally on feature branches (no environment needed)
- **Production**: Release and docs jobs wait for approval/protection rules on main branch

### Manual Approval Process
1. Push to main branch triggers workflow
2. Lint/test/build jobs run automatically
3. Release and docs jobs wait for production environment approval
4. Designated reviewers approve the deployment
5. Release is created and docs are updated

## Benefits

- **🛡️ Protection**: Prevents accidental releases
- **👥 Review**: Ensures releases are reviewed by team members
- **🔐 Security**: Environment-specific secrets and permissions
- **📋 Audit**: Complete audit trail of who approved what releases
- **🚀 Flexibility**: Can still iterate quickly on development branches

## Quick Setup Commands

If you prefer to use GitHub CLI:

```bash
# Install GitHub CLI if needed
# https://cli.github.com/

# Create production environment (basic)
gh api repos/:owner/:repo/environments/production -X PUT

# Note: Protection rules must be configured through the web interface
```

## Testing the Setup

1. Push a change to the main branch
2. Check the Actions tab - you should see:
   - ✅ Lint/test/build jobs complete automatically
   - ⏳ Release and docs jobs waiting for environment approval
3. Go to the workflow run and approve the production deployment
4. ✅ Release and docs jobs complete after approval

---

*This environment setup provides production-grade security while maintaining development velocity.*
