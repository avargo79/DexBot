# Intelligent Issue Routing System
# PowerShell script for content-based component suggestion using NLP techniques
# Phase 3 of DexBot GitHub Issues Workflow Implementation

[CmdletBinding()]
param(
    [Parameter(HelpMessage="Issue title or description text for analysis")]
    [string]$IssueText = "",
    
    [Parameter(HelpMessage="Path to issue file or JSON data")]
    [string]$IssueFile = "",
    
    [Parameter(HelpMessage="GitHub issue number to analyze")]
    [int]$IssueNumber = 0,
    
    [Parameter(HelpMessage="Action to perform: analyze, suggest, route, batch")]
    [ValidateSet("analyze", "suggest", "route", "batch", "train", "help")]
    [string]$Action = "analyze",
    
    [Parameter(HelpMessage="Output format: text, json, csv, detailed")]
    [ValidateSet("text", "json", "csv", "detailed")]
    [string]$Format = "text",
    
    [Parameter(HelpMessage="Confidence threshold for suggestions (0.0-1.0)")]
    [double]$Threshold = 0.7,
    
    [Parameter(HelpMessage="Show verbose analysis details")]
    [switch]$ShowVerbose,
    
    [Parameter(HelpMessage="Dry run mode - show suggestions without applying")]
    [switch]$DryRun,
    
    [Parameter(HelpMessage="Log analysis results to file")]
    [switch]$LogResults
)

# ============================================================================
# INTELLIGENT ROUTING CONFIGURATION
# ============================================================================

$Config = @{
    # Component classification keywords and patterns
    ComponentKeywords = @{
        "auto-heal" = @(
            "heal", "healing", "bandage", "potion", "health", "hp", "life",
            "cure", "curing", "poison", "antidote", "recovery", "restoration"
        )
        "combat" = @(
            "fight", "combat", "attack", "weapon", "damage", "target", "enemy",
            "battle", "war", "pvp", "pvm", "spell", "magic", "casting"
        )
        "looting" = @(
            "loot", "items", "corpse", "inventory", "pick up", "collect",
            "treasure", "gold", "resources", "materials", "gather"
        )
        "ui" = @(
            "interface", "gui", "gump", "window", "display", "screen",
            "button", "menu", "dialog", "form", "visual", "appearance"
        )
        "core" = @(
            "system", "core", "engine", "framework", "architecture", "base",
            "fundamental", "infrastructure", "foundation", "main"
        )
        "config" = @(
            "configuration", "config", "settings", "options", "preferences",
            "parameters", "setup", "customization", "profile"
        )
        "utils" = @(
            "utility", "helper", "tool", "function", "method", "common",
            "shared", "general", "miscellaneous", "support"
        )
    }
    
    # Priority classification patterns
    PriorityPatterns = @{
        "critical" = @(
            "crash", "error", "broken", "failure", "urgent", "critical",
            "blocker", "showstopper", "severe", "major issue"
        )
        "high" = @(
            "important", "significant", "priority", "needed", "required",
            "enhancement", "improvement", "feature request"
        )
        "medium" = @(
            "nice to have", "enhancement", "improvement", "optimization",
            "performance", "efficiency", "better"
        )
        "low" = @(
            "minor", "cosmetic", "polish", "cleanup", "documentation",
            "comment", "style", "formatting"
        )
    }
    
    # Assignment skill patterns (from Phase 2 analysis)
    SkillPatterns = @{
        "razor-enhanced" = @(
            "razor", "enhanced", "api", "uo", "ultima", "online",
            "scripting", "integration", "client"
        )
        "python-core" = @(
            "python", "class", "method", "function", "object", "import",
            "module", "package", "library"
        )
        "system-design" = @(
            "architecture", "design", "pattern", "structure", "framework",
            "modular", "system", "component"
        )
        "ui-development" = @(
            "gump", "interface", "user", "experience", "interaction",
            "visual", "display", "gui"
        )
        "data-analysis" = @(
            "analysis", "data", "statistics", "metrics", "performance",
            "optimization", "efficiency", "algorithm"
        )
    }
    
    # Confidence scoring weights
    ScoringWeights = @{
        ExactMatch = 1.0
        PartialMatch = 0.7
        StemMatch = 0.5
        ContextMatch = 0.3
        TitleBonus = 0.2
        LengthPenalty = 0.1
    }
}

# ============================================================================
# NATURAL LANGUAGE PROCESSING FUNCTIONS
# ============================================================================

