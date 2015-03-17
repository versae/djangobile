# Dependencies  and Instalation #
## Dependencies ##
### Required ###

  * [PyWURFL](http://celljam.net/#processor) ([pywurfl-6.4.0b](http://celljam.net/downloads/pywurfl/pywurfl-6.4.0b.tar.gz)). A Python language package that makes dealing with the WURFL in Python a little easier. Special thanks for Armand Lynch for his patience.

### Optional ###

  * [Levenshtein Module](http://celljam.net/downloads/pywurfl/python-Levenshtein-0.10.1.tar.gz) ([python-Levenshtein-0.10.1](http://celljam.net/downloads/pywurfl/python-Levenshtein-0.10.1.tar.gz)). Required if you want to use the Levenshtein distance or Jaro-Winkler algorithms for user agent similarity.
  * [lxml](http://codespeak.net/lxml/) ([lxml-2.1beta3.tar.gz](http://pypi.python.org/packages/source/l/lxml/lxml-2.1beta3.tar.gz#md5=1991c88415dde06a52db91d494ba680d)). Required in order to validate IDEAL XML templates against MyMobileWeb's IDEAL DTD scheme for presentations.
  * [pyparsing](http://pyparsing.wikispaces.com/) ([pyparsing-1.5.1.tar.gz](http://downloads.sourceforge.net/pyparsing/pyparsing-1.5.1.tar.gz?modtime=1224282264&big_mirror=0)). Required if you want to use the PyWURFL query language for create devices families.

## Instalation ##

Simply check out djangobile in a django project root.

`svn checkout http://djangobile.googlecode.com/svn/trunk/djangobile djangobile`

And set a new context processor in your project settings.py
```
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    # This context processor is required to djangobile works properly.
    'djangobile.context_processors.mobile',

)
```