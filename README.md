# ben2json

This is a python script to convert bencode to or from json.

## Bencode
This is a serialization scheme used by BitTorrent software. Other than torrent files, many BitTorrent software, like transmission and qbitorrent, also use this format to store runtime contextual data, such as the path to store shared files, the bitmap marking obtained pieces, etc, as `.resume` file and the like.

## Usage

When called with `sys.argv[1] == "j"`, this script converts a bencoded binary into json. If a bencode strings is "printable", it is converted to a plain utf-8 python string. otherwise, it is recognized as binary data and encoded into `<bytes len={length}, data='{base64-encoded}'>` form. When `sys.argv[1] == "b"`, this script converts a json conforming to such format back to bencoded binary data. Inputs are to be fed into stdin, and output is sent to stdout.

Inspired by [transmission2qbt](https://github.com/undertheironbridge/transmission2qbt), this script could be used to inspect the content of bencoded files, as well as by other scripts to automatically process runtime contextual data files with grep, sed, or json processors.