function Get-TextTokens {
    <#
    .SYNOPSIS
    Tokenize text into searchable components with stemming
    
    .DESCRIPTION
    Breaks down issue text into individual tokens, removes stop words,
    and applies basic stemming for better keyword matching.
    
    .PARAMETER Text
    Input text to tokenize
    
    .RETURNS
    Array of processed tokens
    #>
    param([string]$Text)
    
    if ([string]::IsNullOrWhiteSpace($Text)) {
        return @()
    }
    
    # Convert to lowercase and split on word boundaries
    $tokens = $Text.ToLower() -split '\W+' | Where-Object { $_.Length -gt 2 }
    
    # Remove common stop words
    $stopWords = @(
        "the", "and", "but", "for", "are", "with", "his", "they", "this",
        "have", "from", "not", "had", "her", "him", "has", "she", "more",
        "will", "when", "can", "all", "one", "there", "what", "said", "each"
    )
    
    $filteredTokens = $tokens | Where-Object { $_ -notin $stopWords }
    
    # Basic stemming (remove common suffixes)
    $stemmedTokens = $filteredTokens | ForEach-Object {
        $token = $_
        
        # Remove common suffixes
        if ($token.EndsWith("ing")) { $token = $token.Substring(0, $token.Length - 3) }
        elseif ($token.EndsWith("ed")) { $token = $token.Substring(0, $token.Length - 2) }
        elseif ($token.EndsWith("er")) { $token = $token.Substring(0, $token.Length - 2) }
        elseif ($token.EndsWith("ly")) { $token = $token.Substring(0, $token.Length - 2) }
        elseif ($token.EndsWith("ion")) { $token = $token.Substring(0, $token.Length - 3) }
        
        return $token
    }
    
    return $stemmedTokens | Sort-Object -Unique
}

function Measure-KeywordRelevance {
    <#
    .SYNOPSIS
    Calculate relevance score between text and keyword set
    
    .DESCRIPTION
    Uses multiple matching strategies to determine how well a set of keywords
    matches the given text, with weighted scoring for different match types.
    
    .PARAMETER Tokens
    Tokenized text array
    
    .PARAMETER Keywords
    Array of keywords to match against
    
    .PARAMETER IsTitle
    Whether the text is from a title (gets scoring bonus)
    
    .RETURNS
    Relevance score between 0.0 and 1.0
    #>
    param(
        [string[]]$Tokens,
        [string[]]$Keywords,
        [bool]$IsTitle = $false
    )
    
    if ($Tokens.Count -eq 0 -or $Keywords.Count -eq 0) {
        return 0.0
    }
    
    $totalScore = 0.0
    $maxPossibleScore = $Keywords.Count * $Config.ScoringWeights.ExactMatch
    
    foreach ($keyword in $Keywords) {
        $keywordLower = $keyword.ToLower()
        $bestScore = 0.0
        
        foreach ($token in $Tokens) {
            $score = 0.0
            
            # Exact match
            if ($token -eq $keywordLower) {
                $score = $Config.ScoringWeights.ExactMatch
            }
            # Partial match (keyword contains token or vice versa)
            elseif ($keywordLower.Contains($token) -or $token.Contains($keywordLower)) {
                $score = $Config.ScoringWeights.PartialMatch
            }
            # Stem match (basic similarity)
            elseif (Get-StemSimilarity -Word1 $token -Word2 $keywordLower) {
                $score = $Config.ScoringWeights.StemMatch
            }
            
            $bestScore = [Math]::Max($bestScore, $score)
        }
        
        $totalScore += $bestScore
    }
    
    # Apply title bonus
    if ($IsTitle -and $totalScore -gt 0) {
        $totalScore += $Config.ScoringWeights.TitleBonus
    }
    
    # Normalize score
    $normalizedScore = $totalScore / $maxPossibleScore
    
    # Apply length penalty for very short text
    if ($Tokens.Count -lt 5) {
        $normalizedScore *= (1.0 - $Config.ScoringWeights.LengthPenalty)
    }
    
    return [Math]::Min(1.0, $normalizedScore)
}

function Get-StemSimilarity {
    <#
    .SYNOPSIS
    Check if two words have similar stems
    
    .DESCRIPTION
    Basic similarity check for word stems using character overlap
    
    .PARAMETER Word1
    First word to compare
    
    .PARAMETER Word2
    Second word to compare
    
    .RETURNS
    Boolean indicating similarity
    #>
    param([string]$Word1, [string]$Word2)
    
    if ($Word1.Length -lt 3 -or $Word2.Length -lt 3) {
        return $false
    }
    
    # Check if words share a common prefix of at least 3 characters
    $minLength = [Math]::Min($Word1.Length, $Word2.Length)
    $commonPrefix = 0
    
    for ($i = 0; $i -lt $minLength; $i++) {
        if ($Word1[$i] -eq $Word2[$i]) {
            $commonPrefix++
        } else {
            break
        }
    }
    
    return $commonPrefix -ge 3
}

# ============================================================================
# ISSUE ANALYSIS FUNCTIONS
# ============================================================================

