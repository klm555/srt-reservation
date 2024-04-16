# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:10:57 2022

@author: hwlee
"""

from cx_Freeze import setup, Executable
import sys

# A list of packages to include in the build (this is to safeguard against cx_freeze missing a package since it automatically detects required packages).
buildOptions = dict(packages = [],
                    excludes = [],
                    include_files = ['SRT_reservation.ui', './images'],
                    zip_exclude_packages = [])

# base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Assigns default installation path while creating msi file
if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\SRT Reservation']
    
exe = [Executable("SRT_reservation_GUI.py", base=base, icon='./images/train_icon.png')]

setup(
    name='SRT_Reservation-v1.0',
    version = '1.0',
    author = "Hyeongwoo Lee",
    description = "SRT Automatic Reservation",
    options = dict(build_exe = buildOptions),
    executables = exe
)

