# -*- mode: python -*-

block_cipher = None

a = Analysis(
        ['lakeception/main.py'],
        pathex=['lakeception'],
        binaries=None,
        datas=[],
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
        console=True,
        exclude_binaries=False,
)

coll = COLLECT(
        exe,
        Tree('assets', 'assets'),
        strip=False,
        upx=True,
        name='lakeception',
)
