# DexBot Development Tasks & Feature Tracking

**Last Updated**: June 28, 2025
**Current Version**: 2.1.0

## Overview
This document tracks planned features, current development tasks, and their implementation status for the DexBot modular bot system, based on the official [Product Requirements Document](DexBot_PRD.md).

---

## ✅ Completed Tasks (v2.1.0)

### ✅ Development Infrastructure & Build System
- **Task**: Transition from a monolithic script to a modular project structure.
- **Task**: Implement a `src` directory for separated source code.
- **Task**: Set up development tooling (`invoke`, `pyproject.toml`).
- **Task**: Create an automated build system to bundle modules into a single distribution file (`tasks.py`).
- **Task**: Establish a structured testing framework (`tests/` directory).
- **Task**: Integrate code quality tools (`.flake8`).

### ✅ Auto Heal System
- **FR-001**: Implement intelligent healing logic (potions for critical, bandages for normal).
- **FR-002**: Implement dual resource management for bandages and potions.
- **FR-003**: Implement real-time health monitoring.
- **FR-004**: Implement advanced retry mechanism for bandages.
- **FR-005**: Implement low resource warnings.
- **FR-006**: Implement journal integration for cooldown tracking.
- **FR-007**: Implement death and resurrection handling.

### ✅ Modern GUMP Interface
- **FR-008**: Create the main status GUMP.
- **FR-009**: Integrate all settings into the main interface.
- **FR-010**: Implement dynamic UI updates to optimize performance.
- **FR-011**: Implement multiple view states (full/minimized).
- **FR-012**: Implement interactive controls with tooltips.
- **FR-013**: Implement color-coded status indicators.
- **FR-014**: Implement rate limiting for button presses.

### ✅ Configuration Management System
- **FR-015**: Implement JSON-based configuration.
- **FR-016**: Implement persistent settings for GUMP toggles.
- **FR-017**: Implement runtime reloading of configuration.
- **FR-018**: Implement default value handling for new configurations.
- **FR-019**: Implement merge protection for configuration updates.

### ✅ Robust Architecture
- **FR-020**: Implement Singleton pattern for configuration and status.
- **FR-021**: Implement a modular design for the codebase.
- **FR-022**: Enforce type safety with type hints.
- **FR-023**: Implement error recovery for common issues.
- **FR-024**: Optimize performance of the bot.
- **FR-025**: Implement a comprehensive logging system.

---

## 🔄 Planned Future Modules

### 🔲 Combat System
- **Priority**: High
- **Status**: Not Started
- **Dependencies**: Auto Heal System
- **Description**: A comprehensive combat system to engage and defeat enemies automatically. This is a foundational module for any PvE automation.
- **Sub-tasks**:
  - 🔲 Detect nearby hostile targets.
  - 🔲 Select a target based on configurable priority (e.g., closest, lowest health).
  - 🔲 Engage the target with the currently equipped weapon.
  - 🔲 Monitor combat status (e.g., target is dead, player is being attacked).
  - 🔲 Disengage or switch targets as needed.

### 🔲 Looting System
- **Priority**: High
- **Status**: Not Started
- **Dependencies**: Combat System
- **Description**: Automatically loot corpses of defeated enemies and skin them for resources.
- **Sub-tasks**:
  - 🔲 Detect nearby corpses.
  - 🔲 Open and loot items from corpses based on a configurable loot list.
  - 🔲 Implement skinning logic for creatures that can be skinned.
  - 🔲 Handle container logic (e.g., looting items from a bag on the corpse).

### 🔲 Buff Management System
- **Priority**: Medium-High
- **Status**: Not Started
- **Dependencies**: None, but most useful with the Combat System.
- **Description**: Automatically maintain player buffs, such as Strength and Agility potions, to ensure peak combat effectiveness.
- **Sub-tasks**:
  - 🔲 Monitor active buffs on the player.
  - 🔲 Use potions or spells to re-apply buffs when they expire.
  - 🔲 Allow configuration of which buffs to maintain.

### 🔲 Inventory Management System
- **Priority**: Medium
- **Status**: Not Started
- **Dependencies**: Looting System
- **Description**: A system to manage the player's inventory to prevent it from becoming full during long botting sessions.
- **Sub-tasks**:
  - 🔲 Monitor backpack item count/weight.
  - 🔲 Automatically drop or move items based on a configurable list (e.g., drop junk items).
  - 🔲 Potentially move valuable items to a secure container.

### 🔲 Fishing System
- **Priority**: Low
- **Status**: Not Started
- **Dependencies**: None
- **Description**: An AFK fishing system to automate the process of fishing for resources.
- **Sub-tasks**:
  - 🔲 Use a fishing pole on a water source.
  - 🔲 Detect successful catches and reel them in.
  - 🔲 Handle common fishing events (e.g., "the fish got away").
