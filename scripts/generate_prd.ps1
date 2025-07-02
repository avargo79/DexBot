#!/usr/bin/env powershell
<#
.SYNOPSIS
    Generate Product Requirements Document (PRD) templates for DexBot features

.DESCRIPTION
    Creates standardized PRD templates for feature requests, with options for
    minimal, comprehensive, and custom templates. Integrates with GitHub Issues
    workflow for fast-track processing.

.PARAMETER TemplateName
    Name of the PRD template to generate

.PARAMETER OutputPath
    Path where the PRD file will be created (default: current directory)

.PARAMETER TemplateType
    Type of template: minimal, comprehensive, or custom

.PARAMETER FeatureTitle
    Title of the feature for the PRD

.PARAMETER ComponentType
    DexBot component this feature relates to

.PARAMETER PriorityLevel
    Priority level for the feature

.PARAMETER Interactive
    Run in interactive mode with prompts

.PARAMETER Force
    Overwrite existing files

.EXAMPLE
    .\generate_prd.ps1 -TemplateName "BuffManagement" -TemplateType comprehensive
    .\generate_prd.ps1 -Interactive
    .\generate_prd.ps1 -FeatureTitle "Auto Resurrection" -ComponentType "Auto Heal" -TemplateType minimal
#>

param(
    [string]$TemplateName,
    
    [string]$OutputPath = ".",
    
    [ValidateSet("minimal", "comprehensive", "custom")]
    [string]$TemplateType = "comprehensive",
    
    [string]$FeatureTitle,
    
    [ValidateSet("Auto Heal System", "Combat System", "Looting System", "User Interface (GUMPs)", "Configuration Management", "Core Systems", "Build/Development Tools", "Documentation")]
    [string]$ComponentType,
    
    [ValidateSet("Low", "Medium", "High", "Critical")]
    [string]$PriorityLevel = "Medium",
    
    [switch]$Interactive = $false,
    
    [switch]$Force = $false
)

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

Write-Info "DexBot PRD Template Generator"
Write-Info "============================"

# Interactive mode
if ($Interactive) {
    Write-Info "Interactive PRD Template Generation"
    Write-Host ""
    
    # Get feature title
    if (-not $FeatureTitle) {
        $FeatureTitle = Read-Host "Enter feature title (e.g., 'Buff Management System')"
    }
    
    # Get template name from feature title if not provided
    if (-not $TemplateName) {
        $TemplateName = ($FeatureTitle -replace '[^a-zA-Z0-9]', '') + "_PRD"
    }
    
    # Get component type
    if (-not $ComponentType) {
        Write-Host ""
        Write-Info "Available components:"
        Write-Host "  1. Auto Heal System" -ForegroundColor Gray
        Write-Host "  2. Combat System" -ForegroundColor Gray
        Write-Host "  3. Looting System" -ForegroundColor Gray
        Write-Host "  4. User Interface (GUMPs)" -ForegroundColor Gray
        Write-Host "  5. Configuration Management" -ForegroundColor Gray
        Write-Host "  6. Core Systems" -ForegroundColor Gray
        Write-Host "  7. Build/Development Tools" -ForegroundColor Gray
        Write-Host "  8. Documentation" -ForegroundColor Gray
        
        $componentChoice = Read-Host "Select component (1-8)"
        $componentMap = @{
            "1" = "Auto Heal System"
            "2" = "Combat System"
            "3" = "Looting System"
            "4" = "User Interface (GUMPs)"
            "5" = "Configuration Management"
            "6" = "Core Systems"
            "7" = "Build/Development Tools"
            "8" = "Documentation"
        }
        $ComponentType = $componentMap[$componentChoice]
    }
    
    # Get priority level
    if (-not $PriorityLevel -or $PriorityLevel -eq "Medium") {
        Write-Host ""
        Write-Info "Priority levels:"
        Write-Host "  1. Low - Nice to have enhancement" -ForegroundColor Gray
        Write-Host "  2. Medium - Useful improvement (default)" -ForegroundColor Gray
        Write-Host "  3. High - Important feature" -ForegroundColor Gray
        Write-Host "  4. Critical - Essential functionality" -ForegroundColor Gray
        
        $priorityChoice = Read-Host "Select priority (1-4, default: 2)"
        if ($priorityChoice -eq "") { $priorityChoice = "2" }
        
        $priorityMap = @{
            "1" = "Low"
            "2" = "Medium"
            "3" = "High"
            "4" = "Critical"
        }
        $PriorityLevel = $priorityMap[$priorityChoice]
    }
    
    # Get template type
    Write-Host ""
    Write-Info "Template types:"
    Write-Host "  1. Minimal - Basic structure with core sections" -ForegroundColor Gray
    Write-Host "  2. Comprehensive - Full PRD with all sections (default)" -ForegroundColor Gray
    Write-Host "  3. Custom - Interactive customization" -ForegroundColor Gray
    
    $templateChoice = Read-Host "Select template type (1-3, default: 2)"
    if ($templateChoice -eq "") { $templateChoice = "2" }
    
    $templateMap = @{
        "1" = "minimal"
        "2" = "comprehensive"
        "3" = "custom"
    }
    $TemplateType = $templateMap[$templateChoice]
}

