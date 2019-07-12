# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['./', 'G:\\Pokemon 1.0'],
             binaries=[],
             datas=[('./*.png','.'),('./*.PNG','.'),('./*.py','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')

["abilities.py","chaos.py","Flampod.PNG","header1.py","healerBoi.png","healthPot.png","hotpi.png","peanis.png","pokeball.png","pourpiss.png","shopBoi.png","thorbon.png","trainer1.png","uncleRicky.png"