function Get-IssueAnalysis {
    <#
    .SYNOPSIS
    Perform comprehensive NLP analysis of issue content
    
    .DESCRIPTION
    Analyzes issue title and description to extract component suggestions,
    priority recommendations, and skill requirements using NLP techniques.
    
    .PARAMETER Title
    Issue title text
    
    .PARAMETER Description
    Issue description/body text
    
    .RETURNS
    Analysis object with suggestions and confidence scores
    #>
    param(
        [string]$Title = "",
        [string]$Description = ""
    )
    
    Write-Verbose "Analyzing issue content..."
    
    # Tokenize text
    $titleTokens = Get-TextTokens -Text $Title
    $descTokens = Get-TextTokens -Text $Description
    $allTokens = ($titleTokens + $descTokens) | Sort-Object -Unique
    
    Write-Verbose "Extracted $($titleTokens.Count) title tokens, $($descTokens.Count) description tokens"
    
    # Analyze components
    $componentScores = @{}
    foreach ($component in $Config.ComponentKeywords.Keys) {
        $keywords = $Config.ComponentKeywords[$component]
        
        $titleScore = Measure-KeywordRelevance -Tokens $titleTokens -Keywords $keywords -IsTitle $true
        $descScore = Measure-KeywordRelevance -Tokens $descTokens -Keywords $keywords
        
        # Weighted combination (title is more important)
        $combinedScore = ($titleScore * 0.7) + ($descScore * 0.3)
        $componentScores[$component] = $combinedScore
        
        Write-Verbose "Component '$component': Title=$($titleScore.ToString('F3')), Desc=$($descScore.ToString('F3')), Combined=$($combinedScore.ToString('F3'))"
    }
    
    # Analyze priority
    $priorityScores = @{}
    foreach ($priority in $Config.PriorityPatterns.Keys) {
        $keywords = $Config.PriorityPatterns[$priority]
        
        $titleScore = Measure-KeywordRelevance -Tokens $titleTokens -Keywords $keywords -IsTitle $true
        $descScore = Measure-KeywordRelevance -Tokens $descTokens -Keywords $keywords
        
        $combinedScore = ($titleScore * 0.8) + ($descScore * 0.2)
        $priorityScores[$priority] = $combinedScore
    }
    
    # Analyze skill requirements
    $skillScores = @{}
    foreach ($skill in $Config.SkillPatterns.Keys) {
        $keywords = $Config.SkillPatterns[$skill]
        
        $titleScore = Measure-KeywordRelevance -Tokens $titleTokens -Keywords $keywords -IsTitle $true
        $descScore = Measure-KeywordRelevance -Tokens $descTokens -Keywords $keywords
        
        $combinedScore = ($titleScore * 0.6) + ($descScore * 0.4)
        $skillScores[$skill] = $combinedScore
    }
    
    # Generate suggestions based on threshold
    $componentSuggestions = $componentScores.GetEnumerator() | 
        Where-Object { $_.Value -ge $Threshold } | 
        Sort-Object Value -Descending |
        Select-Object @{Name='Component'; Expression={$_.Key}}, @{Name='Confidence'; Expression={$_.Value}}
    
    $prioritySuggestion = $priorityScores.GetEnumerator() | 
        Sort-Object Value -Descending | 
        Select-Object -First 1 |
        Select-Object @{Name='Priority'; Expression={$_.Key}}, @{Name='Confidence'; Expression={$_.Value}}
    
    $skillSuggestions = $skillScores.GetEnumerator() | 
        Where-Object { $_.Value -ge ($Threshold * 0.8) } | 
        Sort-Object Value -Descending |
        Select-Object @{Name='Skill'; Expression={$_.Key}}, @{Name='Confidence'; Expression={$_.Value}}
    
    return @{
        Tokens = @{
            Title = $titleTokens
            Description = $descTokens
            All = $allTokens
        }
        Scores = @{
            Components = $componentScores
            Priority = $priorityScores
            Skills = $skillScores
        }
        Suggestions = @{
            Components = $componentSuggestions
            Priority = $prioritySuggestion
            Skills = $skillSuggestions
        }
        Metadata = @{
            Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            Threshold = $Threshold
            TitleLength = $Title.Length
            DescriptionLength = $Description.Length
            TokenCount = $allTokens.Count
        }
    }
}

