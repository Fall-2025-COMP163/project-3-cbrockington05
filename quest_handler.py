"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Cayden Brockington]

AI Usage: [Used ChatGPT to help format accept quest, complete quest, and display classes]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # Initialize lists if they don't exist
    if 'active_quests' not in character:
        character['active_quests'] = []
    if 'completed_quests' not in character:
        character['completed_quests'] = []
    
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    quest = quest_data_dict[quest_id]
    
    # Check not already completed
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed")
    
    # Check not already active
    if quest_id in character['active_quests']:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already active")
    
    # Check level requirement
    if character['level'] < quest['required_level']:
        raise InsufficientLevelError(
            f"Level {quest['required_level']} required (you are level {character['level']})"
        )
    
    # Check prerequisite (if not "NONE")
    prerequisite = quest.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        if prerequisite not in character['completed_quests']:
            raise QuestRequirementsNotMetError(
                f"Must complete '{prerequisite}' first"
            )
    
    # Add to active quests
    character['active_quests'].append(quest_id)
    
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    # Check quest is active
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active")
    
    quest = quest_data_dict[quest_id]
    
    # Remove from active quests
    character['active_quests'].remove(quest_id)
    
    # Add to completed quests
    if 'completed_quests' not in character:
        character['completed_quests'] = []
    character['completed_quests'].append(quest_id)
    
    # Grant rewards
    reward_xp = quest.get('reward_xp', 0)
    reward_gold = quest.get('reward_gold', 0)
    
    # Add XP (use gain_experience if available, otherwise add directly)
    try:
        import character_manager
        character_manager.gain_experience(character, reward_xp)
    except:
        character['experience'] = character.get('experience', 0) + reward_xp
    
    # Add gold
    character['gold'] = character.get('gold', 0) + reward_gold
    
    # Return reward summary
    return {
        'quest_id': quest_id,
        'xp_gained': reward_xp,
        'gold_gained': reward_gold
    }


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active")
    
    character['active_quests'].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    active_quest_ids = character.get('active_quests', [])
    active_quests = []
    
    for quest_id in active_quest_ids:
        if quest_id in quest_data_dict:
            active_quests.append(quest_data_dict[quest_id])
    
    return active_quests


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    completed_quest_ids = character.get('completed_quests', [])
    completed_quests = []
    
    for quest_id in completed_quest_ids:
        if quest_id in quest_data_dict:
            completed_quests.append(quest_data_dict[quest_id])
    
    return completed_quests


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    available_quests = []
    
    for quest_id, quest in quest_data_dict.items():
        if can_accept_quest(character, quest_id, quest_data_dict):
            available_quests.append(quest)
    
    return available_quests


# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    return quest_id in character.get('completed_quests', [])


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    return quest_id in character.get('active_quests', [])


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # Check quest exists
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
    
    # Check not already completed
    if is_quest_completed(character, quest_id):
        return False
    
    # Check not already active
    if is_quest_active(character, quest_id):
        return False
    
    # Check level requirement
    if character['level'] < quest['required_level']:
        return False
    
    # Check prerequisite
    prerequisite = quest.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        if not is_quest_completed(character, prerequisite):
            return False
    
    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    chain = []
    current_quest_id = quest_id
    
    # Follow prerequisites backwards
    while current_quest_id is not None:
        chain.insert(0, current_quest_id)  # Insert at beginning
        
        quest = quest_data_dict[current_quest_id]
        prerequisite = quest.get('prerequisite', 'NONE')
        
        if prerequisite == 'NONE':
            break
        
        if prerequisite not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite '{prerequisite}' not found")
        
        current_quest_id = prerequisite
    
    return chain


# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total_quests = len(quest_data_dict)
    
    if total_quests == 0:
        return 0.0
    
    completed_quests = len(character.get('completed_quests', []))
    percentage = (completed_quests / total_quests) * 100
    
    return round(percentage, 2)


def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0
    
    completed_quest_ids = character.get('completed_quests', [])
    
    for quest_id in completed_quest_ids:
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest.get('reward_xp', 0)
            total_gold += quest.get('reward_gold', 0)
    
    return {
        'total_xp': total_xp,
        'total_gold': total_gold
    }


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    quests_in_range = []
    
    for quest_id, quest in quest_data_dict.items():
        required_level = quest.get('required_level', 1)
        if min_level <= required_level <= max_level:
            quests_in_range.append(quest)
    
    return quests_in_range


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data.get('required_level', 1)}")
    
    prerequisite = quest_data.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        print(f"Prerequisite: {prerequisite}")
    
    print(f"\nRewards:")
    print(f"  - XP: {quest_data.get('reward_xp', 0)}")
    print(f"  - Gold: {quest_data.get('reward_gold', 0)}")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    if not quest_list:
        print("No quests available.")
        return
    
    print("\n" + "=" * 70)
    print(f"{'Quest Title':<30} {'Level':<8} {'XP':<8} {'Gold':<8}")
    print("=" * 70)
    
    for quest in quest_list:
        title = quest.get('title', 'Unknown')[:29]
        level = quest.get('required_level', 1)
        xp = quest.get('reward_xp', 0)
        gold = quest.get('reward_gold', 0)
        
        print(f"{title:<30} {level:<8} {xp:<8} {gold:<8}")
    
    print("=" * 70)


def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    print("\n=== QUEST PROGRESS ===")
    
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    total_count = len(quest_data_dict)
    
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count} / {total_count}")
    
    completion_pct = get_quest_completion_percentage(character, quest_data_dict)
    print(f"Completion: {completion_pct}%")
    
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    print(f"\nTotal Rewards Earned:")
    print(f"  - XP: {rewards['total_xp']}")
    print(f"  - Gold: {rewards['total_gold']}")


# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for quest_id, quest in quest_data_dict.items():
        prerequisite = quest.get('prerequisite', 'NONE')
        
        if prerequisite != 'NONE':
            if prerequisite not in quest_data_dict:
                raise QuestNotFoundError(
                    f"Quest '{quest_id}' has invalid prerequisite '{prerequisite}'"
                )
    
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

