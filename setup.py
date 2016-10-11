from setuptools import setup, find_packages
import os

version = '1.2.0'

tests_require = [
    'ftw.builder',
    'ftw.testbrowser',
    'plone.app.testing',
    'unittest2',
    ]

setup(name='plonetheme.onegovbear',
      version=version,
      description='OneGov Plone theme sponsored by the city of Bern.',
      long_description=(open('README.rst').read() + '\n' +
                        open(os.path.join('docs', 'HISTORY.txt')).read()),

      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],

      keywords='plone theme onegov',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/OneGov/plonetheme.onegovbear',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plonetheme'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'ftw.theming',
          'ftw.upgrade',
          'plone.directives.form',
          'plone.api',
          'plone.app.theming',
          'setuptools',
          'z3c.jbot',
      ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
