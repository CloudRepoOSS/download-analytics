import setuptools

setuptools.setup(
    name="CloudRepoAnalytics",
    version="1.0.0",
    author="CloudRepo",
    author_email="support@cloudrepo.io",
    url="https://cloudrepooss.github.io/download-analytics/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask>=1.0.2",
        "Flask-HttpAuth==3.3.0",
        "filehandlers>=2.7"
    ]
)
