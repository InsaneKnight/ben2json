#!/usr/bin/env python3

# ben2json - Tool to convert bencode to or from json
# Copyright (C) 2026-2028 Edward Chow <equu@openmail.cc>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import base64
import fastbencode
import json
import re
import sys

def dataenc(b):
    return f"<bytes len={len(b)}, data='{base64.b64encode(b).decode('utf-8')}'>"

def datamatch(s):
    return re.search(r"<bytes len=(\d+), data='([^']+)'>", s)

def datadec(s, match):
    expected_len = int(match.group(1))
    encoded_data = match.group(2)

    decoded_b = base64.b64decode(encoded_data)

    if len(decoded_b) != expected_len:
        raise ValueError(f"Length mismatch: expected {expected_len} bytes, but got {len(decoded_b)}.")

    return decoded_b

def human_readable(obj):
    if isinstance(obj, dict):
        return {human_readable(k): human_readable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [human_readable(item) for item in obj]
    if isinstance(obj, bytes):
        try:
            text = obj.decode("utf-8")
        except UnicodeDecodeError:
            return dataenc(obj)
        return text if text.isprintable() else dataenc(obj)
    return obj

def decode_str(obj):
    if isinstance(obj, dict):
        return {decode_str(k): decode_str(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode_str(item) for item in obj]
    if isinstance(obj, str):
        match = datamatch(obj)
        if not match:
            return obj.encode("utf-8")

        return datadec(obj, match)

    return obj



if len(sys.argv) == 1:
    sys.stderr.write(f"Usage: {sys.argv[0]} [j or b] < source > destnation\n")
    exit(0)

if sys.argv[1] == "j":
    data = fastbencode.bdecode(sys.stdin.buffer.read())
    json.dump(human_readable(data), sys.stdout)

if sys.argv[1] == "b":
    data = json.load(sys.stdin)
    sys.stdout.buffer.write(fastbencode.bencode(decode_str(data)))
