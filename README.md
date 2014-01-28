##tpb
It is a simple Python2 script that downloads all the stored photos from Tuenti, a popular Spanish social network. This one replaces the old PHP [tuentiphotobackup](https://github.com/outime/tuentiphotobackup) script.

###Required modules
Only [Requests](http://docs.python-requests.org/) module is required. Installing it with [pip](http://en.wikipedia.org/wiki/Pip_(package_manager\)) is the recommended/easiest way to do it: 

	$ pip install requests

###How to use
Run the tpb.py script with no arguments and it will interactively ask you for the login credentials. Once done that, it will fetch all your photos under the 'tagged' and 'uploaded' albums to later store them under your local 'photos' directory (which will be created if it does not exist beforehand).

One person wrote a full tutorial, although it is only available in Spanish: http://www.taringa.net/posts/hazlo-tu-mismo/17273968/Descargar-todas-las-fotos-del-Tuenti.html

###Issues
If you find that tpb is not working anymore, or that the code can (most likely) be improved, please submit a bug report to the [Issues page](https://github.com/outime/tpb/issues) or a [pull request](https://github.com/outime/tpb/pulls) if you can provide the code straight. Issues not directly related to the script itself will be automatically rejected (e.g. Python installation/configuration assistance).

One known issue that is not going to be fixed in the short-term is that the script downloads a smaller version of each of the pictures, although the difference is small. You can find more information here: https://github.com/outime/tpb/issues/3

###Can I run it using Python 3?
Kinda yes, check this: https://github.com/outime/tpb/pull/2 (TL;DR: use '2to3' Python tool to convert it into a Python 3 script).

###Contact information
Email: outime@gmail.com

Twitter: [@outime](http://twitter.com/outime)

###License
GPL v2. Full terms available in LICENSE file.
