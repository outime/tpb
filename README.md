##tuentiphotobackup (tpb)

It is a simple Python2 script that downloads all the stored photos from Tuenti, a popular Spanish social network. This one replaces the old PHP [tuentiphotobackup](https://github.com/outime/tuentiphotobackup) script.

###Required modules
Only [Requests](http://docs.python-requests.org/) module is required. Installing it with [pip](http://en.wikipedia.org/wiki/Pip_(package_manager\)) is the recommended/easiest way to do it: $ pip install requests

###How to use
Execute 'tpb.py' script with no arguments as it will interactively ask you for the login details. Just after that, it will automatically fetch all your photos under the 'tagged' album and store them under your local 'photos' directory (which will be created if it does not yet exist).

###Issues
If you find that tpb is not working anymore, or you think the code can be improved (I am always learning, feel free to kindly complain) please submit a bug at the [Issues page](https://github.com/outime/tpb/issues) or a [pull request](https://github.com/outime/tpb/pulls) if you can fix it. Issues not directly related to the script itself will be ignored and closed automatically (e.g. Python installation/configuration assistance).

###What about the old "TuentiPhotoBackup"?
The first ugly version was done in PHP as a personal script where beautiful code or logic were not involved. This one is done in Python and although it is still a personal ugly script, it fixes many bugs from the other one. I did not see a reason to replace all the old code from the first version with a new script done in a different language, so I decided to just put it under "tpb" name.

###Contact information
Email: outime@gmail.com

Twitter: [@outime](http://twitter.com/outime)

###License
GPL v2. Full terms available in LICENSE file.
