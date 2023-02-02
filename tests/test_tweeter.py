import filecmp
from unittest import TestCase, skip

from utils import File, Twitter

from tests.test_parser_mixin import TEST_WR
from weather_lk import Tweeter

TEST_TWEETER = Tweeter(TEST_WR)


class TestTweeter(TestCase):
    def test_tweet_image_path(self):
        self.assertEqual(
            TEST_TWEETER.tweet_image_path,
            '/tmp/weather_lk.20230202.png',
        )

    @skip('File Compare')
    def test_build_tweet_image(self):
        TEST_TWEETER.build_tweet_image()
        self.assertTrue(
            filecmp.cmp(
                TEST_TWEETER.tweet_image_path,
                'tests/tweet.png',
                shallow=False,
            )
        )

    def test_tweet_text(self):
        observed_lines = TEST_TWEETER.tweet_text.split('\n')
        expected_lines = File('tests/tweet.txt').read_lines()
        for observed, expected in zip(observed_lines, expected_lines):
            self.assertEqual(observed, expected)

    def test_tweet(self):
        self.assertEqual(
            TEST_TWEETER.tweet.text,
            TEST_TWEETER.tweet_text,
        )

    @skip('Twitter API Use')
    def test_send(self):
        Twitter.from_environ_vars().send(TEST_TWEETER.tweet)
