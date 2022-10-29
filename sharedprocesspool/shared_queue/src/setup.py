from setuptools import setup, Extension

setup(name = "shmqueue",
      version = "0.1",
      ext_modules = [Extension("shmqueue", ["shmqueuemodule.c"])]
      );