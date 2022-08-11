# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['ward/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LICENSE', '.'),
        ('icon.png', '.'),
        ('config.json', '.'),
        ('config', 'keri/cf/')
    ],
    hiddenimports=[
        'falcon.app_helpers',
        'xml.etree',
        'falcon.responders',
        'falcon.routing',
        'falcon.request_helpers',
        'falcon.response_helpers',
        'falcon.forwarded',
        'falcon.media',
        'cgi',
        'falcon.vendor',
        'falcon.vendor.mimeparse'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ward',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=os.environ['WARD_SIGNER'],
    entitlements_file='entitlements.plist',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ward',
)
app = BUNDLE(
    coll,
    name='ward.app',
    icon='icon.icns',
    bundle_identifier=os.environ['WARD_IDENT'],
)
