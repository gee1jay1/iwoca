Greg Judd - Iwoca technical task

There was quite a lot to fit into the time frame here, and I fear I may have spread myself a little thin across
the tasks. There are numerous notes / improvements listed below. I wanted to honour the time limit so have
just listed improvements as opposed to implemented, but I realise my solution is far from perfect.

Notes:

- To run:

  Create a virtual env and install packages 'pip3 install -r requirements.txt'.

  Then to run the actual script:

  python3 companies_house_reporter.py -h

  to provide instructions.

  Note that the input is done by id (see improvements).

  To run tests:

  python3 -m pytest tests/<test_file_name>


- I have never used any graph visualisation libraries, so implementing this took up a good chunk of time.

- I have added tests for the bulk of the functions which don't require external API calls. Had I more time,
  I would have mocked the requests and their responses and added tests for the rest of the functions.
  But hopefully the test files I've provided give an idea of the style in which I write tests.
  I would also add more tests for the functions I have tested  if I had more time.

- I decided to keep the calculation of credit score for the individual companies separate from the graph logic
  to provide flexibility. This value is then assigned to each node, and to get the total score we add the score
  for a given companies node to all those companies which are one separation away (i.e. companies joined together
  with one director between them). Given more time, I imagine something like Pagerank would provide a better
  scoring method.

- I found a library for interfacing with the API so decided to use it - https://github.com/JamesGardiner/chwrapper

- I had some problems trying to install matplotlib.

  If you have errors, try:

  brew install libpng
  brew install freetype

  and if you have any problems with libpng linking, try:

  sudo chown -R "$USER":admin /usr/local
  sudo chown -R "$USER":admin /Library/Caches/Homebrew
  brew link libpng

- The time taken increases fairly dramatically with increased depth (~7mins for depth of 3).
  I may have missed something, but I couldn't find anything in the API that allowed the querying of more than
  one company or director at any one time. Therefore the bottleneck is the number of API calls as you have to make
  one per company / directory you have in the graph and this can get very large.

- Any problems with retrieving data from the API is printed to stdout, but in a more featured application
  this would be directed to a log file.


Improvements:

- Be able to use director / company name instead of id for input. This would likely involve using the API search
  call.

- Perhaps have the interface as a web app instead of a command line if there will be multiple people using it.

- Caching popular queries.

- Caching function for getting search client.

- Add tests for other functions that involve API calls.

- Perhaps normalise the credit score / use a more detailed calculation (Pagerank etc).

- If possible, tailor drawing of graph to the number of nodes so that we don't squash higher
  order graph images. Currently it is optimised for depth of 2.
