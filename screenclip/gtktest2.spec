# -*- mode: python -*-
a = Analysis(['E:\\workspace\\sublime_workspace\\python\\screenclip\\gtktest2.py'],
             pathex=['E:\\workspace\\sublime_workspace\\python\\screenclip'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'gtktest2.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='E:\\workspace\\sublime_workspace\\python\\screenclip\\1.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'gtktest2.exe.app'))
