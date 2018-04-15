from setuptools import setup, find_packages

setup(
      name='prala',
      version='0.0.23',
      description='Practice Language',
      long_description=open('README.md').read(),
      url='http://github.com/dallaszkorben/prala',
      author='dallaszkorben',
      author_email='dallaszkorben@gmail.com',
      license='MIT',
      classifiers =[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
      ],
      packages = find_packages(),
      setup_requires=["numpy", "pyttsx3"],
      install_requires=[
          'pyttsx3', 'numpy', 'configparser', 'iso639'
      ],
      entry_points = {
        'console_scripts': ['pracon=prala.console:main'],
      },
      package_data={
        'prala': ['*.txt'],
      },
      include_package_data = True,
      zip_safe=False)