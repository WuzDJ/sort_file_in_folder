from setuptools import setup, find_packages


setup(
    name='clean_folder',
      version='0.0.1',
      description='Very usefull code for clean and sort files',
      url='https://github.com/WuzDJ/sort_file_in_folder.git',
      author='WuzDJ',
      author_email='flyingcircus@example.com',
      #license='MIT',
      #packages=['clean_folder'],
      packages=find_packages(),
      entry_points={
          'console_scripts': ['clean-folder = clean_folder.clean:main']
      },
      zip_safe=False)