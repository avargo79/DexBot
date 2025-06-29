"""
Centralized import file for RazorEnhanced API
Provides a single location for all RazorEnhanced API imports
"""

# RazorEnhanced API imports - these are available when running inside RazorEnhanced
try:
    import Gumps
    import Items
    import Journal
    import Misc
    import Mobiles

    # These imports are available in the RazorEnhanced environment
    # Import stubs to avoid IDE errors, but the actual implementation comes from RazorEnhanced
    import Player
    import Target
    import Timer
    from AutoComplete import *

    # Core API imports
    from System import *

except ImportError:
    # For development/testing outside RazorEnhanced environment
    # Create mock objects to avoid import errors
    class MockPlayer:
        Hits = 100
        HitsMax = 100
        Connected = True
        IsGhost = False
        Visible = True
        Poisoned = False
        Serial = 123456

        class Backpack:
            Serial = 654321

    class MockItems:
        @staticmethod
        def FindByID(item_id, color=-1, container=None, search_range=2):
            # Mock return with an amount property
            class MockItem:
                Amount = 10
                Serial = 789123

            return MockItem()

        @staticmethod
        def UseItemByID(item_id, color=-1):
            pass

    class MockTimer:
        @staticmethod
        def Check(timer_name):
            return True

        @staticmethod
        def Create(timer_name, duration):
            pass

    class MockJournal:
        @staticmethod
        def SearchByType(message, message_type):
            return False

        @staticmethod
        def Clear():
            pass

    class MockTarget:
        @staticmethod
        def WaitForTarget(timeout):
            pass

        @staticmethod
        def Self():
            pass

    class MockMisc:
        @staticmethod
        def Pause(duration):
            import time

            time.sleep(duration / 1000.0)  # Convert ms to seconds

    class MockGumps:
        @staticmethod
        def CreateGump(movable=True):
            class MockGumpDefinition:
                gumpDefinition = ""
                gumpStrings = []

            return MockGumpDefinition()

        @staticmethod
        def AddPage(gd, page):
            pass

        @staticmethod
        def AddBackground(gd, x, y, width, height, gump_id):
            pass

        @staticmethod
        def AddAlphaRegion(gd, x, y, width, height):
            pass

        @staticmethod
        def AddHtml(gd, x, y, width, height, html, bg, scrollbar):
            pass

        @staticmethod
        def AddButton(gd, x, y, normal_id, pressed_id, button_id, type_val, param):
            pass

        @staticmethod
        def AddTooltip(gd, text):
            pass

        @staticmethod
        def SendGump(gump_id, serial, x, y, gump_def, gump_strings):
            pass

        @staticmethod
        def CloseGump(gump_id):
            pass

        @staticmethod
        def GetGumpData(gump_id):
            class MockGumpData:
                buttonid = 0

            return MockGumpData()

    class MockMobiles:
        @staticmethod
        def Filter():
            # Return empty list for development
            return []

        @staticmethod
        def FindBySerial(serial):
            # Mock mobile object
            class MockMobile:
                Serial = serial
                Name = "TestMobile"
                Hits = 100
                HitsMax = 100
                Notoriety = 3  # Gray
                Position = type('Position', (), {'X': 100, 'Y': 100, 'Z': 0})()

            return MockMobile()

    # Assign mock objects
    Player = MockPlayer()
    Items = MockItems()
    Timer = MockTimer()
    Journal = MockJournal()
    Target = MockTarget()
    Misc = MockMisc()
    Gumps = MockGumps()
    Mobiles = MockMobiles()
