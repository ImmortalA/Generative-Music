from music21 import chord, metadata, stream, environment

us = environment.UserSettings()
us['musicxmlPath'] = r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"

class LSystem:
    """
    A basic L-system class that provides functionality for generating sequences
    based on initial axiom and production rules.
    """

    def __init__(self, axiom, rules):
        """
        Initialize the L-system with an axiom and production rules.

        Parameters:
        - axiom (str): The initial sequence of chords.
        - rules (dict): A dictionary where keys are symbols and values are
            the corresponding replacement strings. For example, {"Am": "F,G"}
        """
        self.axiom = axiom.split(",")
        self.rules = rules
        self.output = self.axiom
    @property
    def alphabet(self):
        """
        Get the alphabet of the L-system.

        Returns:
        - set: The alphabet of the L-system.
        """
        return set(self.axiom + [item for sublist in self.rules.values() for item in sublist.split(",")])

    def iterate(self, n=1):
        """
        Apply the production rules to the current output n times.

        Parameters:
        - n (int): Number of times the rules are to be applied.

        Returns:
        - list: The output after applying the rules n times.
        """
        for i in range(n):
            next_output = self._iterate_once()
            self.output = next_output
            print(f"Output after {i + 1} iteration(s): {','.join(self.output)}")
        final_output = self.output
        self._reset_output()
        return final_output

    def _iterate_once(self):
        """
        Apply the production rules to the current output once.

        Returns:
        - list: The output after applying production rules once.
        """
        symbols = [self._apply_rule(symbol) for symbol in self.output]
        return [item for sublist in symbols for item in sublist]


    def _apply_rule(self, symbol):
        """
        Apply production rules to a given symbol.

        Parameters:
        - symbol (str): The symbol to which rules are to be applied.

        Returns:
        - list: The transformed symbol or original symbol if no rules apply.
        """
        return self.rules.get(symbol, symbol).split(",")

    def _reset_output(self):
        """Reset the output to the initial axiom."""
        self.output = self.axiom


def l_system_to_music21_chords(chord_sequence):
    """
    Translate the L-system generated chord sequence into a list of music21 
    chords.

    Parameters:
    - chord_sequence (list): The L-system generated chord sequence.

    Returns:
    - list of music21.chord.Chord: The corresponding chord progression in music21 format.
    """
    chord_dict = {
        "C": ["C", "E", "G"],       # Cmaj
        "Dm": ["D", "F", "A"],      # Dmin
        "Em": ["E", "G", "B"],      # Emin
        "F": ["F", "A", "C"],       # Fmaj
        "G": ["G", "B", "D"],       # Gmaj
        "Am": ["A", "C", "E"],      # Amin
        "Bdim": ["B", "D", "F"],    # Bdim
    }
    return [chord.Chord(chord_dict[chord_name]) for chord_name in chord_sequence if chord_name in chord_dict]


def create_and_show_music21_score(music21_chords):
    """
    Create and display a music score using the music21 library.

    This function takes a list of music21 chord objects and creates a score
    with them. It then displays this score. The score is titled "L-System Chord Progression".

    Parameters:
    - music21_chords (list): A list of music21 chord objects.
    """

    # Create a new music21 stream.Score object
    score = stream.Score()

    # Set the metadata for the score with a title
    score.metadata = metadata.Metadata(title="L-System Chord Progression")

    # Create a new music21 stream.Part object
    part = stream.Part()

    # Loop through each chord in the music21_chords list
    for chord in music21_chords:
        # Append each chord to the Part object
        part.append(chord)

    # Append the Part object containing chords to the Score object
    score.append(part)

    # Display the score
    score.show()


def main():
    """
    Main function to demonstrate the generation of chord progression using L-system.
    """
    axiom = "Am"
    rules = {"Am": "Am,F,G", "C": "C,G,Am", "F": "Dm", "G": "G,C"}

    l_system = LSystem(axiom, rules)

    chord_sequence = l_system.iterate(4)  # The number determines how many times the rules will be applied
    music21_chords = l_system_to_music21_chords(chord_sequence)

    create_and_show_music21_score(music21_chords)


if __name__ == "__main__":
    main()