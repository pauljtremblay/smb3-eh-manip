from setuptools import setup, find_packages

setup(
    name="smb3-eh-manip",
    version=open("data/version.txt", "r").read().strip(),
    description=("Ingest video data to render smb3 eh manip stimuli"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="smb3-eh-manip",
    author="Jon Robison",
    author_email="narfman0@blastedstudios.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        "dataclass_wizard==0.32.0", # newer versions break wizard_mixins
        "opencv-python",
        "pydispatcher",
        "pygame",
        "pygrabber",
        "pyserial",
        "python-vlc",
        "pyyaml",
        "pywin32",
        "smb3-video-autosplitter",
    ],
    test_suite="tests",
)
