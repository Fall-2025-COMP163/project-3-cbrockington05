"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Cayden Brockignton]

AI Usage: [ChatGPT helped me code the loading classes and the a_files class]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f'quest file not found: {filename}')

    try:
        with open(filename, 'r') as file:
            data = file.read()
    except Exception as e:
        raise CorruptedDataError(f'Could not read quest file: {e}')

    # Split by blank lines
    blocks = [b.strip() for b in data.split('\n\n') if b.strip()]

    quest_dict = {}  

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        try:
            q = parse_quest_block(lines)
        except InvalidDataFormatError as e:
            # for debugging
            raise InvalidDataFormatError(f"Invalid quest block: {e}")

        quest_id = q["quest_id"]
        if quest_id in quests:
            raise InvalidDataFormatError(f"Duplicate quest id '{quest_id}' in file.")
        quests[quest_id] = q

    return quest_dict 
    

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f'Item file not found: {filename}')

    try:
        with open(filename, 'r') as file:
            data = file.read()
    except Exception as e:
        raise CorruptedDataError(f'could not read item file: {e}')

    blocks = [b.strip() for b in data.split('\n\n') if b.strip()]
    item_dict = {}

    for block in blocks:
        for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        try:
            itm = parse_item_block(lines)
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"Invalid item block: {e}")

        item_id = itm["item_id"]
        if item_id in items:
            raise InvalidDataFormatError(f"Duplicate item id '{item_id}' in file.")
        items[item_id] = itm

    return items


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required = [
        'quest_id', 'title', 'description',
        'reward_xp', 'reward_gold',
        'required_level', 'prerequisite'
    ]

    # Make sure all fields are present
    for field in required:
        if field not in quest_dict:
            raise InvalidDataFormatError(f'missing quest field: {field}')

    # Validate numeric values
    numeric_fields = ['reward_xp', 'reward_gold', 'required_level']

    for field in numeric_fields:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f'field {field} must be an integer')

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required = ['item_id', 'name', 'type', 'effect', 'cost', 'description']

    missing = required - set(item_dict.keys())
    if missing:
        raise InvalidDataFormatError(f"Missing item fields: {', '.join(sorted(missing))}")

    if item_dict["type"] not in ("weapon", "armor", "consumable"):
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    # cost must be int
    if not isinstance(item_dict.get("cost"), int):
        raise InvalidDataFormatError("Item field 'cost' must be an integer.")

    # value should be int
    eff = item_dict["effect"]
    if ":" not in eff:
        raise InvalidDataFormatError("Item 'effect' must use format 'stat:value'.")

    stat, val = eff.split(":", 1)
    stat = stat.strip()
    val = val.strip()
    if not stat or not val:
        raise InvalidDataFormatError("Item 'effect' must contain both stat and value.")
    try:
        int(val)
    except ValueError:
        raise InvalidDataFormatError("Item effect value must be an integer.")

    return True


def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    data_dir = "data"
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir, exist_ok=True)
        except Exception as e:
            raise CorruptedDataError(f"Could not create data directory: {e}")

    quests_path = os.path.join(data_dir, "quests.txt")
    items_path = os.path.join(data_dir, "items.txt")

    # Only create if not exists; do not overwrite existing files.
    if not os.path.exists(quests_path):
        default_quests = """QUEST_ID: first_quest
TITLE: First Steps
DESCRIPTION: Prove yourself by completing this simple task.
REWARD_XP: 50
REWARD_GOLD: 25
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: goblin_menace
TITLE: Goblin Menace
DESCRIPTION: Clear out the goblins troubling the nearby farms.
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 2
PREREQUISITE: first_quest
"""
        try:
            with open(quests_path, "w", encoding="utf-8") as f:
                f.write(default_quests)
        except Exception as e:
            raise CorruptedDataError(f"Could not create default quests file: {e}")

    if not os.path.exists(items_path):
        default_items = """ITEM_ID: health_potion
NAME: Health Potion
TYPE: consumable
EFFECT: health:30
COST: 25
DESCRIPTION: Restores a moderate amount of health.

ITEM_ID: iron_sword
NAME: Iron Sword
TYPE: weapon
EFFECT: strength:5
COST: 100
DESCRIPTION: A basic sword that increases strength.

ITEM_ID: leather_armor
NAME: Leather Armor
TYPE: armor
EFFECT: max_health:10
COST: 80
DESCRIPTION: Basic armor that increases maximum health.
"""
        try:
            with open(items_path, "w", encoding="utf-8") as f:
                f.write(default_items)
        except Exception as e:
            raise CorruptedDataError(f"Could not create default items file: {e}")

    return True


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest = {}

    try:
        for line in lines:
            if ':' not in line:  # Skip invalid lines
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            # Convert numeric fields to integers
            if key in ['reward_xp', 'reward_gold', 'required_level']:
                value = int(value)

            # Handle NONE prerequisite
            if key == 'prerequisite' and value.upper() == 'NONE':
                value = 'NONE'  # FIXED: Keep as string 'NONE', not None

            quest[key] = value

        # Ensure quest_id exists
        if 'quest_id' not in quest:
            raise InvalidDataFormatError('quest_id is required')

    except ValueError as e:  # FIXED: Added specific exception
        raise InvalidDataFormatError(f'invalid quest formatting: {e}')
    except Exception as e:
        raise InvalidDataFormatError(f'invalid quest formatting: {e}')

    return quest


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}

    try:
        for line in lines:
            if ':' not in line:  # Skip invalid lines
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            # Convert cost to int
            if key == 'cost':
                value = int(value)

            # Parse effect (format: stat:amount)
            if key == 'effect':
                if ':' in value:
                    stat, amount = value.split(':', 1)
                    stat = stat.strip()
                    amount = amount.strip()
                    # Store as string for compatibility
                    value = f"{stat}:{amount}"
                # Keep the original string format for now

            item[key] = value

        # Ensure item_id exists
        if 'item_id' not in item:
            raise InvalidDataFormatError('item_id is required')

    except ValueError as e:  # FIXED: Added specific exception
        raise InvalidDataFormatError(f'invalid item formatting: {e}')
    except Exception as e:
        raise InvalidDataFormatError(f'invalid item formatting: {e}')

    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

