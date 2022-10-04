from contextlib import suppress
from dataclasses import dataclass, field
from math import nan, isnan
from typing import Final


@dataclass
class Title:
    original: str = field(default_factory=str)
    seasonal: str = field(default_factory=str)
    series: str = field(default_factory=str)


@dataclass
class Codec:
    video: str = field(default_factory=str)
    audio: str = field(default_factory=str)


@dataclass
class File:
    name: str = field(default_factory=str)
    resolution: str = field(default_factory=str)
    codec: Codec = field(default_factory=Codec)


@dataclass
class Provider:
    channel: str = field(default_factory=str)


@dataclass
class Objet:
    title: Title = field(default_factory=Title)
    file: File = field(default_factory=File)
    provider: Provider = field(default_factory=Provider)
    episodes: list[int | float] = field(default_factory=list)
    seasons: list[int] = field(default_factory=list)


def is_numeric(char: str) -> bool:
    return char != " " and char.isnumeric()


def is_alphabet(char: str) -> bool:
    code = ord(char)
    return code >= 97 and code <= 122


def get_leading_numeric(text: str, i: int) -> tuple[int | float, int]:
    kind = ""

    with suppress(IndexError):
        while is_numeric(text[i]) or text[i] == ".":
            kind += text[i]
            i += 1

    # Fuck js number
    if kind.isnumeric():
        kind = int(kind)
    else:
        try:
            kind = float(kind)
        except ValueError:
            kind = nan

    return kind, i


def get_literal_position(text: str, i: int, match: str) -> tuple[str, int]:
    buffer = ""

    while text[i] != match:
        buffer += text[i]
        i += 1

    return buffer, i


def get_numeric_size(n: int) -> int:
    a = 10
    b = 1

    while n / a >= 1:
        a *= 10
        b += 1

    return b


def parse(text: str) -> Objet:
    low = text.lower()
    objet: Final = Objet()
    objet.file.name = text

    buffer: str = ""
    i: int = 0
    while i < len(low):
        # Should be matched during default match -> to be title
        if low[i] == "-":
            if is_numeric(low[i + 1]) and is_numeric(low[i - 1]):
                # Catch SERIESN-N pattern
                _kind = low[i - 1]

                k = i - 2
                while is_numeric(low[k]):
                    _kind = low[k] + _kind
                    k += 1

                kind = int(_kind)
                following, next = get_leading_numeric(text, i + 1)

                if not (following - kind):
                    buffer += text[i]
                    i += 1
                    continue

                assert isinstance(following, int)  # must be int

                objet.title.series = objet.title.series[0:-1]
                objet.episodes = [kind + i for i in range(following - kind + 1)]
                buffer = ""
                i = next
            elif low[i - 1] != " ":
                # It's not type of episode number or series name
                buffer += text[i]
                i += 1
                continue
            # It's kind of episode number or series name
            # Let's set the title and empty buffer
            objet.title.seasonal = objet.title.seasonal or objet.title.original + buffer
            # Fallback for original title because of default case of switch statement
            objet.title.original = objet.title.original or objet.title.seasonal

            i += 1
            expect = i + 1

            if is_numeric(low[expect]):
                # Should be episode number
                kind, next = get_leading_numeric(low, expect)
                objet.episodes = [kind]
                i = next
            elif low.find("-", i) >= 0:
                # Should be series name
                series, next = get_literal_position(text, i, "-")
                objet.title.series += series.strip()
                # Make sure that the hyphen to be matched in next loop
                i = next - 1
            elif low.find("(", i) >= 0:
                # Should be series name
                series, next = get_literal_position(text, i, "(")
                objet.title.series += series.strip()
                # Make sure that the hyphen to be matched in next loop
                i = next - 1
        elif low[i] == "(":
            # Fallback if there was no hyphen during loop
            objet.title.seasonal = objet.title.seasonal or objet.title.original + buffer
            objet.title.original = objet.title.original or objet.title.seasonal

            # Skip initial
            i += 1

            inner, next = get_literal_position(text, i, ")")
            parts = inner.split(" ")

            if len(parts) == 1:
                buffer += text[i]
                i += 1
                continue

            # Almost every extractors set like: CHANNEL RESOLUTION VIDEO_CODEC AUDIO_CODEC
            channel, resolution, video_codec, audio_codec = parts

            objet.provider.channel = channel
            objet.file.resolution = resolution
            objet.file.codec.video = video_codec
            objet.file.codec.audio = audio_codec
            i = next
        elif low[i] == "s":
            # Check if SNEN style available
            kind, next = get_leading_numeric(low, i + 1)
            if isnan(kind) or is_alphabet(low[i - 1]):
                buffer += text[i]
                i += 1
                continue
            # Set the title before clearing out the buffer
            objet.title.original = objet.title.original or buffer
            objet.title.seasonal = objet.title.seasonal or buffer + text[i] + str(kind)

            # Put seasonal data
            assert isinstance(kind, int)  # must be int
            objet.seasons.append(kind)
            buffer = ""
            i = next

        elif low[i] == "e":
            # Check if SNEN style available
            kind, next = get_leading_numeric(low, i + 1)
            if isnan(kind):
                buffer += text[i]
                i += 1
                continue

            objet.episodes = [kind]
            buffer = ""
            i = next
        elif low[i] == "]":
            buffer = ""
        else:
            # Think about the case of: 1st, 2nd, 3rd, and Nth season
            if is_numeric(low[i]):
                ordinal = ["st", "nd", "rd", "th"]

                kind, unit_from = get_leading_numeric(low, i)
                unit = low[unit_from : unit_from + 2]

                assert isinstance(kind, int)  # must be int

                if unit in ordinal and ordinal.index(unit) >= 0:
                    # Fill out the seasonal information and the title
                    objet.title.original = objet.title.original or buffer
                    objet.seasons = [kind]
                    buffer = str(kind) + unit
                    i = unit_from + 2
                elif not is_alphabet(low[i + get_numeric_size(kind) + 1]):
                    # Heuristically guess seasonal information
                    # If text[i + 2] is not alphabet, I suppose text[i + 2] is space or hyphen
                    objet.title.original = objet.title.original or buffer
                    objet.seasons = [kind]
                    buffer = str(kind)
                    i = unit_from

            if len(buffer) or low[i] != " ":
                buffer += text[i]
        i += 1

    if not len(objet.seasons):
        objet.seasons.append(1)

    objet.title.original = objet.title.original.strip()
    objet.title.seasonal = objet.title.seasonal.strip()
    objet.title.series = objet.title.series.strip()

    return objet
