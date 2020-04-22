# _*_ coding: UTF-8 _*_

from setuptools import setup

setup(name="PyGVisuals",
      version="0.7",
      description="A collection of classes to create GUIs and more based purely on pygame.",
      url="https://github.com/Impelon/PyGVisuals",
      author="Impelon & kjkriegel",
      author_email="pygvisuals@kjkriegel.de",
      license="BSD-2-Clause",
      packages=["pygvisuals",
                "pygvisuals.borders",
                "pygvisuals.designs",
                "pygvisuals.io",
                "pygvisuals.util",
                "pygvisuals.widgets",],
      install_requires=["pygame"],
      zip_safe=False,)
