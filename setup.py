from distutils.core import setup
setup(
    name = 'visualdeploy',
    packages = ['visualdeploy'],
    version = '0.1',
    description = 'See your app\'s deployment progress in real time',
    author = 'Frank Yang',
    author_email = 'puilp0502@gmail.com',
    url = 'https://github.com/puilp0502/visualdeploy',
    download_url = 'https://github.com/puilp0502/visualdeploy/tarball/0.1',
    keywords = ['deploy', 'wsgi', 'flask'],
    classifiers = [],
    install_requires=[
        'Werkzeug',
    ],
)
