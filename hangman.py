#!/usr/bin/env python3

"""
Python Hangman

A colorful terminal-based version of the classic Hangman game.

Author: Debi Majumdar
"""

from pathlib import Path
from random import choice
from typing import Final


# ANSI terminal colors
RESET: Final = "\033[0m"
BOLD: Final = "\033[1m"
RED: Final = "\033[91m"
GREEN: Final = "\033[92m"
YELLOW: Final = "\033[93m"
BLUE: Final = "\033[94m"
MAGENTA: Final = "\033[95m"
CYAN: Final = "\033[96m"


HANGMAN_STAGES: Final = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """,
]


BUILT_IN_WORDS: Final = {
    "easy": [
        "apple",
        "beach",
        "cloud",
        "dance",
        "dream",
        "flame",
        "grape",
        "house",
        "music",
        "ocean",
        "panda",
        "plant",
        "smile",
        "tiger",
        "water",
    ],
    "medium": [
        "adventure",
        "butterfly",
        "computer",
        "dinosaur",
        "elephant",
        "festival",
        "galaxy",
        "hospital",
        "keyboard",
        "mountain",
        "penguin",
        "rainbow",
        "sandwich",
        "telescope",
    ],
    "hard": [
        "archaeology",
        "biodiversity",
        "cryptography",
        "electromagnetic",
        "extraordinary",
        "photosynthesis",
        "quintessential",
        "revolutionary",
        "subterranean",
        "transformation",
    ],
}


DIFFICULTIES: Final = {
    "1": ("easy", 8),
    "2": ("medium", 6),
    "3": ("hard", 5),
}


def clear_screen() -> None:
    """Clear the terminal using ANSI escape codes."""

    print("\033[2J\033[H", end="")


def print_title() -> None:
    """Display the game title."""

    print(
        f"""{CYAN}{BOLD}
