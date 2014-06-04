import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()
#enddef

requirements = [
    "flask"
]

setup(
    name='lelebehavior',
    version='0.1.0',
    packages = find_packages(exclude=['tests*']),
    install_requires = requirements,
    description='save user behavior.',
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst') + '\n\n' +
                      read('AUTHORS.rst')),
    url='http://github.com/weixiao/hawkwang/weixiao/wxservice/lelebehavior/',
    download_url = '',
    license='MIT',
    author='Wang Hao (Hawk)',
    author_email='wanghao.buaa@gmail.com',
    py_modules=['leleminer'],
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points = '''
    '''
)

