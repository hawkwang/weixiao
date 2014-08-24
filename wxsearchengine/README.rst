wxanalyzer: Easy URL and web page content analyzer
==========================


The core API call is the function ``flag, msg, event = getEvent(url)``:

.. code-block:: python

   import wxanalyzer

   f, m, e = wxanalyzer.getEvent(url)

Package & Usage
-----------

Since *wxanalyzer* will be used in all the weixiao projects, so we just illustrate 
how to package and used in virtualenv.


Package
^^^^^

1. Prepare the requirements.txt and other stuff
2. Use ``python setup.py sdist`` to package module as follows:

dist

└── wxanalyzer-0.1.0.tar.gz


Usage with virtualenv
^^^^^

1. ``mkdir xyz; cd xyz``
2. ``virtualenv env``
3. Activate the virtual environment
   ``source env/bin/activate``
4. Install the required libraries
   ``pip install -r requirements.txt``
5. Install the wxanalyzer package
   ``pip install --no-index /wxanalyzer/dist/wxanalyzer-0.1.0.tar.gz``
6. Great, we can use the API call, see previous section.

Usage with Chinese
^^^^^

See: http://blog.csdn.net/gufengshanyin/article/details/21533409
