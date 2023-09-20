from setuptools import find_packages,setup
from typing import List

ignore = '-e .'

## Takes input file_path:(string object) and returns a list(of Requirements)
def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as file_obj:
        ## Reading all the requirements:
        requirements = file_obj.readlines()
        ## As all requirements would not be mentioned in same line:replace \n with blank
        requirements = [req.replace("\n","") for req in requirements]
        ## Ignoring -e. -> For building up packages:
        if ignore in requirements:
            requirements.remove(ignore)
        return requirements

setup(
    name="STUDENT_PERFORMANCE_ANALYSIS",
    version="0.0.1",
    author="Meet vasa",
    author_email="meet2work09@gmail.com",
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()

)