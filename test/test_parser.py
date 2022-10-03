from dataclasses import asdict
from math import nan
import parser


def test_is_numeric():
    assert parser.is_numeric(" ") is False
    assert parser.is_numeric("0") is True
    assert parser.is_numeric("1") is True


def test_get_leading_numeric():
    assert parser.get_leading_numeric("1a", 0) == (1, 1)
    assert parser.get_leading_numeric("123a", 0) == (123, 3)
    assert parser.get_leading_numeric("a", 0) == (nan, 0)
    assert parser.get_leading_numeric("12", 0) == (12, 2)


def test_get_literal_position():
    assert parser.get_literal_position("abc-", 0, "-") == ("abc", 3)


def test_get_numeric_size():
    assert parser.get_numeric_size(1) == 1
    assert parser.get_numeric_size(0) == 1
    assert parser.get_numeric_size(10) == 2
    assert parser.get_numeric_size(100) == 3


def test_is_alphabet():
    assert parser.is_alphabet("a") is True
    assert parser.is_alphabet("A") is False
    assert parser.is_alphabet("z") is True
    assert parser.is_alphabet("Z") is False
    assert parser.is_alphabet("0") is False
    assert parser.is_alphabet("-") is False


def test_parse():
    # Title with numeric episode number
    assert asdict(parser.parse("Title - 1 (CH 1920x1080 x264 AAC)")) == {
        "title": {
            "original": "Title",
            "seasonal": "Title",
            "series": "",
        },
        "file": {
            "name": "Title - 1 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {
                "video": "x264",
                "audio": "AAC",
            },
        },
        "provider": {
            "channel": "CH",
        },
        "episodes": [1],
        "seasons": [1],
    }
    # Title with numeric episode number and season number
    assert asdict(parser.parse("Title 2 - 1 (CH 1920x1080 x264 AAC)")) == {
        "title": {"original": "Title", "seasonal": "Title 2", "series": ""},
        "file": {
            "name": "Title 2 - 1 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [1],
        "seasons": [2],
    }
    # Title with two digit numeric episode number
    assert asdict(parser.parse("Title - 01 (CH 1920x1080 x264 AAC)")) == {
        "title": {"original": "Title", "seasonal": "Title", "series": ""},
        "file": {
            "name": "Title - 01 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [1],
        "seasons": [1],
    }
    # Title with float type episode number
    assert asdict(parser.parse("Title - 01.2 (CH 1920x1080 x264 AAC)")) == {
        "title": {"original": "Title", "seasonal": "Title", "series": ""},
        "file": {
            "name": "Title - 01.2 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [1.2],
        "seasons": [1],
    }
    # Title with series name and episode number
    assert asdict(parser.parse("Title - Subtitle - 01 (CH 1920x1080 x264 AAC)")) == {
        "title": {"original": "Title", "seasonal": "Title", "series": "Subtitle"},
        "file": {
            "name": "Title - Subtitle - 01 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [1],
        "seasons": [1],
    }
    # Title with ranged episode number
    assert asdict(parser.parse("Title - SUB2-9 (CH 1920x1080 x264 AAC)")) == {
        "title": {"original": "Title", "seasonal": "Title", "series": "SUB"},
        "file": {
            "name": "Title - SUB2-9 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [2, 3, 4, 5, 6, 7, 8, 9],
        "seasons": [1],
    }
    # Title with provider name
    assert asdict(
        parser.parse("[PROVIDER] Title - SUB2-9 (CH 1920x1080 x264 AAC)")
    ) == {
        "title": {"original": "Title", "seasonal": "Title", "series": "SUB"},
        "file": {
            "name": "[PROVIDER] Title - SUB2-9 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [2, 3, 4, 5, 6, 7, 8, 9],
        "seasons": [1],
    }
    # Title with literal season
    assert asdict(
        parser.parse("[PROVIDER] Title 2nd season - SUB2-9 (CH 1920x1080 x264 AAC)")
    ) == {
        "title": {"original": "Title", "seasonal": "Title 2nd season", "series": "SUB"},
        "file": {
            "name": "[PROVIDER] Title 2nd season - SUB2-9 (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [2, 3, 4, 5, 6, 7, 8, 9],
        "seasons": [2],
    }
    # Title with no episode numbers (condensed)
    assert asdict(
        parser.parse("[PROVIDER] Title 2nd season (CH 1920x1080 x264 AAC)")
    ) == {
        "title": {"original": "Title", "seasonal": "Title 2nd season", "series": ""},
        "file": {
            "name": "[PROVIDER] Title 2nd season (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [],
        "seasons": [2],
    }
    # Title with episode name including ending note
    assert asdict(
        parser.parse("[PROVIDER] Title 2nd season - 2 END (CH 1920x1080 x264 AAC)")
    ) == {
        "title": {"original": "Title", "seasonal": "Title 2nd season", "series": ""},
        "file": {
            "name": "[PROVIDER] Title 2nd season - 2 END (CH 1920x1080 x264 AAC)",
            "resolution": "1920x1080",
            "codec": {"video": "x264", "audio": "AAC"},
        },
        "provider": {"channel": "CH"},
        "episodes": [2],
        "seasons": [2],
    }
