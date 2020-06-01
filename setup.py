import setuptools

# Read the long description:
with open("README.md", mode="r") as FILE_HANDLER:
    LONG_DESCRIPTION = FILE_HANDLER.read()

URLs = \
    {
        "Bug Tracker": "https://github.com/CloudRepoOSS/download-analytics/issues",
        "Source Code": "https://github.com/CloudRepoOSS/download-analytics",
        "License": "https://github.com/CloudRepoOSS/download-analytics/blob/master/LICENSE",
    }

CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Framework :: Flask",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: Apache Software License",
    "Intended Audience :: Developers",
    "Topic :: System",
    "Topic :: System :: Filesystems",
    "Topic :: System :: Logging",
    "Topic :: System :: Monitoring",
    "Topic :: System :: Software Distribution",
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Internet :: WWW/HTTP :: Site Management",
    "Topic :: Utilities",
    "Development Status :: 5 - Production/Stable",
    "Natural Language :: English",
]

setuptools.setup(
    name="CloudRepoAnalytics",
    description="Flask and Annie-based server to keep track of CloudRepo artifact download counts",
    version="2.0.0",
    author="CloudRepo",
    author_email="support@cloudrepo.io",
    maintainer="Reece Dunham",
    maintainer_email="me@rdil.rocks",
    url="https://cloudrepooss.github.io/download-analytics/",
    packages=setuptools.find_packages(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    include_package_data=True,
    zip_safe=False,
    project_urls=URLs,
    classifiers=CLASSIFIERS,
    install_requires=open("requirements.txt", "r").readlines(),
    python_requires=">3.3"
)
