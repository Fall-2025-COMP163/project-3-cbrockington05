"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Cayden Brockington]

AI Usage: [used ChatGPT to help format save_character and load_character classes]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # Dictionary of classes and their stats
    valid_classes = {
        'Warrior': {'health': 120, 'strength': 15, 'magic': 5},
        'Mage': {'health': 80, 'strength': 8, 'magic': 20},
        'Rogue': {'health': 90, 'strength': 12, 'magic': 10},
        'Cleric': {'health': 100, 'strength': 10, 'magic': 15},
    }

    # Validating the classes
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class '{character_class}'. Valid: {list(valid_classes.keys())}")
    
    base = valid_classes[character_class]

    character = {
        'name': name,
        'class': character_class,
        'level': 1,
        'health': base['health'],
        'max_health': base['health'], 
        'strength': base['strength'],
        'magic': base['magic'],
        'experience': 0,
        'gold': 100,
        'inventory': [],
        'active_quests': [],
        'completed_quests': []
    }

    return character


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # Create directory if it doesn't exist already
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, 'w') as file:
             file.write(f"NAME: {character['name']}\n")
            file.write(f"CLASS: {character['class']}\n")
            file.write(f"LEVEL: {character['level']}\n")
            file.write(f"HEALTH: {character['health']}\n")
            file.write(f"MAX_HEALTH: {character['max_health']}\n")
            file.write(f"STRENGTH: {character['strength']}\n")
            file.write(f"MAGIC: {character['magic']}\n")
            file.write(f"EXPERIENCE: {character['experience']}\n")
            file.write(f"GOLD: {character['gold']}\n")
            file.write(f"INVENTORY: {','.join(character['inventory']) if character['inventory'] else ''}\n")
            file.write(f"ACTIVE_QUESTS: {','.join(character['active_quests']) if character['active_quests'] else ''}\n")
            file.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests']) if character['completed_quests'] else ''}\n")

    except Exception as e:
        raise e  

    return True

 
def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    filename = os.path.join(save_directory, f'{character_name}_save.txt')

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f'No save file found for {character_name}')

    # Read file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except:
        raise SaveFileCorruptedError('Could not read save file')

    character = {}

    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

             if ":" not in line:
                raise InvalidSaveDataError("Missing ':' in save data")
            
            if ": " in line:
                key, value = line.split(": ", 1)
            else:
                key, value = line.split(":", 1)
                value = value.lstrip()

            # Handling list fields
            if key in ['INVENTORY', 'ACTIVE_QUESTS', 'COMPLETED_QUESTS']:
                character[key.lower()] = value.split(',') if value else []
             # Convert from str to int
            elif key in ("LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"):
                character[key.lower()] = int(value)
            else:
                character[key.lower()] = value

        

        validate_character_data(character)
        return character

    except Exception as e:
        raise InvalidSaveDataError(f'Invalid save file data: {e}')


def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    if not os.path.exists(save_directory):
        return []

    names = []

    for filename in os.listdir(save_directory):
        if filename.endswith('_save.txt'): 
            characters.append(filename.replace('_save.txt', ''))

    return names


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    filename = os.path.join(save_directory, f'{character_name}_save.txt')

    # Verify file's existence
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f'Save file for {character_name} not found')

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # Can't gain xp if dead
    if character['health'] <= 0:
        raise CharacterDeadError('Dead characters cannot gain experience')

    character['experience'] += xp_amount
    leveled_up = False

    # Check if character levels up
    while character['experience'] >= character['level'] * 100:
        character['experience'] -= character['level'] * 100
        character['level'] += 1
        # Level up increases
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2
        # Heal to full health when leveling up
        character['health'] = character['max_health']
        leveled_up = True

    return leveled_up


def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    new_total = character['gold'] + amount

    if new_total < 0:
        raise ValueError('Not enough gold')

    character['gold'] = new_total
    return character['gold]


def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """

    if amount < 0:
        return 0
    
    before = character['health']
    character['health'] = min(character['health'] + amount, character['max_health'])
    return character['health'] - before


def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character['health'] <= 0  # FIXED: was 'haelth'


def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    if not is_character_dead(character):
        return False
        
    character['health'] = character['max_health'] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required = [
        'name', 'class', 'level', 'health', 
        'max_health', 'strength', 'magic', 'experience', 
        'gold', 'inventory', 'active_quests', 'completed_quests'
    ]

    # Check required keys
    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f'Missing key: {key}')

    # Check numeric fields
    numeric_fields = ['level', 'health', 'max_health', 'strength', 
                      'magic', 'experience', 'gold']
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f'Invalid type for {field}: expected int')

    # Check list fields
    list_fields = ['inventory', 'active_quests', 'completed_quests']
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f'{field} must be a list')

    return True
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")