function Format-AnalysisOutput {
    <#
    .SYNOPSIS
    Format analysis results in specified output format
    
    .DESCRIPTION
    Converts analysis results to text, JSON, CSV, or detailed format
    based on the specified format parameter.
    
    .PARAMETER Analysis
    Analysis results object
    
    .PARAMETER Format
    Output format (text, json, csv, detailed)
    
    .RETURNS
    Formatted output string
    #>
    param(
        [object]$Analysis,
        [string]$Format = "text"
    )
    
    switch ($Format.ToLower()) {
        "json" {
            return $Analysis | ConvertTo-Json -Depth 10 -Compress
        }
        
        "csv" {
            $csvData = @()
            
            # Component suggestions
            foreach ($comp in $Analysis.Suggestions.Components) {
                $csvData += [PSCustomObject]@{
                    Type = "Component"
                    Suggestion = $comp.Component
                    Confidence = $comp.Confidence.ToString("F3")
                }
            }
            
            # Priority suggestion
            if ($Analysis.Suggestions.Priority) {
                $csvData += [PSCustomObject]@{
                    Type = "Priority"
                    Suggestion = $Analysis.Suggestions.Priority.Priority
                    Confidence = $Analysis.Suggestions.Priority.Confidence.ToString("F3")
                }
            }
            
            # Skill suggestions
            foreach ($skill in $Analysis.Suggestions.Skills) {
                $csvData += [PSCustomObject]@{
                    Type = "Skill"
                    Suggestion = $skill.Skill
                    Confidence = $skill.Confidence.ToString("F3")
                }
            }
            
            return $csvData | ConvertTo-Csv -NoTypeInformation | Out-String
        }
        
        "detailed" {
            $output = @()
            $output += "=" * 80
            $output += "INTELLIGENT ISSUE ROUTING ANALYSIS"
            $output += "=" * 80
            $output += ""
            $output += "Analysis Metadata:"
            $output += "  Timestamp: $($Analysis.Metadata.Timestamp)"
            $output += "  Confidence Threshold: $($Analysis.Metadata.Threshold.ToString('F2'))"
            $output += "  Title Length: $($Analysis.Metadata.TitleLength) characters"
            $output += "  Description Length: $($Analysis.Metadata.DescriptionLength) characters"
            $output += "  Unique Tokens: $($Analysis.Metadata.TokenCount)"
            $output += ""
            
            # Component Analysis
            $output += "COMPONENT ANALYSIS:"
            $output += "-" * 40
            foreach ($comp in $Config.ComponentKeywords.Keys | Sort-Object) {
                $score = $Analysis.Scores.Components[$comp]
                $status = if ($score -ge $Threshold) { "* SUGGESTED" } else { "  below threshold" }
                $output += "  $comp`: $($score.ToString('F3')) $status"
            }
            $output += ""
            
            # Top Component Suggestions
            if ($Analysis.Suggestions.Components.Count -gt 0) {
                $output += "TOP COMPONENT SUGGESTIONS:"
                foreach ($comp in $Analysis.Suggestions.Components | Select-Object -First 3) {
                    $output += "  $($comp.Component) (confidence: $($comp.Confidence.ToString('F3')))"
                }
            } else {
                $output += "No component suggestions above threshold ($($Threshold.ToString('F2')))"
            }
            $output += ""
            
            # Priority Analysis
            $output += "PRIORITY ANALYSIS:"
            $output += "-" * 40
            foreach ($priority in $Config.PriorityPatterns.Keys | Sort-Object) {
                $score = $Analysis.Scores.Priority[$priority]
                $status = if ($Analysis.Suggestions.Priority.Priority -eq $priority) { "* RECOMMENDED" } else { "" }
                $output += "  $priority`: $($score.ToString('F3')) $status"
            }
            
            if ($Analysis.Suggestions.Priority) {
                $output += ""
                $output += "RECOMMENDED PRIORITY: $($Analysis.Suggestions.Priority.Priority.ToUpper()) (confidence: $($Analysis.Suggestions.Priority.Confidence.ToString('F3')))"
            }
            $output += ""
            
            # Skill Analysis
            $output += "SKILL REQUIREMENTS ANALYSIS:"
            $output += "-" * 40
            foreach ($skill in $Config.SkillPatterns.Keys | Sort-Object) {
                $score = $Analysis.Scores.Skills[$skill]
                $threshold = $Threshold * 0.8
                $status = if ($score -ge $threshold) { "* REQUIRED" } else { "  optional" }
                $output += "  $skill`: $($score.ToString('F3')) $status"
            }
            
            if ($Analysis.Suggestions.Skills.Count -gt 0) {
                $output += ""
                $output += "REQUIRED SKILLS:"
                foreach ($skill in $Analysis.Suggestions.Skills) {
                    $output += "  $($skill.Skill) (confidence: $($skill.Confidence.ToString('F3')))"
                }
            }
            $output += ""
            
            # Token Analysis
            if ($ShowVerbose) {
                $output += "TOKEN ANALYSIS:"
                $output += "-" * 40
                $output += "Title Tokens: $($Analysis.Tokens.Title -join ', ')"
                $output += "Description Tokens: $($Analysis.Tokens.Description -join ', ')"
                $output += "All Unique Tokens: $($Analysis.Tokens.All -join ', ')"
                $output += ""
            }
            
            $output += "=" * 80
            
            return $output -join "`n"
        }
        
        default { # "text"
            $output = @()
            $output += "Intelligent Issue Routing Analysis"
            $output += "Analyzed at: $($Analysis.Metadata.Timestamp)"
            $output += ""
            
            if ($Analysis.Suggestions.Components.Count -gt 0) {
                $output += "Component Suggestions:"
                foreach ($comp in $Analysis.Suggestions.Components) {
                    $output += "  $($comp.Component) (confidence: $($comp.Confidence.ToString('F3')))"
                }
            } else {
                $output += "No component suggestions above threshold ($($Threshold.ToString('F2')))"
            }
            $output += ""
            
            if ($Analysis.Suggestions.Priority) {
                $output += "Priority Recommendation: $($Analysis.Suggestions.Priority.Priority) (confidence: $($Analysis.Suggestions.Priority.Confidence.ToString('F3')))"
            } else {
                $output += "No clear priority recommendation"
            }
            $output += ""
            
            if ($Analysis.Suggestions.Skills.Count -gt 0) {
                $output += "Skill Requirements:"
                foreach ($skill in $Analysis.Suggestions.Skills) {
                    $output += "  $($skill.Skill) (confidence: $($skill.Confidence.ToString('F3')))"
                }
            } else {
                $output += "No specific skill requirements identified"
            }
            
            return $output -join "`n"
        }
    }
}

