import unittest
import urllib.request

from concurrent.futures import ThreadPoolExecutor

from osrs_api import get_icon_url
from osrs_api import const


def _fetch_icon(name):
    url = get_icon_url(name)
    request = urllib.request.Request(url, headers={"User-Agent": "python-osrsapi-tests"})

    with urllib.request.urlopen(request, timeout=10) as response:
        return name, url, response.getcode(), response.info().get_content_type()


class TestIconUrls(unittest.TestCase):
    def test_known_urls_match_expected_paths(self):
        self.assertEqual(
            get_icon_url("attack"),
            "https://www.runescape.com/img/rsp777/hiscores/skill_icon_attack1.gif",
        )
        self.assertEqual(
            get_icon_url("Bounty Hunter - Hunter"),
            "https://www.runescape.com/img/rsp777/game_icon_bountyhunterhunter.png",
        )
        self.assertEqual(
            get_icon_url("barrows"),
            "https://www.runescape.com/img/rsp777/game_icon_barrowschests.png",
        )

    def test_invalid_name_raises(self):
        with self.assertRaises(ValueError):
            get_icon_url("not a real hiscore entry")

    def test_all_canonical_icon_urls_are_reachable(self):
        names = const.SKILLS + const.MINIGAMES + const.BOSSES

        with ThreadPoolExecutor(max_workers=12) as executor:
            for name, url, status_code, content_type in executor.map(_fetch_icon, names):
                with self.subTest(name=name, url=url):
                    self.assertEqual(status_code, 200)
                    self.assertTrue(content_type.startswith("image/"), content_type)