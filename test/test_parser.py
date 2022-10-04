from dataclasses import asdict
import parser


def test_title_with_numeric_episode_number():
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


def test_title_with_numeric_episode_number_and_season_number():
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


def test_title_with_two_digit_numeric_episode_number():
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


def test_title_with_float_type_episode_number():
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


def test_title_with_series_name_and_episode_number():
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


def test_title_with_ranged_episode_number():
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


def test_title_with_provider_name():
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


def test_title_with_literal_season():
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


def test_title_with_no_episode_numbers_condensed():
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


def test_title_with_episode_name_including_ending_note():
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
