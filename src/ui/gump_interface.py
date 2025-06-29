"""
GUMP Interface System for DexBot
Handles all in-game GUI interactions and displays
"""

import time

from ..core.bot_config import BotConfig, BotMessages, GumpState
from ..core.logger import Logger, SystemStatus
from ..utils.helpers import get_resource_color
from ..utils.imports import Gumps, Items, Player


class GumpSection:
    """Reusable component for creating consistent UI sections in the gump"""

    @staticmethod
    def create_section(
        gd,
        title,
        x,
        y,
        width,
        content_lines=None,
        title_color="#87CEEB",
        content_indent="2em",
        toggle_button=None,
    ):
        """
        Create a standardized section with title and content, optionally with a toggle button

        Args:
            gd: Gump definition object
            title: Section title text
            x, y: Position coordinates
            width: Section width
            content_lines: List of content line dictionaries with 'text' and optional 'color'
            title_color: Color for the section title
            content_indent: CSS margin-left value for content indentation
            toggle_button: Optional dict with button config: {
                'enabled': bool,
                'button_id': int,
                'enabled_art': int,
                'enabled_pressed_art': int,
                'disabled_art': int,
                'disabled_pressed_art': int,
                'tooltip': str
            }

        Returns:
            The Y position after this section (for positioning next elements)
        """
        current_y = y
        section_start_x = x

        # If toggle button is provided, add it to the left of the section
        if toggle_button:
            button_x = x - 45  # Position button to the left with margin
            button_y = current_y + 2  # Align with section title

            # Choose button art based on enabled state
            if toggle_button["enabled"]:
                button_art = toggle_button["enabled_art"]
                button_pressed_art = toggle_button["enabled_pressed_art"]
            else:
                button_art = toggle_button["disabled_art"]
                button_pressed_art = toggle_button["disabled_pressed_art"]

            # Add the toggle button
            Gumps.AddButton(
                gd,
                button_x,
                button_y,
                button_art,
                button_pressed_art,
                toggle_button["button_id"],
                1,
                0,
            )

            # Add tooltip if provided
            if "tooltip" in toggle_button:
                Gumps.AddTooltip(gd, toggle_button["tooltip"])

        # Add section title (centered)
        title_html = (
            f'<center><basefont color="{title_color}" size="3"><b>{title}</b></basefont></center>'
        )
        Gumps.AddHtml(gd, section_start_x, current_y, width, 20, title_html, False, False)
        current_y += 20

        # Add content lines if provided
        if content_lines:
            for line in content_lines:
                line_text = line.get("text", "")
                line_color = line.get("color", "#FFFFFF")

                # Apply indentation using div with margin-left
                content_html = f'<div style="margin-left: {content_indent};"><basefont color="{line_color}" size="2">{line_text}</basefont></div>'
                Gumps.AddHtml(gd, section_start_x, current_y, width, 20, content_html, False, False)
                current_y += 20

        return current_y

    @staticmethod
    def create_player_status_section(gd, x, y, width):
        """Create the player status section using the standardized format"""
        config = BotConfig()
        health_percentage = (Player.Hits / Player.HitsMax) * 100 if Player.HitsMax > 0 else 0
        health_color = get_resource_color(
            int(health_percentage), config.HEALTH_HIGH_THRESHOLD, config.HEALTH_MEDIUM_THRESHOLD
        )

        # Create content lines for player status
        content_lines = [
            {
                "text": f'HP: <basefont color="{health_color}" size="3"><b>{Player.Hits}/{Player.HitsMax}</b></basefont> <basefont color="#CCCCCC" size="2">({health_percentage:.0f}%)</basefont>',
                "color": "#FFFFFF",
            }
        ]

        return GumpSection.create_section(gd, "PLAYER STATUS", x, y, width, content_lines)

    @staticmethod
    def create_system_summary_line(
        gd,
        x,
        y,
        width,
        system_name,
        enabled,
        active,
        status_text,
        enable_button_id,
        settings_button_id,
    ):
        """
        Create a single-line system summary with toggle, name, status, and settings button

        Args:
            gd: Gump definition object
            x, y: Position coordinates
            width: Line width
            system_name: Display name of the system (e.g., "AUTO HEAL")
            enabled: Whether the system is enabled
            active: Whether the system is currently active/working
            status_text: Status description (e.g., "Ready", "Healing...", "Disabled")
            enable_button_id: Button ID for enable/disable toggle
            settings_button_id: Button ID for opening settings GUMP

        Returns:
            The Y position after this line (for positioning next elements)
        """
        config = BotConfig()
        current_y = y

        # Enable/Disable toggle button (left side)
        toggle_x = x - 40
        toggle_y = current_y + 2

        if enabled:
            toggle_art = config.BUTTON_ENABLED
            toggle_pressed_art = config.BUTTON_ENABLED_PRESSED
            system_color = "#00FF00" if active else "#FFFF00"
            toggle_tooltip = f"Disable {system_name}"
        else:
            toggle_art = config.BUTTON_DISABLE
            toggle_pressed_art = config.BUTTON_DISABLE_PRESSED
            system_color = "#FF0000"
            toggle_tooltip = f"Enable {system_name}"

        Gumps.AddButton(
            gd, toggle_x, toggle_y, toggle_art, toggle_pressed_art, enable_button_id, 1, 0
        )
        Gumps.AddTooltip(gd, toggle_tooltip)

        # Settings button (right side)
        settings_x = x + width - 25
        settings_y = current_y + 2
        Gumps.AddButton(
            gd,
            settings_x,
            settings_y,
            config.BUTTON_SETTINGS,
            config.BUTTON_SETTINGS_PRESSED,
            settings_button_id,
            1,
            0,
        )
        Gumps.AddTooltip(gd, f"Open Bot Settings")

        # System summary line
        if enabled and active:
            status_display = f'<basefont color="#FFFF00" size="2"><b>{status_text}</b></basefont>'
        elif enabled:
            status_display = f'<basefont color="#00FF00" size="2"><b>{status_text}</b></basefont>'
        else:
            status_display = f'<basefont color="#888888" size="2"><b>Disabled</b></basefont>'

        summary_line = f'<basefont color="{system_color}" size="3"><b>{system_name}</b></basefont> - {status_display}'

        # Add the summary line (with space for buttons on both sides)
        line_x = x + 5  # Small margin from toggle button
        line_width = width - 35  # Leave space for settings button
        Gumps.AddHtml(gd, line_x, current_y, line_width, 20, summary_line, False, False)

        return current_y + 25  # Return Y position after this line


