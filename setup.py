#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五子棋游戏 py2app 打包配置文件
"""

from setuptools import setup

APP = ['gomoku.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None,  # 可以添加 .icns 图标文件路径
    'plist': {
        'CFBundleName': '五子棋游戏',
        'CFBundleDisplayName': 'Gomoku',
        'CFBundleIdentifier': 'com.gomoku.game',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHumanReadableCopyright': 'Copyright © 2024. All rights reserved.',
        'LSMinimumSystemVersion': '10.13',
        'NSPrincipalClass': 'NSApplication',
    },
    'packages': ['pygame'],
    'includes': ['pygame'],
    'excludes': [
        'tkinter',
        'unittest',
        'email',
        'html',
        'xml',
        'pydoc',
        'doctest',
        'pdb',
    ],
}

setup(
    name='Gomoku',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
