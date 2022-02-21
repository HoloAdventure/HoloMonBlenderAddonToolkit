# 定数の定義
ADDON_COMMONNAME = "holomon_control_view"
ADDON_OPERATOR_IDNAME_STATUS = "holomon.show_status"

# 利用するタイプやメソッドのインポート
import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, EnumProperty

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
class HOLOMON_PT_holomon_control_view(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "表示画面のカスタマイズ"
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
        showstats_row = draw_layout.row()
        # ポリゴン情報の表示切替を実行するボタンを配置する
        showstats_row.operator(ADDON_OPERATOR_IDNAME_STATUS)
        # ボックス要素を作成する
        shading_box = draw_layout.box()
        # 要素行を作成する
        shading_row = shading_box.row()
        # テキストを配置する
        shading_row.label(text="シェーディング切替")
        # 要素列を作成する
        shading_column = shading_box.column(align=True)
        # シェーディングタイプの選択肢を配置する
        # row(列)要素に expand=True を指定して EnumProperty を設定すると縦並びに表示される
        shading_column.prop(context.scene.holomon_control_view, "prop_shadingselect", expand=True)

# Operatorクラスの作成（ポリゴン情報表示のためのサブ関数）
# 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html
class HOLOMON_OT_holomon_control_view(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = ADDON_OPERATOR_IDNAME_STATUS
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "ポリゴン情報の表示切替"
    # クラスの説明文
    # (マウスオーバー時に表示)
    bl_description = "3Dビューの統計データ表示を切り替えてオブジェクト数やポリゴン数を表示します"
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
        # 現在の show_status の状態を切り替える
        # 参考URL:https://docs.blender.org/api/2.91/bpy.types.SpaceView3D.html
        # 参考URL:https://docs.blender.org/api/2.91/bpy.types.View3DOverlay.html
        # アドオンは VIEW_3D パネルで実行されているため space_data のアクセス先は SpaceView3D になる
        context_overlay = context.space_data.overlay
        if context_overlay.show_stats:
            context_overlay.show_stats = False
        else:
            context_overlay.show_stats = True
        
        return {'FINISHED'}

# PropertyGroupクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.PropertyGroup.html
class HOLOMON_PROP_holomon_control_view(PropertyGroup):
    # 選択肢の更新時に実行する関数を定義する
    def change_shadingselect(self, context):
        # 指定された選択肢を取得する
        target_shadingselect = context.scene.holomon_control_view.prop_shadingselect
        # 選択したIDを元にシェーディングタイプを設定する
        # (https://docs.blender.org/api/current/bpy.types.View3DShading.html#bpy.types.View3DShading.type)
        if target_shadingselect == "Wireframe":
            context.space_data.shading.type = 'WIREFRAME'
        elif target_shadingselect == "Solid":
            context.space_data.shading.type = 'SOLID'
        elif target_shadingselect == "Material":
            context.space_data.shading.type = 'MATERIAL'

    # シーン上のパネルに表示する選択肢のカスタムプロパティを定義する
    # 選択肢(ID,名前,説明)を作成する
    # EnumPropertyの選択肢要素のマニュアル
    # (https://docs.blender.org/api/current/bpy.props.html#bpy.props.EnumProperty)
    prop_shadingselect: EnumProperty(
        name="シェーディングの選択",                                     # プロパティ名
        items= [
            ("Wireframe","ワイヤーフレーム表示","ワイヤーフレーム表示に切り替え","SHADING_WIRE",0),
            ("Solid","ソリッド表示","ソリッド表示に切り替え","SHADING_SOLID",1),
            ("Material","マテリアル表示","マテリアル表示に切り替え","SHADING_TEXTURE",2),
        ],                                                               # 選択肢
        default="Solid",                                                 # デフォルト値
        description = "3Dビューのシェーディング処理を指定します",          # 説明文
        update = change_shadingselect,                                  # 更新時実行関数
        )


# 登録に関する処理
# 登録対象のクラス名
regist_classes = (
    HOLOMON_PT_holomon_control_view,
    HOLOMON_OT_holomon_control_view,
    HOLOMON_PROP_holomon_control_view,
)

# 作成クラスと定義の登録メソッド
def register():
    # カスタムクラスを登録する
    for regist_cls in regist_classes:
        bpy.utils.register_class(regist_cls)
    # シーン情報にカスタムプロパティを登録する
    bpy.types.Scene.holomon_control_view = \
      PointerProperty(type=HOLOMON_PROP_holomon_control_view)

# 作成クラスと定義の登録解除メソッド
def unregister():
    # カスタムクラスを解除する
    for regist_cls in regist_classes:
        bpy.utils.unregister_class(regist_cls)
    # カスタムクラスを解除する
    for regist_cls in regist_classes:
        bpy.utils.unregister_class(regist_cls)