class GumpInterface:
    """In-game GUMP interface for bot control and status display"""

    @staticmethod
    def create_status_gump():
        """Create and display the appropriate GUMP based on current state"""
        config = BotConfig()
        status = SystemStatus()

        try:
            # Close any existing GUMP to ensure clean state
            Gumps.CloseGump(config.GUMP_ID)

            # Determine which GUMP to create based on current state
            current_state = status.get_gump_state()

            if current_state == GumpState.CLOSED:
                # Don't create any GUMP
                return
            elif current_state == GumpState.MAIN_MINIMIZED or status.gump_minimized:
                GumpInterface.create_minimized_gump()
                status.set_gump_state(GumpState.MAIN_MINIMIZED)
            elif current_state == GumpState.BOT_SETTINGS:
                GumpInterface.create_bot_settings_gump()
            else:
                # Default to main GUMP (MAIN_FULL or unknown state)
                GumpInterface.create_main_gump_new()
                status.set_gump_state(GumpState.MAIN_FULL)

        except Exception as e:
            Logger.error(f"Error creating GUMP: {str(e)}")

    @staticmethod
    def create_main_gump_new():
        """Create the new modular main GUMP with system summary lines"""
        config = BotConfig()
        messages = BotMessages()
        status = SystemStatus()

        # Get current status information
        runtime_minutes = status.get_runtime_minutes()

        # Create GUMP using proper Razor Enhanced pattern
        gd = Gumps.CreateGump(movable=True)
        Gumps.AddPage(gd, 0)

        # Background
        Gumps.AddBackground(gd, 0, 0, config.GUMP_WIDTH, config.GUMP_HEIGHT, 30546)
        Gumps.AddAlphaRegion(gd, 0, 0, config.GUMP_WIDTH, config.GUMP_HEIGHT)

        # Add title at the top center of the gump
        Gumps.AddHtml(
            gd,
            70,
            5,
            config.GUMP_WIDTH - 20,
            25,
            f'<center><basefont color="#FFD700" size="5"><b>{messages.GUMP_TITLE}</b></basefont></center>',
            False,
            False,
        )

        # Window control buttons in upper right corner
        # Close Button
        close_button_x = config.GUMP_WIDTH - 40
        close_button_y = 5
        Gumps.AddButton(
            gd,
            close_button_x,
            close_button_y,
            config.BUTTON_CANCEL,
            config.BUTTON_CANCEL_PRESSED,
            4,
            1,
            0,
        )
        Gumps.AddTooltip(gd, "Close Interface")

        # Minimize Button
        minimize_button_x = config.GUMP_WIDTH - 70
        minimize_button_y = 5
        Gumps.AddButton(
            gd,
            minimize_button_x,
            minimize_button_y,
            config.BUTTON_MINIMIZE_NORMAL,
            config.BUTTON_MINIMIZE_PRESSED,
            3,
            1,
            0,
        )
        Gumps.AddTooltip(gd, "Minimize Interface")

        # Add online status and runtime just below the title
        Gumps.AddHtml(
            gd,
            80,
            30,
            config.GUMP_WIDTH - 20,
            20,
            f'<center><basefont color="#00FF00" size="3"><b>● {messages.GUMP_STATUS_ONLINE}</b></basefont> <basefont color="#CCCCCC" size="2">| Runtime: </basefont><basefont color="#FFFFFF" size="3"><b>{runtime_minutes}m</b></basefont></center>',
            False,
            False,
        )

        # System summary section
        section_x = 65  # Centered position for system lines
        section_width = config.GUMP_WIDTH - 130  # Leave space for buttons on both sides
        current_y = 65

        # Player Status Section (keep as-is for now)
        current_y = GumpSection.create_player_status_section(
            gd, section_x, current_y, section_width
        )
        current_y += 15  # Add spacing

        # Systems header
        Gumps.AddHtml(
            gd,
            section_x,
            current_y,
            section_width,
            20,
            f'<center><basefont color="#87CEEB" size="3"><b>SYSTEMS</b></basefont></center>',
            False,
            False,
        )
        current_y += 25

        # Auto Heal System Summary Line
        heal_status_text = "Healing..." if status.healing_active else "Ready"
        current_y = GumpSection.create_system_summary_line(
            gd,
            section_x,
            current_y,
            section_width,
            system_name="CORE BOT",
            enabled=config.HEALING_ENABLED,
            active=status.healing_active,
            status_text=heal_status_text,
            enable_button_id=1,  # Toggle Auto Heal
            settings_button_id=10,  # Open Bot Settings
        )

        # Debug Button - positioned in bottom left corner
        debug_button_x = 20
        debug_button_y = config.GUMP_HEIGHT - 35

        if config.DEBUG_MODE:
            Gumps.AddButton(
                gd,
                debug_button_x,
                debug_button_y,
                config.BUTTON_DEBUG_ENABLED,
                config.BUTTON_DEBUG_ENABLED_PRESSED,
                2,
                1,
                0,
            )
            debug_status = "ON"
            debug_color = "#00BFFF"
        else:
            Gumps.AddButton(
                gd,
                debug_button_x,
                debug_button_y,
                config.BUTTON_DEBUG_DISABLED,
                config.BUTTON_DEBUG_DISABLED_PRESSED,
                2,
                1,
                0,
            )
            debug_status = "OFF"
            debug_color = "#888888"
        Gumps.AddTooltip(gd, f"Toggle Debug Mode (Currently {debug_status})")

        # Debug button label
        debug_labels = f"""
        <basefont color="{debug_color}" size="2"><b>DEBUG</b></basefont><br>
        <basefont color="#CCCCCC" size="1">{debug_status}</basefont>
        """
        Gumps.AddHtml(
            gd, debug_button_x - 3, debug_button_y + 15, 60, 25, debug_labels, False, False
        )

        # Send the GUMP
        Gumps.SendGump(
            config.GUMP_ID,
            Player.Serial,
            config.GUMP_X,
            config.GUMP_Y,
            gd.gumpDefinition,
            gd.gumpStrings,
        )

        Logger.debug("New modular main GUMP created and displayed")

    @staticmethod
    def create_minimized_gump():
        """Create the minimized status GUMP"""
        config = BotConfig()

        # Create compact GUMP
        gd = Gumps.CreateGump(movable=True)
        Gumps.AddPage(gd, 0)

        # Background
        Gumps.AddBackground(gd, 0, 0, config.GUMP_MIN_WIDTH, config.GUMP_MIN_HEIGHT, 30546)
        Gumps.AddAlphaRegion(gd, 0, 0, config.GUMP_MIN_WIDTH, config.GUMP_MIN_HEIGHT)

        # Title in upper left corner
        Gumps.AddHtml(
            gd,
            5,
            5,
            65,
            20,
            f'<basefont color="#FFD700" size="3"><b>DexBot</b></basefont>',
            False,
            False,
        )

        # Expand button in upper right corner (no text label) - closer to title
        expand_button_x = config.GUMP_MIN_WIDTH - 22  # Closer to edge for tighter spacing
        expand_button_y = 5  # Top edge aligned with title
        Gumps.AddButton(
            gd,
            expand_button_x,
            expand_button_y,
            config.BUTTON_MAXIMIZE_NORMAL,
            config.BUTTON_MAXIMIZE_PRESSED,
            5,
            1,
            0,
        )
        Gumps.AddTooltip(gd, "Expand Interface")

        # Send the GUMP
        Gumps.SendGump(
            config.GUMP_ID,
            Player.Serial,
            config.GUMP_X,
            config.GUMP_Y,
            gd.gumpDefinition,
            gd.gumpStrings,
        )

        Logger.debug("Minimized status GUMP created and displayed")

    @staticmethod
    def create_bot_settings_gump():
        """Create the Bot Settings GUMP with detailed configuration options"""
        config = BotConfig()
        status = SystemStatus()

        # Create GUMP using proper Razor Enhanced pattern
        gd = Gumps.CreateGump(movable=True)
        Gumps.AddPage(gd, 0)

        # Background (slightly taller and wider for more options and longer text)
        settings_height = 300
        settings_width = 450  # Increased width to accommodate longer text
        Gumps.AddBackground(gd, 0, 0, settings_width, settings_height, 30546)
        Gumps.AddAlphaRegion(gd, 0, 0, settings_width, settings_height)

        # Title
        Gumps.AddHtml(
            gd,
            50,
            5,
            settings_width - 20,
            25,
            f'<center><basefont color="#FFD700" size="5"><b>BOT SETTINGS</b></basefont></center>',
            False,
            False,
        )

        # Back button in upper left corner
        back_button_x = 10
        back_button_y = 5
        Gumps.AddButton(
            gd,
            back_button_x,
            back_button_y,
            config.BUTTON_SETTINGS,
            config.BUTTON_SETTINGS_PRESSED,
            20,
            1,
            0,
        )  # Button ID 20 for back
        Gumps.AddTooltip(gd, "Back to Main GUMP")

        # Close Button in upper right corner
        close_button_x = settings_width - 30
        close_button_y = 5
        Gumps.AddButton(
            gd,
            close_button_x,
            close_button_y,
            config.BUTTON_CANCEL,
            config.BUTTON_CANCEL_PRESSED,
            4,
            1,
            0,
        )
        Gumps.AddTooltip(gd, "Close Interface")

        # Content area
        section_x = 20
        section_width = settings_width - 40
        current_y = 40

        # System Status Section
        system_status = "ENABLED" if config.HEALING_ENABLED else "DISABLED"
        system_color = "#00FF00" if config.HEALING_ENABLED else "#FF0000"
        status_text = "Healing..." if status.healing_active else "Ready"

        status_line = f'<basefont color="#87CEEB" size="3"><b>System Status:</b></basefont> <basefont color="{system_color}" size="3"><b>{system_status}</b></basefont>'
        if config.HEALING_ENABLED:
            status_line += f' <basefont color="#CCCCCC" size="2">({status_text})</basefont>'

        Gumps.AddHtml(gd, section_x, current_y, section_width, 20, status_line, False, False)
        current_y += 30

        # Healing Methods Section
        current_y = GumpSection.create_section(
            gd, "HEALING METHODS", section_x, current_y, section_width, title_color="#87CEEB"
        )
        current_y += 5

        # Bandage Healing Toggle
        bandage_toggle_x = section_x + 10
        bandage_toggle_y = current_y + 2
        if config.BANDAGE_HEALING_ENABLED:
            bandage_art = config.BUTTON_ENABLED
            bandage_pressed_art = config.BUTTON_ENABLED_PRESSED
            bandage_status = "ENABLED"
            bandage_color = "#00FF00"
        else:
            bandage_art = config.BUTTON_DISABLE
            bandage_pressed_art = config.BUTTON_DISABLE_PRESSED
            bandage_status = "DISABLED"
            bandage_color = "#FF0000"

        Gumps.AddButton(
            gd, bandage_toggle_x, bandage_toggle_y, bandage_art, bandage_pressed_art, 21, 1, 0
        )  # Button ID 21
        Gumps.AddTooltip(
            gd, f"Toggle Bandage Healing ({'ON' if config.BANDAGE_HEALING_ENABLED else 'OFF'})"
        )

        bandage_count = Items.FindByID(
            config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE
        )
        bandage_amount = bandage_count.Amount if bandage_count else 0
        bandage_line = f'<basefont color="#FFFFFF" size="3"><b>Bandage Healing:</b></basefont> <basefont color="{bandage_color}" size="2"><b>{bandage_status}</b></basefont> <basefont color="#CCCCCC" size="2">| Available: </basefont><basefont color="#FFFFFF" size="2"><b>{bandage_amount}</b></basefont> <basefont color="#CCCCCC" size="2">| Used: </basefont><basefont color="#FFFFFF" size="2"><b>{status.bandage_count}</b></basefont>'

        Gumps.AddHtml(
            gd, section_x + 50, current_y + 4, section_width - 50, 15, bandage_line, False, False
        )
        current_y += 25  # Original spacing restored

        # Potion Healing Toggle
        potion_toggle_x = section_x + 10
        potion_toggle_y = current_y + 2
        if config.POTION_HEALING_ENABLED:
            potion_art = config.BUTTON_ENABLED
            potion_pressed_art = config.BUTTON_ENABLED_PRESSED
            potion_status = "ENABLED"
            potion_color = "#00FF00"
        else:
            potion_art = config.BUTTON_DISABLE
            potion_pressed_art = config.BUTTON_DISABLE_PRESSED
            potion_status = "DISABLED"
            potion_color = "#FF0000"

        Gumps.AddButton(
            gd, potion_toggle_x, potion_toggle_y, potion_art, potion_pressed_art, 22, 1, 0
        )  # Button ID 22
        Gumps.AddTooltip(
            gd, f"Toggle Potion Healing ({'ON' if config.POTION_HEALING_ENABLED else 'OFF'})"
        )

        heal_potion_count = Items.FindByID(
            config.HEAL_POTION_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE
        )
        heal_potion_amount = heal_potion_count.Amount if heal_potion_count else 0
        potion_line = f'<basefont color="#FFFFFF" size="3"><b>Potion Healing:</b></basefont> <basefont color="{potion_color}" size="2"><b>{potion_status}</b></basefont> <basefont color="#CCCCCC" size="2">| Available: </basefont><basefont color="#FFFFFF" size="2"><b>{heal_potion_amount}</b></basefont> <basefont color="#CCCCCC" size="2">| Used: </basefont><basefont color="#FFFFFF" size="2"><b>{status.heal_potion_count}</b></basefont>'

        Gumps.AddHtml(
            gd, section_x + 50, current_y + 4, section_width - 50, 15, potion_line, False, False
        )
        current_y += 25

        # Add spacing between sections (same as between System Status and Healing Methods)
        current_y += 30

        # Health Thresholds Section
        current_y = GumpSection.create_section(
            gd,
            "HEALTH THRESHOLDS",
            section_x,
            current_y,
            section_width,
            content_lines=[
                {
                    "text": f'Healing Threshold: <basefont color="#FFFF00" size="3"><b>{config.HEALING_THRESHOLD_PERCENTAGE}%</b></basefont> <basefont color="#CCCCCC" size="2">(Start healing below this %)</basefont>',
                    "color": "#FFFFFF",
                },
                {
                    "text": f'Critical Health: <basefont color="#FF6B6B" size="3"><b>{config.CRITICAL_HEALTH_THRESHOLD}%</b></basefont> <basefont color="#CCCCCC" size="2">(Use potions for fast healing)</basefont>',
                    "color": "#FFFFFF",
                },
            ],
            title_color="#87CEEB",
        )

        # Send the GUMP
        Gumps.SendGump(
            config.GUMP_ID,
            Player.Serial,
            config.GUMP_X,
            config.GUMP_Y,
            gd.gumpDefinition,
            gd.gumpStrings,
        )

        Logger.debug("Bot Settings GUMP created and displayed")

    @staticmethod
    def handle_gump_response():
        """Handle player interactions with the GUMP"""
        config = BotConfig()
        status = SystemStatus()

        # Don't handle GUMP responses if it was manually closed
        if status.gump_closed:
            return False

        try:
            # Rate limiting: prevent rapid button presses (minimum 500ms between presses)
            current_time = time.time()
            if current_time - status.last_button_press_time < 0.5:
                return True  # Ignore rapid button presses

            # Check if our GUMP has a response
            gd = Gumps.GetGumpData(config.GUMP_ID)
            if gd and gd.buttonid > 0:
                button_pressed = gd.buttonid

                # Update last button press time
                status.last_button_press_time = current_time

                # Close and recreate the GUMP to clear the button press
                Gumps.CloseGump(config.GUMP_ID)

                if button_pressed == 1:  # Toggle Auto Heal (only in full GUMP)
                    config.HEALING_ENABLED = not config.HEALING_ENABLED
                    status_msg = "enabled" if config.HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Auto Heal system {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()

                elif button_pressed == 2:  # Toggle Debug Mode (only in full GUMP)
                    config.DEBUG_MODE = not config.DEBUG_MODE
                    status_msg = "enabled" if config.DEBUG_MODE else "disabled"
                    Logger.info(f"[DexBot] Debug mode {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()

                elif button_pressed == 3:  # Minimize GUMP (only in full GUMP)
                    status.gump_minimized = True
                    Logger.info("[DexBot] Status GUMP minimized")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()

                elif button_pressed == 4:  # Close GUMP (only in full GUMP)
                    status.gump_closed = True  # Mark GUMP as closed
                    status.set_gump_state(GumpState.CLOSED)  # Update state
                    Logger.info("[DexBot] Status GUMP closed")
                    return False  # Signal that GUMP was closed

                elif button_pressed == 5:  # Maximize GUMP (only in minimized GUMP)
                    status.gump_minimized = False
                    Logger.info("[DexBot] Status GUMP maximized")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()

                elif button_pressed == 7:  # Toggle Bandage Healing (only in full GUMP)
                    config.BANDAGE_HEALING_ENABLED = not config.BANDAGE_HEALING_ENABLED
                    status_msg = "enabled" if config.BANDAGE_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Bandage healing {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()

                elif button_pressed == 8:  # Toggle Potion Healing (only in full GUMP)
                    config.POTION_HEALING_ENABLED = not config.POTION_HEALING_ENABLED
                    status_msg = "enabled" if config.POTION_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Potion healing {status_msg} via GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Force update of displayed values and recreate GUMP
                    status.check_gump_data_changed()  # This will update the cached values
                    GumpInterface.create_status_gump()

                elif button_pressed == 10:  # Open Bot Settings GUMP
                    Logger.info("[DexBot] Opening Bot Settings")
                    status.set_gump_state(GumpState.BOT_SETTINGS)
                    GumpInterface.create_bot_settings_gump()

                elif button_pressed == 20:  # Back to Main GUMP (from Bot Settings)
                    Logger.info("[DexBot] Returning to main GUMP")
                    status.set_gump_state(GumpState.MAIN_FULL)
                    GumpInterface.create_status_gump()

                elif button_pressed == 21:  # Toggle Bandage Healing (in Bot Settings)
                    config.BANDAGE_HEALING_ENABLED = not config.BANDAGE_HEALING_ENABLED
                    status_msg = "enabled" if config.BANDAGE_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Bandage healing {status_msg} via Settings GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Recreate the Bot Settings GUMP to show updated state
                    GumpInterface.create_bot_settings_gump()

                elif button_pressed == 22:  # Toggle Potion Healing (in Bot Settings)
                    config.POTION_HEALING_ENABLED = not config.POTION_HEALING_ENABLED
                    status_msg = "enabled" if config.POTION_HEALING_ENABLED else "disabled"
                    Logger.info(f"[DexBot] Potion healing {status_msg} via Settings GUMP")
                    # Save settings to config file
                    if config.save_settings():
                        Logger.debug("[DexBot] Settings saved to config files")
                    # Recreate the Bot Settings GUMP to show updated state
                    GumpInterface.create_bot_settings_gump()

        except Exception as e:
            Logger.debug(f"GUMP response handling error: {str(e)}")

        return True  # GUMP is still active


def update_gump_system():
    """Update the GUMP system - handle responses and periodic updates with real-time health tracking"""
    config = BotConfig()
    status = SystemStatus()

    # Don't update GUMP system if it was manually closed
    if status.gump_closed:
        return

    # Handle any GUMP responses
    gump_active = GumpInterface.handle_gump_response()

    # Check if any displayed data has changed
    data_changed = status.check_gump_data_changed()

    # Update GUMP only if data has changed or on periodic intervals
    if gump_active:
        status.gump_update_counter += 1
        should_update = (
            status.gump_update_counter >= config.GUMP_UPDATE_INTERVAL_CYCLES or data_changed
        )

        if should_update and data_changed:
            # Only update if data actually changed
            GumpInterface.create_status_gump()
            status.gump_update_counter = 0
            Logger.debug("GUMP updated due to data changes")
        elif should_update and not data_changed:
            # Reset counter but don't update gump since no data changed
            status.gump_update_counter = 0
            Logger.debug("GUMP update skipped - no data changes")

    # Show console status every 20 cycles (~5 seconds) only when debug mode is enabled
    if config.DEBUG_MODE and status.gump_update_counter == 0 and status.runtime_cycles % 20 == 0:
        runtime_minutes = status.get_runtime_minutes()
        bandage_count = Items.FindByID(
            config.BANDAGE_ID, -1, Player.Backpack.Serial, config.SEARCH_RANGE
        )
        bandage_amount = bandage_count.Amount if bandage_count else 0
        health_percentage = (Player.Hits / Player.HitsMax) * 100 if Player.HitsMax > 0 else 0

        Logger.debug(
            f"[DexBot] Status - Health: {Player.Hits}/{Player.HitsMax} ({health_percentage:.0f}%) | Bandages: {bandage_amount} (Used: {status.bandage_count}) {'[ON]' if config.BANDAGE_HEALING_ENABLED else '[OFF]'} | Potions: (Used: {status.heal_potion_count}) {'[ON]' if config.POTION_HEALING_ENABLED else '[OFF]'} | Runtime: {runtime_minutes}min"
        )
