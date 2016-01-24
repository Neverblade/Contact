import random


class Contact:

    # Game States
    IDLE = 'IDLE'  # Game has yet to start. (no picked King).
    STANDBY = 'STANDBY'  # Game has started, but waiting on King to lock in word choice.
    WAITING = 'WAITING'  # Game was ACTIVE or STANDBY, but challengers left (not enough people).
    ACTIVE = 'ACTIVE'  # Game has started.

    # Special Messages
    GAME_END = "THE GAME HAS ENDED. THIS MESSAGE SHOULD NEVER BE SEEN."

    """
    CONSTRUCTOR
    Creates an empty list of players, sets running state to off. (Add more as needed)
    """
    def __init__(self):
        self.players = []  # The players currently in the game.
        self.word = ''  # The mystery word the challengers are trying to find.
        self.layer = 0  # How much of the word is currently revealed.
        self.seen_words = set()  # What words have already been said before
        self.game_state = Contact.IDLE  # The state of the game.
        self.messages = []  # All messages the server needs to display.

    """
    The substring of the word that's currently revealed to challengers.
    """
    @property
    def revealed(self):
        return self.word[0:self.layer]

    """
    The number of players in the game.
    """
    @property
    def num_players(self):
        return len(self.players)

    """
    Initializes the game.
    A game can only be initialized from the IDLE state (moves to STANDBY).
    """
    def init_game(self):
        self.manual_init_game(random.choice(self.players))

    """
    Initializes the game, with manual King selection.
    """
    def manual_init_game(self, king):
        assert self.game_state == Contact.IDLE
        king.position = Player.KING
        self.add_message(king.name + " was made the king.")
        self.add_message("Waiting for the king to choose a word.")
        self.game_state = Contact.STANDBY

    """
    Starts the game.
    Takes the king's word and locks it in, then sets the reveal and layer.
    A game can only be started from a STANDBY mode.
    """
    def start_game(self):
        assert self.game_state == Contact.STANDBY
        king = self.find_king()
        self.word = king.word
        self.layer = 1
        self.game_state = Contact.ACTIVE
        self.clear_words()

    """
    Clears the game, readying it to be played.
    Puts the game into the IDLE position.
    """
    def clear_game(self):
        self.word = ''
        self.seen_words = set()
        self.layer = 0
        for player in self.players:
            player.word = ''
            player.position = Player.CHALLENGER
        self.game_state = Contact.IDLE

    """
    Advances the game, increasing the layer and clearing words.
    Only works in ACTIVE mode.
    """
    def advance_game(self):
        print(self.game_state)
        assert self.game_state == Contact.ACTIVE
        self.layer += 1
        self.clear_words()

    """
    Clears all the player's words.
    Works only in ACTIVE mode.
    """
    def clear_words(self):
        assert self.game_state == Contact.ACTIVE
        for player in self.players:
            player.word = ''

    """
    PUBLIC
    Creates and adds a player with the given name to the list of players.
    Fails if the name already exists.
        NAME: string
    """
    def add_player(self, name):
        self.players.append(Player(name))
        self.add_message(name + " has joined the game.")
        if self.num_players == 3:  # Enough players to start (with not enough before)
            if self.game_state == Contact.IDLE:
                self.init_game()
            else:  # Game must be in WAITING
                assert self.game_state == Contact.WAITING
                self.add_message("Resuming play.")
                if self.word == '':
                    self.game_state = Contact.STANDBY
                    self.add_message("Waiting for the king to choose a word.")
                else:
                    self.game_state = Contact.ACTIVE

    """
    PUBLIC
    Removes a player with the given name.
    Fails if the name doesn't exist.
        NAME: string
    """
    def remove_player(self, name):
        player = self.find_player(name)
        self.players.remove(player)
        self.add_message(name + " left the game.")
        if player.position == Player.KING:
            self.clear_game()
            self.add_message("The king has left. Restarting the game.")
            if self.num_players >= 3:  # Still have enough people to play
                self.init_game()
        elif self.num_players == 2:  # A challenger is removed and we now don't have enough people
                self.game_state = Contact.WAITING
                self.add_message("Waiting for enough challengers.")

    """
    PUBLIC
    Processes behavior for when a player locks in a word.
    If King, (only in STANDBY), move to either ACTIVE or WAITING.
    If Challenger (only allowed in ACTIVE), compare words and check for
    advancement or win conditions.
        NAME: String
        WORD: String
    Returns; Either "" or a string detailing what went wrong.
    """
    def submit_word(self, name, word):
        word = word.upper()
        player = self.find_player(name)
        if not player:
            return "Player not found. No one should every see this text."
        if player.position == Player.KING:
            if self.game_state == Contact.STANDBY:
                player.word = word
                self.start_game()
                self.add_message("The king has selected a word. Game start!")
            elif self.game_state == Contact.ACTIVE:
                validity = self.valid_word(word)
                if validity == -1:
                    return "Not a valid word."
                elif validity == 0:
                    return "Word was used before."
                elif word == self.word:
                    return "Can't lock the secret word!"
                player.word = word
                for other_player in self.players:
                    if other_player != player and other_player.word == word:
                        self.add_message("The king has locked down " + word + ". Sorry " + other_player.name + "!")
                        self.seen_words.add(word)
                        self.clear_words()
                        return ""
            return ""
        else:  # Challenger
            validity = self.valid_word(word)
            if validity == -1:
                return "Not a valid word."
            elif validity == 0:
                return "Word was used before."
            assert self.game_state == Contact.ACTIVE
            player.word = word
            for other_player in self.players:
                if other_player != player and other_player.word == player.word:
                    if other_player.position == Player.KING:  # They locked themselves!
                        self.add_message(player.name + " guessed a word trapped by the king! Sorry " + player.name + "!")
                        self.seen_words.add(word)
                        self.clear_words()
                        return ""
                    else:  # Contact with another player
                        self.add_message("Contact! " + other_player.name + " and " + player.name
                                         + " advance the game with the word \"" + word + "\".")
                        king = self.find_king()
                        if king.word == word:  # The King's word was guessed through Contact!
                            self.add_message(other_player.name + " has overthrown the king!")
                            self.add_message("The word was \"" + word + "\".")
                            self.clear_game()
                            self.manual_init_game(other_player)
                            return ""
                        else:  # Advance regularly, check for exhaustion win condition
                            self.seen_words.add(word)
                            self.advance_game()
                            if self.revealed == self.word:
                                self.add_message("The full word was revealed! It was \"" + self.word + "\".")
                                self.clear_game()
                                self.manual_init_game(other_player)
                            return ""
            return ""

    """
    UTILITY
    Returns the player with the given name.
        NAME: String
    Returns: Player object with the given name, None if it doesn't exist.
    """
    def find_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    """
    UTILITY
    Finds and returns the King.
    Returns: Player object that has the King position, None if it doesn't exist.
    """
    def find_king(self):
        for player in self.players:
            if player.position == Player.KING:
                return player
        return None

    """
    UTILITY
    Checks the given word for whether it fits the current revealed status.
    If the current revealed word is "", then nothing is valid.
        WORD: String
    Returns: -1 for a bad word, 0 for a word seen before, and 1 for a good word
    """
    def valid_word(self, word):
        if self.revealed == "" or len(word) < self.layer or word[:self.layer] != self.revealed:
            return -1
        if word in self.seen_words:
            return 0
        return 1

    """
    DEBUGGING, PUBLIC
    Outputs the current state of the game, including:
        Game state, hidden word, visible word, players, seen words.
    """
    def print_state(self):
        print("=== Current Game Status ===")
        print("Current State: " + self.game_state)
        print("Hidden Word: " + self.word)
        print("Revealed Word: " + self.revealed)
        print("== " + str(len(self.players)) + " Players ==")
        for player in self.players:
            print("    " + player.name + ":")
            print("        " + "Position: " + player.position)
            print("        " + "Word: " + player.word)
        print("== " + str(len(self.seen_words)) + " Seen Words ==")
        for word in self.seen_words:
            print("    " + word)
        print("===========================")

    """
    PUBLIC
    Returns true if the messages list contains messages.
    """
    def has_messages(self):
        return len(self.messages) != 0

    """
    PUBLIC
    Reads a message by removing the first one from the list and returning it.
    """
    def read_message(self):
        message = self.messages[0]
        del self.messages[0]
        return message

    """
    Adds the given message to the end of the messages list.
        MESSAGE: String
    """
    def add_message(self, message):
        self.messages.append(message)


class Player:

    KING = 'King'
    CHALLENGER = 'Challenger'

    """
    Constructor. Initializes the name, whether or not they're king or a challenger, and a var for their Word.
    """
    def __init__(self, name, position=CHALLENGER):
        self.name = name
        self.position = position
        self.word = ''