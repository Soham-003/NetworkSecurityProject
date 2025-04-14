from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    requirements_lst:List[str] = []
    try:
            with open(file_path,'r') as f:
                lines = f.readlines()
                for line in lines:
                    req = line.strip()
                    if req and req!= '-e.':
                        requirements_lst.append(req)
    except FileNotFoundError:
         print("requirements file was not found")

    return requirements_lst


setup(
     name = 'NetworkSecurity',
     author = 'Soham Khanna',
     author_email='sohamsawankhanna@gmail.com',
     version='0.0.1',
     packages= find_packages(),
     install_requires = get_requirements('requirements.txt')
)
