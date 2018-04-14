from setuptools import setup, find_packages

setup(
      name='prala',
      version='0.0.11',
      description='Practice Language',
      long_description=open('README.md').read(),
      url='http://github.com/dallaszkorben/prala',
      author='dallaszkorben',
      author_email='dallaszkorben@gmail.com',
      license='MIT',
      classifiers =[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
      ],
      packages = find_packages(),
      install_requires=[
          'pyttsx3', 'numpy',
      ],
      entry_points = {
        'console_scripts': ['pracon=prala.console:main'],
      },
      package_data={
        'prala': ['*.txt'],
      },
      include_package_data = True,
      zip_safe=False)