import unittest

from osrs_api.hiscores import Hiscores
from osrs_api.const import SKILLS_AMT, MINIGAMES_AMT, BOSSES_AMT


class TestHiscore(unittest.TestCase):
    def test_api_length(self):
        """
        Check to see if the API returns the same number of skill, activity, and boss
        rows that are mentioned in const.py. If this test fails, the items in
        const.py need to be updated.
        """
        score = Hiscores(username="Lelalt")
        expected_num_api_elements = 1 + SKILLS_AMT + MINIGAMES_AMT + BOSSES_AMT
        api_data = score._get_api_data()

        len_api_data = len(api_data)

        self.assertEqual(expected_num_api_elements, len_api_data)

    def test_current_hiscore_entries_present(self):
        score = Hiscores(username="Lelalt")

        self.assertIn("sailing", score.skills)
        self.assertIn("Grid Points", score.minigames)
        self.assertIn("League Points", score.minigames)
        self.assertIn("Collections Logged", score.minigames)
        self.assertIn("Brutus", score.bosses)
        self.assertIn("Doom of Mokhaiotl", score.bosses)
        self.assertIn("Shellbane Gryphon", score.bosses)
        self.assertIn("The Royal Titans", score.bosses)
        self.assertIn("Yama", score.bosses)