# ============================================================================
# GITHUB INTEGRATION FUNCTIONS
# ============================================================================

function Get-GitHubIssue {
    <#
    .SYNOPSIS
    Retrieve issue content from GitHub
    
    .DESCRIPTION
    Fetches issue title and body from GitHub API or local git repository
    
    .PARAMETER IssueNumber
    GitHub issue number to retrieve
    
    .RETURNS
    Issue object with title and body
    #>
    param([int]$IssueNumber)
    
    Write-Verbose "Retrieving GitHub issue #$IssueNumber..."
    
    try {
        # Try to get issue from GitHub CLI if available
        $ghResult = & gh issue view $IssueNumber --json title,body 2>$null
        if ($LASTEXITCODE -eq 0) {
            $issueData = $ghResult | ConvertFrom-Json
            return @{
                Title = $issueData.title
                Body = $issueData.body
                Source = "GitHub CLI"
            }
        }
    } catch {
        Write-Verbose "GitHub CLI not available or failed: $($_.Exception.Message)"
    }
    
    # Fallback: try to parse from local git repository
    try {
        $gitLog = & git log --grep="#$IssueNumber" --oneline | Select-Object -First 1
        if ($gitLog) {
            return @{
                Title = $gitLog -replace "^[a-f0-9]+ ", ""
                Body = "Retrieved from git log"
                Source = "Git Log"
            }
        }
    } catch {
        Write-Verbose "Git log search failed: $($_.Exception.Message)"
    }
    
    throw "Unable to retrieve issue #$IssueNumber from GitHub or git repository"
}

function Apply-RoutingSuggestions {
    <#
    .SYNOPSIS
    Apply routing suggestions to GitHub issue
    
    .DESCRIPTION
    Updates GitHub issue with component labels, priority, and assignment
    based on intelligent routing analysis.
    
    .PARAMETER IssueNumber
    GitHub issue number to update
    
    .PARAMETER Analysis
    Analysis results with suggestions
    
    .PARAMETER DryRun
    Show what would be done without making changes
    
    .RETURNS
    Array of actions taken or that would be taken
    #>
    param(
        [int]$IssueNumber,
        [object]$Analysis,
        [bool]$DryRun = $false
    )
    
    $actions = @()
    
    Write-Verbose "Applying routing suggestions to issue #$IssueNumber (DryRun: $DryRun)..."
    
    # Apply component labels
    foreach ($comp in $Analysis.Suggestions.Components) {
        $label = "component:$($comp.Component)"
        $action = "Add label '$label' (confidence: $($comp.Confidence.ToString('F3')))"
        $actions += $action
        
        if (-not $DryRun) {
            try {
                & gh issue edit $IssueNumber --add-label $label
                Write-Verbose "Applied label: $label"
            } catch {
                Write-Warning "Failed to apply label $label`: $($_.Exception.Message)"
            }
        }
    }
    
    # Apply priority label
    if ($Analysis.Suggestions.Priority -and $Analysis.Suggestions.Priority.Confidence -ge $Threshold) {
        $priorityLabel = "priority:$($Analysis.Suggestions.Priority.Priority)"
        $action = "Add priority label '$priorityLabel' (confidence: $($Analysis.Suggestions.Priority.Confidence.ToString('F3')))"
        $actions += $action
        
        if (-not $DryRun) {
            try {
                & gh issue edit $IssueNumber --add-label $priorityLabel
                Write-Verbose "Applied priority label: $priorityLabel"
            } catch {
                Write-Warning "Failed to apply priority label $priorityLabel`: $($_.Exception.Message)"
            }
        }
    }
    
    # Add intelligent routing comment
    if (-not $DryRun) {
        $comment = @"
[ROBOT] **Intelligent Issue Routing Analysis**

This issue has been automatically analyzed using NLP techniques:

**Component Suggestions:**
$( ($Analysis.Suggestions.Components | ForEach-Object { "- $($_.Component) (confidence: $($_.Confidence.ToString('F3')))" }) -join "`n" )

**Priority Recommendation:** $($Analysis.Suggestions.Priority.Priority) (confidence: $($Analysis.Suggestions.Priority.Confidence.ToString('F3')))

**Required Skills:**
$( ($Analysis.Suggestions.Skills | ForEach-Object { "- $($_.Skill) (confidence: $($_.Confidence.ToString('F3')))" }) -join "`n" )

*Analysis performed at $($Analysis.Metadata.Timestamp) with threshold $($Analysis.Metadata.Threshold.ToString('F2'))*
"@
        
        try {
            $comment | & gh issue comment $IssueNumber --body-file -
            $actions += "Added intelligent routing analysis comment"
            Write-Verbose "Added analysis comment to issue"
        } catch {
            Write-Warning "Failed to add analysis comment: $($_.Exception.Message)"
        }
    }
    
    return $actions
}

