# -*- mode: python -*-

block_cipher = None

a = Analysis(
        ['main.py'],
        pathex=[],
        binaries=None,
        datas=[
            ('biomes', 'biomes'),
            ('audio', 'audio'),
        ],
        hiddenimports=[],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
)

pyz = PYZ(
        a.pure,
        a.zipped_data,
        cipher=block_cipher,
)

exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name='lakeception',
        debug=False,
        strip=False,
        upx=True,
        console=False,
        exclude_binaries=False,
)

coll = COLLECT(
        exe,
        strip=False,
        upx=True,
        name='main',
)
