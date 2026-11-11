#!/usr/bin/env python3
"""Regenerate the self-hosted LXGW WenKai subset used for headings."""

import argparse
import pathlib

from fontTools import subset

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_EXTS = {'.astro', '.ts', '.tsx', '.css', '.svg'}
EXTRA_CHARS = set('，。、；：？！“”‘’（）《》〈〉【】…—·～￥↑')


def collect_chars() -> str:
    chars = set()
    for path in (ROOT / 'src').rglob('*'):
        if path.suffix in SOURCE_EXTS:
            chars |= set(path.read_text(encoding='utf-8'))
    chars |= {chr(codepoint) for codepoint in range(0x20, 0x7F)}
    chars |= EXTRA_CHARS
    return ''.join(sorted(chars))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', help='LXGW WenKai TTF/OTF/WOFF2 source file')
    parser.add_argument(
        '--output',
        default=str(ROOT / 'public' / 'fonts' / 'lxgw-wenkai-regular.woff2'),
    )
    args = parser.parse_args()

    text = collect_chars()
    options = subset.Options()
    options.flavor = 'woff2'
    options.hinting = False

    font = subset.load_font(args.source, options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    subset.save_font(font, str(output), options)
    print(f'{len(text)} characters -> {output}')


if __name__ == '__main__':
    main()