# ============================================================================
# BATCH PROCESSING FUNCTIONS
# ============================================================================

function Invoke-BatchRouting {
    <#
    .SYNOPSIS
    Process multiple issues with intelligent routing
    
    .DESCRIPTION
    Analyzes and applies routing suggestions to a batch of GitHub issues
    
    .PARAMETER IssueNumbers
    Array of issue numbers to process
    
    .PARAMETER DryRun
    Show what would be done without making changes
    
    .RETURNS
    Batch processing results
    #>
    param(
        [int[]]$IssueNumbers,
        [bool]$DryRun = $false
    )
    
    $results = @()
    $processed = 0
    $total = $IssueNumbers.Count
    
    Write-Host "Starting batch routing for $total issues..." -ForegroundColor Green
    
    foreach ($issueNum in $IssueNumbers) {
        $processed++
        Write-Progress -Activity "Processing Issues" -Status "Issue #$issueNum ($processed/$total)" -PercentComplete (($processed / $total) * 100)
        
        try {
            # Get issue content
            $issue = Get-GitHubIssue -IssueNumber $issueNum
            
            # Analyze issue
            $analysis = Get-IssueAnalysis -Title $issue.Title -Description $issue.Body
            
            # Apply suggestions
            $actions = Apply-RoutingSuggestions -IssueNumber $issueNum -Analysis $analysis -DryRun $DryRun
            
            $results += @{
                IssueNumber = $issueNum
                Title = $issue.Title
                Analysis = $analysis
                Actions = $actions
                Status = "Success"
                Error = $null
            }
            
            Write-Verbose "Successfully processed issue #$issueNum"
            
        } catch {
            $results += @{
                IssueNumber = $issueNum
                Title = "Unable to retrieve"
                Analysis = $null
                Actions = @()
                Status = "Error"
                Error = $_.Exception.Message
            }
            
            Write-Warning "Failed to process issue #$issueNum`: $($_.Exception.Message)"
        }
        
        # Rate limiting delay
        Start-Sleep -Milliseconds 500
    }
    
    Write-Progress -Activity "Processing Issues" -Completed
    Write-Host "Batch processing completed: $($results.Count) issues processed" -ForegroundColor Green
    
    return $results
}

# ============================================================================
# TRAINING AND LEARNING FUNCTIONS
# ============================================================================

function Update-RoutingModel {
    <#
    .SYNOPSIS
    Update routing model based on feedback
    
    .DESCRIPTION
    Learns from manual corrections and feedback to improve routing accuracy
    
    .PARAMETER FeedbackData
    Training data with correct classifications
    
    .RETURNS
    Updated model statistics
    #>
    param([object[]]$FeedbackData)
    
    Write-Host "Training mode: Updating routing model..." -ForegroundColor Yellow
    Write-Host "This feature will be implemented in a future version." -ForegroundColor Yellow
    Write-Host "Current implementation focuses on rule-based NLP routing." -ForegroundColor Yellow
    
    # TODO: Implement machine learning feedback loop
    # - Store feedback data in training database
    # - Adjust keyword weights based on success rates
    # - Learn new keyword associations from corrections
    # - Update confidence thresholds based on accuracy metrics
    
    return @{
        Status = "Not Implemented"
        Message = "Machine learning training will be added in future version"
        CurrentApproach = "Rule-based NLP with weighted keyword matching"
    }
}

# ============================================================================
# LOGGING AND REPORTING FUNCTIONS
# ============================================================================

function Write-AnalysisLog {
    <#
    .SYNOPSIS
    Log analysis results to file
    
    .DESCRIPTION
    Saves analysis results and actions to timestamped log file
    
    .PARAMETER Analysis
    Analysis results to log
    
    .PARAMETER Actions
    Actions taken or suggested
    
    .PARAMETER IssueNumber
    Issue number being processed
    
    .RETURNS
    Path to log file
    #>
    param(
        [object]$Analysis,
        [string[]]$Actions = @(),
        [int]$IssueNumber = 0
    )
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $logFile = "tmp/intelligent_routing_$timestamp.log"
    
    $logData = @{
        Timestamp = $Analysis.Metadata.Timestamp
        IssueNumber = $IssueNumber
        Analysis = $Analysis
        Actions = $Actions
        Environment = @{
            Threshold = $Threshold
            DryRun = $DryRun.IsPresent
            Verbose = $ShowVerbose.IsPresent
            Format = $Format
        }
    }
    
    try {
        # Ensure tmp directory exists
        if (-not (Test-Path "tmp")) {
            New-Item -ItemType Directory -Path "tmp" -Force | Out-Null
        }
        
        $logData | ConvertTo-Json -Depth 10 | Out-File -FilePath $logFile -Encoding UTF8
        
        Write-Verbose "Analysis logged to: $logFile"
        return $logFile
        
    } catch {
        Write-Warning "Failed to write log file: $($_.Exception.Message)"
        return $null
    }
}