# Validate required parameters
if (-not $FeatureTitle) {
    Write-Error "FeatureTitle is required. Use -Interactive or specify -FeatureTitle"
    exit 1
}

if (-not $TemplateName) {
    $TemplateName = ($FeatureTitle -replace '[^a-zA-Z0-9]', '') + "_PRD"
}

# Create output file path
$outputFile = Join-Path $OutputPath "$TemplateName.md"

# Check if file exists
if ((Test-Path $outputFile) -and (-not $Force)) {
    Write-Error "File already exists: $outputFile"
    Write-Info "Use -Force to overwrite or choose a different name"
    exit 1
}

Write-Host ""
Write-Info "Generating PRD template..."
Write-Host "  Feature: $FeatureTitle" -ForegroundColor Gray
Write-Host "  Component: $ComponentType" -ForegroundColor Gray
Write-Host "  Priority: $PriorityLevel" -ForegroundColor Gray
Write-Host "  Template: $TemplateType" -ForegroundColor Gray
Write-Host "  Output: $outputFile" -ForegroundColor Gray

# Generate current date
$currentDate = Get-Date -Format "yyyy-MM-dd"
$currentDateTime = Get-Date -Format "yyyy-MM-dd HH:mm"

# Create the PRD content based on template type
switch ($TemplateType) {
    "minimal" {
        $prdContent = @"
# Product Requirements Document (PRD)
## $FeatureTitle

**Date**: $currentDate  
**Component**: $ComponentType  
**Priority**: $PriorityLevel  
**Status**: Draft  

---

## Problem Statement

*Describe the problem this feature solves and why it's important for DexBot users.*

[Provide a clear, concise description of the current problem or limitation]

## Success Criteria

*Define what success looks like for this feature.*

- [ ] Primary success metric
- [ ] Secondary success metric
- [ ] User satisfaction measure

## User Stories

*Describe how users will interact with this feature.*

**As a** DexBot user  
**I want** [desired functionality]  
**So that** [benefit or outcome]

## Technical Requirements

*High-level technical requirements for implementation.*

- **API Requirements**: [RazorEnhanced APIs needed]
- **Performance**: [Performance requirements]
- **Configuration**: [Configuration needs]
- **Integration**: [Integration points]

## Acceptance Criteria

*Testable criteria that define when the feature is complete.*

- [ ] [Specific, testable requirement]
- [ ] [Specific, testable requirement]
- [ ] [Specific, testable requirement]

## Implementation Notes

*Additional context for developers.*

[Any specific implementation guidance or constraints]

---

*PRD generated on $currentDateTime using DexBot PRD Template Generator*
"@
    }
    
    "comprehensive" {
        $prdContent = @"
# Product Requirements Document (PRD)
## $FeatureTitle

**Date**: $currentDate  
**Component**: $ComponentType  
**Priority**: $PriorityLevel  
**Status**: Draft  
**Version**: 1.0  

---

## Executive Summary

*Brief overview of the feature and its strategic importance.*

[Provide a 2-3 sentence summary of what this feature does and why it's valuable]

## Problem Statement

*Detailed description of the problem this feature addresses.*

### Current State
[Describe the current situation, limitations, or pain points]

### Desired State
[Describe the ideal situation after implementing this feature]

### Impact of Not Solving
[Explain what happens if this problem remains unsolved]

## Success Criteria

*Measurable outcomes that define success.*

### Primary Success Metrics
- [ ] [Quantifiable primary metric]
- [ ] [Quantifiable primary metric]

### Secondary Success Metrics
- [ ] [Supporting metric]
- [ ] [Supporting metric]

### User Satisfaction
- [ ] [User experience improvement]
- [ ] [User workflow enhancement]

## User Stories

*Comprehensive user scenarios and use cases.*

### Primary User Story
**As a** DexBot user  
**I want** [primary desired functionality]  
**So that** [primary benefit or outcome]

### Secondary User Stories
**As a** DexBot user  
**I want** [secondary functionality]  
**So that** [secondary benefit]

**As a** DexBot administrator  
**I want** [configuration capability]  
**So that** [administrative benefit]

### Edge Cases
**As a** DexBot user  
**I want** [edge case handling]  
**So that** [reliability benefit]

## Technical Requirements

*Detailed technical specifications for implementation.*

### RazorEnhanced API Requirements
- **Player APIs**: [Player.* methods needed]
- **Items APIs**: [Items.* methods needed]
- **Mobiles APIs**: [Mobiles.* methods needed]
- **Misc APIs**: [Misc.* methods needed]
- **Other APIs**: [Additional API requirements]

### Performance Requirements
- **Response Time**: [Maximum acceptable latency]
- **Resource Usage**: [Memory/CPU constraints]
- **Session Duration**: [12+ hour session compatibility]
- **API Call Frequency**: [Rate limiting considerations]

### Configuration Requirements
- **Config File**: [JSON configuration structure]
- **User Settings**: [Customizable parameters]
- **Default Values**: [Sensible defaults]
- **Validation**: [Input validation requirements]

### Integration Requirements
- **System Integration**: [Which DexBot systems this integrates with]
- **UI Integration**: [GUMP interface requirements]
- **Logging Integration**: [Logging and monitoring needs]
- **Error Handling**: [Error scenarios and recovery]

## Architecture Overview

*High-level system design and component interaction.*

### Component Architecture
[Describe how this feature fits into the existing DexBot architecture]

### Data Flow
[Describe how data flows through the system]

### State Management
[Describe any state that needs to be maintained]

### External Dependencies
[List any external systems or APIs this depends on]

## Acceptance Criteria

*Comprehensive, testable requirements for feature completion.*

### Core Functionality
- [ ] [Core feature requirement 1]
- [ ] [Core feature requirement 2]
- [ ] [Core feature requirement 3]

### Configuration & Settings
- [ ] [Configuration requirement 1]
- [ ] [Configuration requirement 2]

### Error Handling & Edge Cases
- [ ] [Error handling requirement 1]
- [ ] [Edge case requirement 1]

### Performance & Reliability
- [ ] [Performance requirement 1]
- [ ] [Reliability requirement 1]

### User Experience
- [ ] [UX requirement 1]
- [ ] [UX requirement 2]

### Testing Requirements
- [ ] [Testing requirement 1]
- [ ] [Testing requirement 2]

### Documentation Requirements
- [ ] [Documentation requirement 1]
- [ ] [Documentation requirement 2]

## Risk Assessment

*Potential challenges and mitigation strategies.*

### Technical Risks
- **Risk**: [Technical challenge or limitation]
  - **Impact**: [Severity and scope]
  - **Mitigation**: [Strategy to address]

### Performance Risks
- **Risk**: [Performance-related concern]
  - **Impact**: [Effect on user experience]
  - **Mitigation**: [Performance optimization approach]

### Integration Risks
- **Risk**: [Integration complexity or conflict]
  - **Impact**: [System stability or functionality impact]
  - **Mitigation**: [Integration testing and validation plan]

## Timeline Estimate

*Development effort and schedule estimation.*

### Development Phases
1. **Research & Design** (X hours)
   - API research and prototyping
   - UI/UX design and validation

2. **Core Implementation** (X hours)
   - Core functionality development
   - Configuration system integration

3. **Integration & Testing** (X hours)
   - System integration testing
   - Performance validation
   - Edge case testing

4. **Documentation & Deployment** (X hours)
   - User documentation
   - Developer documentation
   - Deployment and validation

### Total Estimated Effort
**Development Time**: X-Y hours  
**Target Completion**: [Target date]

## Testing Requirements

*Comprehensive testing strategy and validation plan.*

### Unit Testing
- [ ] [Core logic testing requirements]
- [ ] [Configuration validation testing]
- [ ] [Error handling testing]

### Integration Testing
- [ ] [System integration testing]
- [ ] [API integration testing]
- [ ] [UI integration testing]

### Performance Testing
- [ ] [Load testing requirements]
- [ ] [Long-running session testing]
- [ ] [Resource usage validation]

### User Acceptance Testing
- [ ] [User workflow testing]
- [ ] [Edge case scenario testing]
- [ ] [Configuration flexibility testing]

## Dependencies

*Prerequisites and blocking factors.*

### Technical Dependencies
- [System or component dependencies]
- [API availability requirements]
- [Third-party integrations]

### Business Dependencies
- [Stakeholder approvals needed]
- [Resource allocation requirements]
- [Timeline dependencies]

## Success Metrics & Monitoring

*How success will be measured post-implementation.*

### Performance Metrics
- [Performance indicators to monitor]
- [Baseline measurements]
- [Success thresholds]

### User Adoption Metrics
- [Usage tracking methods]
- [Adoption success criteria]
- [User feedback collection]

### System Health Metrics
- [Error rates and reliability measures]
- [Resource usage monitoring]
- [Integration health indicators]

---

## Appendix

### References
- [Related documentation links]
- [API documentation references]
- [Similar feature implementations]

### Glossary
- **Term**: Definition
- **Term**: Definition

---

*PRD generated on $currentDateTime using DexBot PRD Template Generator*  
*Template Type: Comprehensive*  
*Generated for: $ComponentType component*
"@
    }
    
    "custom" {
        Write-Info "Custom template generation - interactive section selection"
        
        # Core sections (always included)
        $sections = @(
            "Problem Statement",
            "Success Criteria", 
            "User Stories",
            "Technical Requirements",
            "Acceptance Criteria"
        )
        
        # Optional sections
        $optionalSections = @(
            "Executive Summary",
            "Architecture Overview", 
            "Risk Assessment",
            "Timeline Estimate",
            "Testing Requirements",
            "Dependencies",
            "Success Metrics & Monitoring"
        )
        
        Write-Host ""
        Write-Info "Select additional sections to include:"
        foreach ($i in 0..($optionalSections.Count - 1)) {
            $include = Read-Host "Include '$($optionalSections[$i])'? (y/N)"
            if ($include -eq "y" -or $include -eq "Y") {
                $sections += $optionalSections[$i]
            }
        }
        
        # Generate custom template
        $prdContent = @"
# Product Requirements Document (PRD)
## $FeatureTitle

**Date**: $currentDate  
**Component**: $ComponentType  
**Priority**: $PriorityLevel  
**Status**: Draft  

---

"@
        
        foreach ($section in $sections) {
            switch ($section) {
                "Executive Summary" {
                    $prdContent += @"
## Executive Summary

*Brief overview of the feature and its strategic importance.*

[Provide a 2-3 sentence summary of what this feature does and why it's valuable]

"@
                }
                "Problem Statement" {
                    $prdContent += @"
## Problem Statement

*Describe the problem this feature solves.*

[Provide a clear description of the current problem or limitation]

"@
                }
                "Success Criteria" {
                    $prdContent += @"
## Success Criteria

*Define measurable success outcomes.*

- [ ] Primary success metric
- [ ] Secondary success metric

"@
                }
                "User Stories" {
                    $prdContent += @"
## User Stories

*Describe user interactions with this feature.*

**As a** DexBot user  
**I want** [desired functionality]  
**So that** [benefit or outcome]

"@
                }
                "Technical Requirements" {
                    $prdContent += @"
## Technical Requirements

*Technical specifications for implementation.*

- **API Requirements**: [RazorEnhanced APIs needed]
- **Performance**: [Performance requirements]
- **Configuration**: [Configuration needs]

"@
                }
                "Architecture Overview" {
                    $prdContent += @"
## Architecture Overview

*High-level system design.*

[Describe component architecture and data flow]

"@
                }
                "Acceptance Criteria" {
                    $prdContent += @"
## Acceptance Criteria

*Testable completion criteria.*

- [ ] [Specific, testable requirement]
- [ ] [Specific, testable requirement]

"@
                }
                "Risk Assessment" {
                    $prdContent += @"
## Risk Assessment

*Potential challenges and mitigation strategies.*

- **Risk**: [Potential challenge]
  - **Mitigation**: [Strategy to address]

"@
                }
                "Timeline Estimate" {
                    $prdContent += @"
## Timeline Estimate

*Development effort estimation.*

**Estimated Development Time**: X-Y hours  
**Target Completion**: [Target date]

"@
                }
                "Testing Requirements" {
                    $prdContent += @"
## Testing Requirements

*Testing strategy and validation.*

- [ ] [Testing requirement]
- [ ] [Testing requirement]

"@
                }
                "Dependencies" {
                    $prdContent += @"
## Dependencies

*Prerequisites and blocking factors.*

- [Dependency or requirement]
- [Dependency or requirement]

"@
                }
                "Success Metrics & Monitoring" {
                    $prdContent += @"
## Success Metrics & Monitoring

*Post-implementation success measurement.*

- [Performance metric to monitor]
- [User adoption indicator]

"@
                }
            }
        }
        
        $prdContent += @"

---

*PRD generated on $currentDateTime using DexBot PRD Template Generator*  
*Template Type: Custom*  
*Sections: $($sections -join ', ')*
"@
    }
}

# Write the PRD file
try {
    $prdContent | Out-File -FilePath $outputFile -Encoding UTF8
    Write-Success "PRD template generated successfully!"
    Write-Host "  File: $outputFile" -ForegroundColor Green
    Write-Host "  Size: $((Get-Item $outputFile).Length) bytes" -ForegroundColor Gray
    
    Write-Host ""
    Write-Info "Next steps:"
    Write-Host "  1. Edit the PRD file to add specific details" -ForegroundColor Gray
    Write-Host "  2. Review and validate all sections" -ForegroundColor Gray
    Write-Host "  3. Copy content to GitHub issue for fast-track validation" -ForegroundColor Gray
    Write-Host "  4. Run fast-track validation: .\manage_issues.ps1 -Action fast-track -IssueNumber XXX" -ForegroundColor Gray
    
} catch {
    Write-Error "Failed to create PRD file: $($_.Exception.Message)"
    exit 1
}

Write-Host ""
Write-Info "PRD Template Generation Complete!"
Write-Success "Template '$TemplateName' created successfully in $OutputPath"
