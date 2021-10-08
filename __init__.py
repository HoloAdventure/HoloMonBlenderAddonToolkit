# 各種ライブラリインポート
if "bpy" in locals():
    import importlib
    if "Addon_control_view" in locals():
        importlib.reload(Addon_control_view)
    if "Addon_delete_object_byvolume" in locals():
        importlib.reload(Addon_delete_object_byvolume)
    if "Addon_decimate_mesh" in locals():
        importlib.reload(Addon_decimate_mesh)
import bpy
from . import Addon_control_view
from . import Addon_delete_object_byvolume
from . import Addon_decimate_mesh

# bl_infoでプラグインに関する情報の定義を行う
bl_info = {
    "name": "HoloMon Blender Addon Toolkit",         # プラグイン名
    "author": "HoloMon",                             # 制作者名
    "version": (1, 2),                               # バージョン
    "blender": (2, 90, 0),                           # 動作可能なBlenderバージョン
    "support": "COMMUNITY",                          # サポートレベル(OFFICIAL,COMMUNITY,TESTING)
    "category": "3D View",                           # カテゴリ名
    "location": "View3D > Sidebar > HMToolkit",      # ロケーション
    "description": "自作簡易アドオンの詰め合わせ",     # 説明文
    "location": "",                                  # 機能の位置付け
    "warning": "",                                   # 注意点やバグ情報
    "doc_url": "",                                   # ドキュメントURL
}

# 作成クラスと定義の登録メソッド
def register():
    # 各アドオンの登録メソッドを呼び出す
    Addon_control_view.register()
    Addon_delete_object_byvolume.register()
    Addon_decimate_mesh.register()
# 作成クラスと定義の登録解除メソッド
def unregister():
    # 各アドオンの登録解除メソッドを呼び出す
    Addon_control_view.unregister()
    Addon_delete_object_byvolume.unregister()
    Addon_decimate_mesh.unregister()

# 実行時の処理
if __name__ == "__main__":
    # 作成クラスと定義を登録する
    register()


