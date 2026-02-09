# -*- mode: python -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Users\\cimei\\Documents\\Scripts\\AvalDesemp'],
             binaries=[],
             datas=[('instance','var\\project-instance'),\
                    ('project\\templates', 'project\\templates'),\
                    ('project\\core', 'project\\core'),\
                    ('project\\static','project\\static')],
             hiddenimports=['sqlalchemy.sql.default_comparator','pyodbc'],       
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
