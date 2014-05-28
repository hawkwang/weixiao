import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()
#enddef

requirements = [
    "beautifulsoup",
]

setup(
    name='wxanalyzer',
    version='0.1.0',
    packages = find_packages(exclude=['tests*']),
    install_requires = requirements,
    dependency_links = ['git+https://github.com/Hypernode/M2Crypto#egg=M2Crypto-0.22.dev',
                        'git+https://github.com/andymccurdy/redis-py.git@976e72be529fdf741b75a71746f34c6530fc8ae9#egg=redis-dev'],    
    description='Dealing with url webpages using lots of fantastic algorithms.',
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst') + '\n\n' +
                      read('AUTHORS.rst')),
    url='http://github.com/weixiao/hawkwang/weixiao/analyzer/',
    download_url = '',
    license='MIT',
    author='Wang Hao (Hawk)',
    author_email='wanghao.buaa@gmail.com',
    py_modules=['wxanalyzer'],
    include_package_data=True,
    classifiers=[
        'Private :: Do Not Upload',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points = '''
    '''
)