╔══════════════════════════════════╗
║          PYTHON HANGMAN          ║
╚══════════════════════════════════╝
{RESET}"""
    )


def normalize_word(word: str) -> str:
    """Return a cleaned lowercase word containing letters or hyphens."""

    return "".join(
        character.lower()
        for character in word.strip()
        if character.isalpha() or character == "-"
    )


def load_external_words(filename: str = "dictionary-short.txt") -> list[str]:
    """
    Load valid words from an optional local dictionary file.

    The built-in word collection is used when the file does not exist.
    """

    path = Path(filename)

    if not path.exists():
        return []

    try:
        words = {
            normalize_word(line)
            for line in path.read_text(encoding="utf-8").splitlines()
        }

        return sorted(
            word
            for word in words
            if len(word.replace("-", "")) >= 3
        )
    except OSError:
        return []


def words_for_difficulty(difficulty: str) -> list[str]:
    """Return suitable words for the selected difficulty."""

    external_words = load_external_words()

    if difficulty == "easy":
        filtered = [
            word
            for word in external_words
            if 3 <= len(word.replace("-", "")) <= 6
        ]
    elif difficulty == "medium":
        filtered = [
            word
            for word in external_words
            if 7 <= len(word.replace("-", "")) <= 9
        ]
    else:
        filtered = [
            word
            for word in external_words
            if len(word.replace("-", "")) >= 10
        ]

    return filtered or BUILT_IN_WORDS[difficulty]


def choose_difficulty() -> tuple[str, int]:
    """Prompt the player to select a difficulty."""

    print(f"{BOLD}Choose a difficulty:{RESET}")
    print(f"  {GREEN}1. Easy{RESET}   — shorter words, 8 lives")
    print(f"  {YELLOW}2. Medium{RESET} — medium words, 6 lives")
    print(f"  {RED}3. Hard{RESET}   — longer words, 5 lives")

    while True:
        selection = input(f"\n{CYAN}> {RESET}").strip()

        if selection in DIFFICULTIES:
            return DIFFICULTIES[selection]

        print(f"{RED}Please enter 1, 2, or 3.{RESET}")


def display_word(word: str, guessed_letters: set[str]) -> str:
    """Return the partially revealed word."""

    characters = []

    for character in word:
        if character == "-":
            characters.append("-")
        elif character in guessed_letters:
            characters.append(character.upper())
        else:
            characters.append("_")

    return " ".join(characters)


def is_word_complete(word: str, guessed_letters: set[str]) -> bool:
    """Return whether every letter in the word has been guessed."""

    return all(
        character == "-" or character in guessed_letters
        for character in word
    )


def available_hint_letters(
    word: str,
    guessed_letters: set[str],
) -> list[str]:
    """Return unguessed letters that appear in the word."""

    return sorted(
        {
            character
            for character in word
            if character.isalpha() and character not in guessed_letters
        }
    )


def print_game_status(
    word: str,
    guessed_letters: set[str],
    wrong_guesses: set[str],
    lives_remaining: int,
    max_lives: int,
    difficulty: str,
) -> None:
    """Display the current game state."""

    stage_index = min(max_lives - lives_remaining, len(HANGMAN_STAGES) - 1)

    print(f"{MAGENTA}{HANGMAN_STAGES[stage_index]}{RESET}")
    print(f"{BOLD}Difficulty:{RESET} {difficulty.title()}")
    print(f"{BOLD}Word:{RESET} {CYAN}{display_word(word, guessed_letters)}{RESET}")
    print(
        f"{BOLD}Lives:{RESET} "
        f"{GREEN if lives_remaining > 2 else RED}"
        f"{'♥ ' * lives_remaining}{RESET}"
    )

    if wrong_guesses:
        print(
            f"{BOLD}Incorrect guesses:{RESET} "
            f"{RED}{', '.join(sorted(letter.upper() for letter in wrong_guesses))}"
            f"{RESET}"
        )
    else:
        print(f"{BOLD}Incorrect guesses:{RESET} None")

    print(
        f"\nEnter a {BOLD}letter{RESET}, the {BOLD}full word{RESET}, "
        f"or type {YELLOW}hint{RESET}."
    )


def get_guess(
    guessed_letters: set[str],
    word: str,
) -> tuple[str, str]:
    """
    Collect and validate the player's guess.

    Returns a tuple containing the guess type and value.
    """

    while True:
        guess = input(f"{CYAN}> {RESET}").strip().lower()

        if not guess:
            print(f"{RED}Please enter a guess.{RESET}")
            continue

        if guess == "hint":
            return "hint", guess

        normalized_guess = normalize_word(guess)

        if len(normalized_guess) == 1:
            if normalized_guess in guessed_letters:
                print(
                    f"{YELLOW}You already guessed "
                    f"{normalized_guess.upper()}.{RESET}"
                )
                continue

            return "letter", normalized_guess

        if normalized_guess == word or normalized_guess.isalpha():
            return "word", normalized_guess

        print(f"{RED}Please enter letters only.{RESET}")


def play_round(
    difficulty: str,
    max_lives: int,
) -> tuple[bool, str]:
    """Play one round and return whether the player won and the word."""

    word = choice(words_for_difficulty(difficulty)).lower()
    guessed_letters: set[str] = set()
    wrong_guesses: set[str] = set()
    lives_remaining = max_lives
    hints_remaining = 1

    while lives_remaining > 0:
        clear_screen()
        print_title()
        print_game_status(
            word,
            guessed_letters,
            wrong_guesses,
            lives_remaining,
            max_lives,
            difficulty,
        )

        guess_type, guess = get_guess(guessed_letters, word)

        if guess_type == "hint":
            if hints_remaining == 0:
                print(f"{YELLOW}You have already used your hint.{RESET}")
                input("\nPress Enter to continue...")
                continue

            hint_letters = available_hint_letters(word, guessed_letters)

            if hint_letters:
                revealed_letter = choice(hint_letters)
                guessed_letters.add(revealed_letter)
                hints_remaining -= 1
                print(
                    f"{YELLOW}Hint: the word contains "
                    f"'{revealed_letter.upper()}'.{RESET}"
                )
                input("\nPress Enter to continue...")

        elif guess_type == "word":
            if guess == word:
                guessed_letters.update(
                    character for character in word if character.isalpha()
                )
            else:
                lives_remaining -= 1
                print(f"{RED}That is not the word. You lost one life.{RESET}")
                input("\nPress Enter to continue...")

        elif guess in word:
            guessed_letters.add(guess)
            print(f"{GREEN}Correct!{RESET}")
            input("\nPress Enter to continue...")

        else:
            guessed_letters.add(guess)
            wrong_guesses.add(guess)
            lives_remaining -= 1
            print(f"{RED}Incorrect. You lost one life.{RESET}")
            input("\nPress Enter to continue...")

        if is_word_complete(word, guessed_letters):
            clear_screen()
            print_title()
            print_game_status(
                word,
                guessed_letters,
                wrong_guesses,
                lives_remaining,
                max_lives,
                difficulty,
            )
            print(
                f"\n{GREEN}{BOLD}You won! "
                f"The word was {word.upper()}.{RESET}"
            )
            return True, word

    clear_screen()
    print_title()
    print_game_status(
        word,
        guessed_letters,
        wrong_guesses,
        lives_remaining,
        max_lives,
        difficulty,
    )
    print(
        f"\n{RED}{BOLD}Game over! "
        f"The word was {word.upper()}.{RESET}"
    )
    return False, word


def ask_to_play_again() -> bool:
    """Ask whether the player wants another round."""

    while True:
        response = input(
            f"\nWould you like to play again? "
            f"{BOLD}[Y/N]{RESET} "
        ).strip().lower()

        if response in {"y", "yes"}:
            return True

        if response in {"n", "no"}:
            return False

        print(f"{RED}Please enter Y or N.{RESET}")


def main() -> None:
    """Run the Hangman application."""

    wins = 0
    losses = 0
    current_streak = 0
    best_streak = 0

    clear_screen()
    print_title()
    print("Guess the hidden word before the hangman is completed.\n")

    while True:
        difficulty, max_lives = choose_difficulty()
        won, _ = play_round(difficulty, max_lives)

        if won:
            wins += 1
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            losses += 1
            current_streak = 0

        print(
            f"\n{BOLD}Session statistics{RESET}\n"
            f"  Wins: {GREEN}{wins}{RESET}\n"
            f"  Losses: {RED}{losses}{RESET}\n"
            f"  Current streak: {current_streak}\n"
            f"  Best streak: {best_streak}"
        )

        if not ask_to_play_again():
            break

        clear_screen()
        print_title()

    print(f"\n{CYAN}Thanks for playing Python Hangman!{RESET}\n")


if __name__ == "__main__":
    main()
