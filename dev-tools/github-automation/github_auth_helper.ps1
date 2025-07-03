# GitHub Authentication Setup with .env file support
function Read-EnvironmentFile {
    param(
        [string]$Path = ".env"
    )
    
    $envVars = @{}
    
    if (Test-Path $Path) {
        Write-Host "📄 Loading environment from: $Path" -ForegroundColor Cyan
        Get-Content $Path | ForEach-Object {
            if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*)$') {
                $key = $Matches[1].Trim()
                $value = $Matches[2].Trim()
                # Remove quotes if present
                $value = $value -replace '^[''"]|[''"]$', ''
                $envVars[$key] = $value
                # Also set as environment variable for this session
                Set-Item -Path "env:$key" -Value $value
            }
        }
        Write-Host "✅ Loaded $($envVars.Count) environment variables" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No .env file found at: $Path" -ForegroundColor Yellow
        Write-Host "💡 Copy .env.example to .env and configure your GitHub token" -ForegroundColor Cyan
    }
    
    return $envVars
}

function Initialize-GitHubAuthentication {
    param(
        [Parameter(Mandatory = $false)]
        [string]$Token,
        [Parameter(Mandatory = $false)]
        [string]$EnvFile = ".env"
    )
    
    # Load environment variables from .env file
    $envVars = Read-EnvironmentFile -Path $EnvFile
    
    # Use token from parameter, environment file, or environment variable
    if (-not $Token) {
        $Token = $envVars['GITHUB_TOKEN']
        if (-not $Token) {
            $Token = $env:GITHUB_TOKEN
        }
    }
    
    if (-not $Token) {
        Write-Host "❌ No GitHub token found!" -ForegroundColor Red
        Write-Host "💡 Set GITHUB_TOKEN in .env file, environment variable, or pass as parameter" -ForegroundColor Yellow
        return $false
    }
    
    try {
        # Import PowerShellForGitHub module
        if (-not (Get-Module -Name PowerShellForGitHub -ListAvailable)) {
            Write-Host "Installing PowerShellForGitHub module..." -ForegroundColor Yellow
            Install-Module -Name PowerShellForGitHub -Scope CurrentUser -Force
        }
        Import-Module PowerShellForGitHub -Force
        
        # Convert token to secure string and create credential object (correct for PowerShellForGitHub v0.17.0)
        $secureToken = ConvertTo-SecureString -String $Token -AsPlainText -Force
        $credential = New-Object System.Management.Automation.PSCredential("username_ignored", $secureToken)
        
        # Set authentication with correct syntax for current version
        Set-GitHubAuthentication -Credential $credential -SessionOnly
        
        # Clear sensitive objects
        $secureToken = $null
        $credential = $null
        
        # Test authentication by getting current user
        $user = Get-GitHubUser
        Write-Host "✅ Successfully authenticated as: $($user.login)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Error "❌ GitHub authentication failed: $_"
        return $false
    }
}

# Rate limiting protection function
function Invoke-GitHubAPIWithRetry {
    param(
        [scriptblock]$APICall,
        [int]$MaxRetries = 3,
        [int]$DelaySeconds = 5
    )
    
    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
        try {
            # Add small delay to respect rate limits
            if ($attempt -gt 1) {
                Write-Verbose "Retry attempt $attempt after rate limit delay"
            }
            Start-Sleep -Milliseconds 200  # Basic rate limiting
            
            $result = & $APICall
            return $result
        }
        catch {
            if ($_.Exception.Message -match "rate limit|403|429") {
                Write-Warning "⚠️ Rate limit hit, waiting $DelaySeconds seconds..."
                Start-Sleep -Seconds $DelaySeconds
                $DelaySeconds *= 2  # Exponential backoff
            }
            elseif ($attempt -eq $MaxRetries) {
                Write-Error "❌ Max retries exceeded: $_"
                throw
            }
            else {
                Write-Verbose "Retrying after error: $_"
                Start-Sleep -Seconds 2
            }
        }
    }
}
