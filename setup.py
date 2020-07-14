from setuptools import setup, find_packages

setup(
    name="home_alarm",
    python_requires=">=3.6",
    package_dir={"": "apps/home_alarm"},
    packages=find_packages(where="apps/home_alarm"),
    py_modules=["home_alarm"],
)
