from distutils.core import setup

setup(name='noterminal',
      version='0.1',
      description='Transient Jupyter notebooks',
      author='Andy Jones',
      author_email='andyjones.ed@gmail.com',
      url='https://github.com/andyljones/noterminal',
      packages=['noterminal'],
      install_requires=[
            'jupyter_nbextensions_configurator'
      ])
