import optparse


_parser = optparse.OptionParser(
    usage="""%prog [OPTIONS]
Examples:

Encode the file abc.txt:
    ~ $ manga-downloader  MANGA_NAME

        """,
    description="Encode/Decode a file using manga-downloader 's code",
)

# quiet options
_parser.add_option("-q", "--quiet",
                   dest="verbose",
                   action="store_false",
                   help="suppress non error messages",
                   default=True
                   )

_parser.add_option("-d", "--path",
                   dest="path",
                   type='string',
                   help="path to save the manga",
                   )
