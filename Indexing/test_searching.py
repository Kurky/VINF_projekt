import unittest
from unittest.mock import patch
from io import StringIO
import sys

from Indexing.searching import searchPlayerInfoAndSeasonsByName, whoScoredMostGoals, twoPlayersPlayedTogether, \
    listOfPlayersCountryPosition


class TestPlayerFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='Patrick Kane')
    def test_searchPlayerInfoAndSeasonsByName(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            searchPlayerInfoAndSeasonsByName()
            output = mock_stdout.getvalue()
        self.assertIn('Results for player:  Patrick Kane', output)

    @patch('builtins.input', return_value='Matej Kuran')
    def test_searchPlayerInfoAndSeasonsByName_nonexistent_player(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            searchPlayerInfoAndSeasonsByName()
            output = mock_stdout.getvalue()
        self.assertIn('No results found for Player Name: Matej Kuran', output)

    @patch('builtins.input', side_effect=['Patrick Kane', 'Marian Hossa'])
    def test_twoPlayersPlayedTogether(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            twoPlayersPlayedTogether()
            output = mock_stdout.getvalue().strip()
        self.assertIn("Players played together in seasons:", output)

    @patch('builtins.input', side_effect=['Patrick Kane', 'Milan Jurcina'])
    def test_twoPlayersPlayedTogether_didnt_play(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            twoPlayersPlayedTogether()
            output = mock_stdout.getvalue().strip()
        self.assertIn("Players did not played together.", output)

    @patch('builtins.input', side_effect=['Sidney Crosby', 'Peter Forsberg', 'end'])
    def test_whoScoredMostGoals(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            whoScoredMostGoals()
            output = mock_stdout.getvalue().strip()
        self.assertIn("Player with most goals is: Sidney Crosby,Goals: 553", output)

    @patch('builtins.input', side_effect=['Russia', 'centre'])
    def test_listOfPlayersCountryPosition(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            listOfPlayersCountryPosition()
            output = mock_stdout.getvalue().strip()
        self.assertIn("List of players from specific country playing on specific position contains  26 records", output)


if __name__ == '__main__':
    unittest.main()
