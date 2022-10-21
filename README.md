# koi
Object code instrumentation tool.

1. Change working directory into ./koi/
2. Set KOI\_ROOT to the current working directory:
KOI\_ROOT=`pwd`
3. Set desired platform in $KOI\_ROOT/config.py
4. Go to $KOI\_ROOT/examples/
5. Rum "make all\_oc" to build the demo app with instrumentation.
6. Run the app and collect the trace output to $KOI\_ROOT/examples/coverage.log
7. Run "make graph" to build the coverage data report (\*.cov and \*.dot files)
8. Have fun.