# ============================================================================
# MAIN EXECUTION LOGIC
# ============================================================================

function Show-Help {
    @"
INTELLIGENT ISSUE ROUTING SYSTEM
Phase 3 of DexBot GitHub Issues Workflow Implementation

DESCRIPTION:
    Uses Natural Language Processing (NLP) techniques to analyze GitHub issues
    and automatically suggest component labels, priority levels, and skill
    requirements based on issue content.

USAGE:
    .\intelligent_routing.ps1 -Action <action> [parameters]

ACTIONS:
    analyze     Analyze issue text and show suggestions
    suggest     Generate suggestions without applying changes
    route       Apply suggestions to GitHub issue (requires gh CLI)
    batch       Process multiple issues in batch mode
    train       Update routing model based on feedback (future feature)
    help        Show this help message

EXAMPLES:
    # Analyze issue text directly
    .\intelligent_routing.ps1 -Action analyze -IssueText "Combat system crashes when target dies"
    
    # Analyze GitHub issue by number
    .\intelligent_routing.ps1 -Action analyze -IssueNumber 123 -Format detailed
    
    # Apply routing suggestions to issue (dry run)
    .\intelligent_routing.ps1 -Action route -IssueNumber 123 -DryRun
    
    # Batch process multiple issues
    .\intelligent_routing.ps1 -Action batch -IssueFile "issues.txt" -Threshold 0.8
    
    # Get suggestions in JSON format
    .\intelligent_routing.ps1 -Action suggest -IssueText "Need to fix looting system" -Format json

PARAMETERS:
    -IssueText          Issue title or description text for analysis
    -IssueFile          Path to file containing issue data or issue numbers
    -IssueNumber        GitHub issue number to analyze
    -Action             Action to perform (analyze|suggest|route|batch|train|help)
    -Format             Output format (text|json|csv|detailed)
    -Threshold          Confidence threshold for suggestions (0.0-1.0, default: 0.7)
    -DryRun             Show suggestions without applying changes
    -ShowVerbose        Show detailed analysis information
    -LogResults         Save analysis results to timestamped log file

FEATURES:
    [x] Natural Language Processing with tokenization and stemming
    [x] Multi-component keyword matching with confidence scoring
    [x] Priority and skill requirement analysis
    [x] GitHub integration via GitHub CLI
    [x] Batch processing with progress tracking
    [x] Multiple output formats (text, JSON, CSV, detailed)
    [x] Comprehensive logging and audit trail
    [x] Dry-run mode for safe testing

REQUIREMENTS:
    - PowerShell 5.1 or later
    - GitHub CLI (gh) for issue updates (optional)
    - Git repository context for issue retrieval

For more information, see: docs/GITHUB_ISSUES_IMPLEMENTATION_ROADMAP.md
"@
}

