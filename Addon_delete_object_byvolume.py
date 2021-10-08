# 定数の定義
ADDON_TITLE = "Object Delete ByVolume"
ADDON_COMMONNAME = "holomon_delete_object_byvolume"
ADDON_OPERATOR_IDNAME = "holomon.decimate_object"

# bl_infoでプラグインに関する情報の定義を行う
bl_info = {
    "name": ADDON_TITLE + " Addon by HoloMon",       # プラグイン名
    "author": "HoloMon",                             # 制作者名
    "version": (1, 0),                               # バージョン
    "blender": (2, 90, 0),                           # 動作可能なBlenderバージョン
    "support": "TESTING",                            # サポートレベル
    "category": "3D View",                           # カテゴリ名
    "location": "View3D > Sidebar > HMToolkit",      # ロケーション
    "description": ADDON_TITLE + "Addon",            # 説明文
    "location": "",                                  # 機能の位置付け
    "warning": "",                                   # 注意点やバグ情報
    "doc_url": "",                                   # ドキュメントURL
}

# 利用するタイプやメソッドのインポート
import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, FloatProperty

# 継承するクラスの命名規則は以下の通り
# [A-Z][A-Z0-9_]*_(継承クラスごとの識別子)_[A-Za-z0-9_]+
# クラスごとの識別子は以下の通り
#   bpy.types.Operator  OT
#   bpy.types.Panel     PT
#   bpy.types.Header    HT
#   bpy.types.MENU      MT
#   bpy.types.UIList    UL

# Panelクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.Panel.html
class HOLOMON_PT_holomon_delete_object_byvolume(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "指定オブジェクトの削除"
    # クラスのIDを定義する
    # 命名規則は CATEGORY_PT_name
    bl_idname = "HOLOMON_PT_" + ADDON_COMMONNAME
    # パネルを使用する領域を定義する
    # 利用可能な識別子は以下の通り
    #   EMPTY：無し
    #   VIEW_3D：3Dビューポート
    #   IMAGE_EDITOR：UV/画像エディター
    #   NODE_EDITOR：ノードエディター
    #   SEQUENCE_EDITOR：ビデオシーケンサー
    #   CLIP_EDITOR：ムービークリップエディター
    #   DOPESHEET_EDITOR：ドープシート
    #   GRAPH_EDITOR：グラフエディター
    #   NLA_EDITOR：非線形アニメーション
    #   TEXT_EDITOR：テキストエディター
    #   CONSOLE：Pythonコンソール
    #   INFO：情報、操作のログ、警告、エラーメッセージ
    #   TOPBAR：トップバー
    #   STATUSBAR：ステータスバー
    #   OUTLINER：アウトライナ
    #   PROPERTIES：プロパティ
    #   FILE_BROWSER：ファイルブラウザ
    #   PREFERENCES：設定
    bl_space_type = 'VIEW_3D'
    # パネルが使用される領域を定義する
    # 利用可能な識別子は以下の通り
    # ['WINDOW'、 'HEADER'、 'CHANNELS'、 'TEMPORARY'、 'UI'、
    #  'TOOLS'、 'TOOL_PROPS'、 'PREVIEW'、 'HUD'、 'NAVIGATION_BAR'、
    #  'EXECUTE'、 'FOOTER'の列挙型、 'TOOL_HEADER']
    bl_region_type = 'UI'
    # パネルタイプのオプションをset型で定義する
    # DEFAULT_CLOSED：作成時にパネルを開くか折りたたむ必要があるかを定義する。
    # HIDE_HEADER：ヘッダーを非表示するかを定義する。Falseに設定するとパネルにはヘッダーが表示される。
    # デフォルトはオプション無し
    bl_options = set()
    # パネルの表示順番を定義する
    # 小さい番号のパネルは、大きい番号のパネルの前にデフォルトで順序付けられる
    # デフォルトは 0
    bl_order = 0
    # パネルのカテゴリ名称を定義する
    # 3Dビューポートの場合、サイドバーの名称になる
    # デフォルトは名称無し
    bl_category = "HMToolkit"
 
    # 描画の定義
    def draw(self, context):
        # Operatorをボタンとして配置する
        draw_layout = self.layout
        # 要素行を作成する
        line_row = draw_layout.row()
        # 最大体積指定用のカスタムプロパティを配置する
        line_row.prop(context.scene.holomon_delete_object_byvolume, "prop_targetmaxvolume")
        # 要素行を作成する
        line_row = draw_layout.row()
        # ポリゴン数削減を実行するボタンを配置する
        line_row.operator(ADDON_OPERATOR_IDNAME)

# Operatorクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html
class HOLOMON_OT_holomon_delete_object_byvolume(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = ADDON_OPERATOR_IDNAME
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "選択オブジェクトの削除"
    # クラスの説明文
    # (マウスオーバー時に表示)
    bl_description = "選択中のオブジェクトを全て削除します"
    # クラスの属性
    # 以下の属性を設定できる
    #   REGISTER      : Operatorを情報ウィンドウに表示し、やり直しツールバーパネルをサポートする
    #   UNDO          : 元に戻すイベントをプッシュする（Operatorのやり直しに必要）
    #   UNDO_GROUPED  : Operatorの繰り返しインスタンスに対して単一の取り消しイベントをプッシュする
    #   BLOCKING      : 他の操作がマウスポインタ―を使用できないようにブロックする
    #   MACRO         : Operatorがマクロであるかどうかを確認するために使用する
    #   GRAB_CURSOR   : 継続的な操作が有効な場合にオペレーターがマウスポインターの動きを参照して、操作を有効にする
    #   GRAB_CURSOR_X : マウスポインターのX軸の動きのみを参照する
    #   GRAB_CURSOR_Y : マウスポインターのY軸の動きのみを参照する
    #   PRESET        : Operator設定を含むプリセットボタンを表示する
    #   INTERNAL      : 検索結果からOperatorを削除する
    # 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.bl_options
    bl_options = {'REGISTER', 'UNDO'}

    # Operator実行時の処理
    def execute(self, context):
        # 選択中のオブジェクトを削除する
        bpy.ops.object.delete()
        
        return {'FINISHED'}

# PropertyGroupクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.PropertyGroup.html
class HOLOMON_PROP_holomon_delete_object_byvolume(PropertyGroup):
    # 最大体積指定の更新時に実行する関数を定義する
    def change_targetmaxvolume(self, context):
        # 最初に全てのオブジェクトの選択状態を解除する
        clear_select_object()
        # 指定された体積を取得する
        target_volume = context.scene.holomon_delete_object_byvolume.prop_targetmaxvolume
        # 体積が指定以下のMeshオブジェクトリストを作成する
        target_objectlist = list()
        for obj in bpy.context.scene.objects:
            if obj.type != 'MESH':
                continue
            if (get_volume_object(obj) <= target_volume):
                target_objectlist.append(obj)
        # オブジェクトリストのオブジェクトを選択状態にする
        select_objectlist(target_objectlist)

    # シーン上のパネルに表示する最大体積指定用のカスタムプロパティを定義する
    prop_targetmaxvolume: FloatProperty(
        name = "削除対象とする体積の上限値",                                       # プロパティ名
        default=0,                                                              # デフォルト値
        description = "削除対象として選択するオブジェクトの体積の上限値を指定します", # 説明文
        update = change_targetmaxvolume,                                        # 更新時実行関数
    )


# 登録に関する処理
# 登録対象のクラス名
regist_classes = (
    HOLOMON_PT_holomon_delete_object_byvolume,
    HOLOMON_OT_holomon_delete_object_byvolume,
    HOLOMON_PROP_holomon_delete_object_byvolume,
)

# 作成クラスと定義の登録メソッド
def register():
    # カスタムクラスを登録する
    for regist_cls in regist_classes:
        bpy.utils.register_class(regist_cls)
    # シーン情報にカスタムプロパティを登録する
    bpy.types.Scene.holomon_delete_object_byvolume = \
      PointerProperty(type=HOLOMON_PROP_holomon_delete_object_byvolume)

# 作成クラスと定義の登録解除メソッド
def unregister():
    # シーン情報のカスタムプロパティを削除する
    del bpy.types.Scene.holomon_delete_object_byvolume
    # カスタムクラスを解除する
    for regist_cls in regist_classes:
        bpy.utils.unregister_class(regist_cls)


# オブジェクトの選択状態をクリアする
def clear_select_object():
    """オブジェクトの選択状態をクリアする

    Keyword Arguments:

    Returns:
    """

    # アクティブなオブジェクトを解除する    
    bpy.context.view_layer.objects.active = None
    # シーン内の全オブジェクトを走査する
    for obj in bpy.context.scene.objects:
        # 選択状態のオブジェクトを非選択状態にする
        if obj.select_get():
            obj.select_set(False)
        
    return

# 指定のオブジェクトを全て選択状態にする
def select_objectlist(arg_targetobjectlist:list):
    """オブジェクトの寸法情報から体積を計算する

    Keyword Arguments:
        arg_targetobjectlist {list} -- 対象オブジェクトリスト

    Returns:
    """
    
    for obj in arg_targetobjectlist:
        # 指定データがオブジェクトでない場合は処理しない
        if isinstance(obj, bpy.types.Object) == False:
            continue
        # 指定のオブジェクトを選択状態にする
        obj.select_set(True)
        
    return

def delete_object():
    """オブジェクトの選択状態をクリアする

    Keyword Arguments:

    Returns:
    """

    # アクティブなオブジェクトを解除する    
    bpy.context.view_layer.objects.active = None
    # シーン内の全オブジェクトを走査する
    for obj in bpy.context.scene.objects:
        # 指定のオブジェクトを非選択状態にする
        obj.select_set(False)
        
    return

# オブジェクトの寸法情報から体積を計算する
def get_volume_object(arg_targetobject:bpy.types.Object) -> float:
    """オブジェクトの寸法情報から体積を計算する

    Keyword Arguments:
        arg_targetobject {bpy.types.Object} -- 対象オブジェクト

    Returns:
        float -- 体積(取得失敗時:0)
    """
    
    # 指定オブジェクトがメッシュか確認する
    if arg_targetobject.type != 'MESH':
        # 指定オブジェクトがMESHでない場合は処理しない
        return 0
        
    # 指定オブジェクトの寸法情報を取得する
    # オブジェクトのインタフェース
    # (https://docs.blender.org/api/current/bpy.types.Object.html)
    target_dimensions = arg_targetobject.dimensions
    # 体積を計算する(X軸の長さ x Y軸の長さ x Z軸の長さ)
    result_volume = target_dimensions[0] * target_dimensions[1] * target_dimensions[2]

    return result_volume

# エディター実行時の処理
if __name__ == "__main__":
    # 作成クラスと定義を登録する
    register()


