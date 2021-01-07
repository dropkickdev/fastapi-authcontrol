import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi-authcontrol", # Replace with your own username
    version="0.1.0",
    author="DropkickDev",
    author_email="enchance@gmail.com",
    description="A drop-in JWT authentication package which uses FastAPI-Users.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dropkickdev/fastapi-authcontrol.git",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)