# Main execution
try {
    Write-Verbose "Starting Intelligent Issue Routing System..."
    Write-Verbose "Action: $Action, Threshold: $Threshold, Format: $Format"
    
    switch ($Action.ToLower()) {
        "help" {
            Show-Help
            exit 0
        }
        
        { ($_ -eq "analyze") -or ($_ -eq "suggest") } {
            $title = ""
            $description = ""
            
            # Determine input source
            if ($IssueNumber -gt 0) {
                Write-Host "Retrieving issue #$IssueNumber..." -ForegroundColor Yellow
                $issue = Get-GitHubIssue -IssueNumber $IssueNumber
                $title = $issue.Title
                $description = $issue.Body
                Write-Host "Retrieved: $title" -ForegroundColor Green
            } elseif (-not [string]::IsNullOrWhiteSpace($IssueText)) {
                $title = $IssueText
                $description = ""
            } elseif (-not [string]::IsNullOrWhiteSpace($IssueFile)) {
                if (Test-Path $IssueFile) {
                    $content = Get-Content $IssueFile -Raw
                    $lines = $content -split "`n"
                    $title = $lines[0]
                    $description = ($lines[1..($lines.Length-1)] -join "`n").Trim()
                } else {
                    throw "Issue file not found: $IssueFile"
                }
            } else {
                throw "No issue content provided. Use -IssueText, -IssueFile, or -IssueNumber"
            }
            
            # Perform analysis
            if ($Format.ToLower() -ne "json") {
                Write-Host "Analyzing issue content..." -ForegroundColor Yellow
            }
            $analysis = Get-IssueAnalysis -Title $title -Description $description
            
            # Output results
            $output = Format-AnalysisOutput -Analysis $analysis -Format $Format
            Write-Host $output
            
            # Log results if requested
            if ($LogResults) {
                $logFile = Write-AnalysisLog -Analysis $analysis -IssueNumber $IssueNumber
                if ($logFile) {
                    Write-Host "`nResults logged to: $logFile" -ForegroundColor Green
                }
            }
        }
        
        "route" {
            if ($IssueNumber -le 0) {
                throw "Issue number required for routing action. Use -IssueNumber parameter"
            }
            
            # Get issue and analyze
            Write-Host "Retrieving and analyzing issue #$IssueNumber..." -ForegroundColor Yellow
            $issue = Get-GitHubIssue -IssueNumber $IssueNumber
            $analysis = Get-IssueAnalysis -Title $issue.Title -Description $issue.Body
            
            # Apply suggestions
            $modeText = if ($DryRun) { " (DRY RUN)" } else { "" }
            Write-Host "Applying routing suggestions$modeText..." -ForegroundColor Yellow
            
            $actions = Apply-RoutingSuggestions -IssueNumber $IssueNumber -Analysis $analysis -DryRun $DryRun
            
            Write-Host "`nActions taken:" -ForegroundColor Green
            foreach ($action in $actions) {
                Write-Host "  $action" -ForegroundColor White
            }
            
            # Show analysis summary
            Write-Host "`nAnalysis Summary:" -ForegroundColor Cyan
            $summary = Format-AnalysisOutput -Analysis $analysis -Format "text"
            Write-Host $summary
            
            # Log results
            if ($LogResults) {
                $logFile = Write-AnalysisLog -Analysis $analysis -Actions $actions -IssueNumber $IssueNumber
                if ($logFile) {
                    Write-Host "`nResults logged to: $logFile" -ForegroundColor Green
                }
            }
        }
        
        "batch" {
            $issueNumbers = @()
            
            # Parse issue numbers from file or parameter
            if (-not [string]::IsNullOrWhiteSpace($IssueFile)) {
                if (Test-Path $IssueFile) {
                    $content = Get-Content $IssueFile
                    $issueNumbers = $content | ForEach-Object {
                        if ($_ -match '^\d+$') { [int]$_ }
                    } | Where-Object { $_ -gt 0 }
                } else {
                    throw "Issue file not found: $IssueFile"
                }
            } elseif ($IssueNumber -gt 0) {
                $issueNumbers = @($IssueNumber)
            } else {
                throw "No issue numbers provided. Use -IssueFile with list of issue numbers or -IssueNumber for single issue"
            }
            
            if ($issueNumbers.Count -eq 0) {
                throw "No valid issue numbers found"
            }
            
            Write-Host "Starting batch routing for $($issueNumbers.Count) issues..." -ForegroundColor Green
            
            $results = Invoke-BatchRouting -IssueNumbers $issueNumbers -DryRun $DryRun
            
            # Show summary
            $successful = ($results | Where-Object { $_.Status -eq "Success" }).Count
            $failed = ($results | Where-Object { $_.Status -eq "Error" }).Count
            
            Write-Host "`nBatch Processing Complete:" -ForegroundColor Green
            Write-Host "  Successful: $successful" -ForegroundColor Green
            Write-Host "  Failed: $failed" -ForegroundColor Red
            
            # Show failed issues
            if ($failed -gt 0) {
                Write-Host "`nFailed Issues:" -ForegroundColor Red
                $results | Where-Object { $_.Status -eq "Error" } | ForEach-Object {
                    Write-Host "  Issue #$($_.IssueNumber): $($_.Error)" -ForegroundColor Yellow
                }
            }
            
            # Export results
            $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
            $resultFile = "tmp/batch_routing_results_$timestamp.json"
            
            try {
                if (-not (Test-Path "tmp")) {
                    New-Item -ItemType Directory -Path "tmp" -Force | Out-Null
                }
                
                $results | ConvertTo-Json -Depth 10 | Out-File -FilePath $resultFile -Encoding UTF8
                Write-Host "`nDetailed results exported to: $resultFile" -ForegroundColor Green
            } catch {
                Write-Warning "Failed to export results: $($_.Exception.Message)"
            }
        }
        
        "train" {
            $trainingResult = Update-RoutingModel -FeedbackData @()
            Write-Host ($trainingResult | ConvertTo-Json -Depth 3)
        }
        
        default {
            throw "Unknown action: $Action. Use 'help' action to see available options."
        }
    }
    
    Write-Verbose "Intelligent Issue Routing completed successfully"
    
} catch {
    Write-Error "Intelligent Issue Routing failed: $($_.Exception.Message)"
    
    if ($ShowVerbose) {
        Write-Host "`nFull Error Details:" -ForegroundColor Red
        Write-Host $_.Exception.ToString() -ForegroundColor Yellow
        Write-Host "`nStack Trace:" -ForegroundColor Red
        Write-Host $_.ScriptStackTrace -ForegroundColor Yellow
    }
    
    exit 1
}
