from setuptools import setup, find_packages
import os

version = '1.3.3'

setup(name='redturtle.sendto_extension',
      version=version,
      description="Extension for the mail_to form on Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone sendto mail users groups',
      author='Redturtle Technology',
      author_email='info@redturtle.net',
      url='https://code.redturtle.it/svn/redturtle/redturtle.sendto_extension/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redturtle'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
