from setuptools import setup, find_packages 
  
# with open('requirements.txt') as f: 
#     requirements = f.readlines() 
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# long_description = 'later' 
  
setup( 
        name ='megmap', 
        version ='0.0.1', 
        author ='Daniel H. Huson  and Anupam Gautam', 
        author_email ='gautamanupam07@gmail.com', 
        url ='https://github.com/husonlab/megmap.git', 
        description ='Start', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='GPL', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'megmap = megmap.megmap:main',
                'indexgenerator = megmap.index:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3.10", 
            # "License :: OSI Approved :: GPL", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='metagenome, alignment, mapping', 
        zip_safe = True
) 
