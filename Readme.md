==About==
a python script that runs in 2.7 and 3.6 with no additional libraries needed.  If defined, the program pings all listed IP's in the cached file.  Then sweeps between the start and stop IP.  Once done, both cached and newly found IP's are merged into one sorted file, with duplicates removed.

==usage==
use --start to define start IP
use --stop to define stop IP
use --help or -? to display help

type python pingcheck.py <args> to run