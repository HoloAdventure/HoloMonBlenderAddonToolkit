# 定数の定義
ADDON_COMMONNAME = "holomon_decimate_mesh"
ADDON_OPERATOR_IDNAME = "holomon.decimate_mesh"
ADDON_OPERATOR_IDNAME_SUB = "holomon.show_status"

# 利用するタイプやメソッドのインポート
import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, IntProperty

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
class HOLOMON_PT_holomon_decimate_mesh(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "ポリゴン数の削減"
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
        button_row = draw_layout.row()
        # ポリゴン数の表示切替を実行するボタンを配置する
        button_row.operator(ADDON_OPERATOR_IDNAME_SUB)
        # 要素行を作成する
        uvlayername_row = draw_layout.row()
        # 削減後の総ポリゴン数指定用のカスタムプロパティを配置する
        uvlayername_row.prop(context.scene.holomon_decimate_mesh, "prop_targettrianglecount")
        # 要素行を作成する
        uvlayername_row = draw_layout.row()
        # １メッシュ辺りの最低ポリゴン数指定用のカスタムプロパティを配置する
        uvlayername_row.prop(context.scene.holomon_decimate_mesh, "prop_mintrianglecount")
        # 要素行を作成する
        button_row = draw_layout.row()
        # ポリゴン数削減を実行するボタンを配置する
        button_row.operator(ADDON_OPERATOR_IDNAME)

# Operatorクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html
class HOLOMON_OT_holomon_decimate_mesh(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = ADDON_OPERATOR_IDNAME
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "ポリゴン数削減の実行"
    # クラスの説明文
    # (マウスオーバー時に表示)
    bl_description = "全メッシュを対象に指定のポリゴン数までの削減を行います"
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
        # カスタムプロパティから削減後の総ポリゴン数を取得する
        targettrianglecount = context.scene.holomon_decimate_mesh.prop_targettrianglecount
        
        # 削減後の総ポリゴン数をチェックする
        if targettrianglecount <= 0:
            # 削減後の総ポリゴン数が 0 以下ならエラーメッセージを表示する
            self.report({'ERROR'}, "削減後の総ポリゴン数は 1 以上を設定して下さい")
            return {'CANCELLED'}

        # カスタムプロパティから1メッシュ辺りの最低ポリゴン数を取得する
        mintrianglecount = context.scene.holomon_decimate_mesh.prop_mintrianglecount
        
        # 全メッシュを対象に指定のポリゴン数まで削減する
        operator_result = apply_decimate_allmeshcount(
            arg_targettrianglecount=targettrianglecount,
            arg_mintrianglecount=mintrianglecount
        )

        # 実行結果を確認する
        if operator_result == False:
            # 実行に失敗した場合はエラーメッセージを表示する
            self.report({'ERROR'}, "実行に失敗しました")
            return {'CANCELLED'}

        return {'FINISHED'}

# Operatorクラスの作成（ポリゴン数表示のためのサブ関数）
# 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html
class HOLOMON_OT_holomon_show_status(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = ADDON_OPERATOR_IDNAME_SUB
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "ポリゴン数の表示切替"
    # クラスの説明文
    # (マウスオーバー時に表示)
    bl_description = "3Dビューの統計データ表示を切り替えてポリゴン数を表示します"
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
        
        # カスタムプロパティから削減後の総ポリゴン数を取得する
        targettrianglecount = context.scene.holomon_decimate_mesh.prop_targettrianglecount
        
        # 削減後の総ポリゴン数をチェックする
        if targettrianglecount <= 0:
            # 削減後の総ポリゴン数の指定が 0 以下の時、現在の総ポリゴン数を削減後の総ポリゴン(三角面)数に設定する
            context.scene.holomon_decimate_mesh.prop_targettrianglecount = count_alltriangles_mesh()

        return {'FINISHED'}

# PropertyGroupクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.PropertyGroup.html
class HOLOMON_PROP_holomon_decimate_mesh(PropertyGroup):
    # シーン上のパネルに表示する削減後の総ポリゴン数指定用のカスタムプロパティを定義する
    prop_targettrianglecount: IntProperty(
        name = "削減後の総ポリゴン(三角面)数",                   # プロパティ名
        default=0,                                             # デフォルト値
        description = "削減後の総ポリゴン(三角面)数を指定します", # 説明文
    )
    
    # シーン上のパネルに表示する１メッシュ辺りの最低ポリゴン数指定用のカスタムプロパティを定義する
    prop_mintrianglecount: IntProperty(
        name = "1メッシュ辺りの最低ポリゴン数",                   # プロパティ名
        default=0,                                              # デフォルト値
        description = "1メッシュ辺りの最低ポリゴン数を指定します", # 説明文
    )


# 登録に関する処理
# 登録対象のクラス名
regist_classes = (
    HOLOMON_PT_holomon_decimate_mesh,
    HOLOMON_OT_holomon_decimate_mesh,
    HOLOMON_PROP_holomon_decimate_mesh,
    HOLOMON_OT_holomon_show_status,
)

# 作成クラスと定義の登録メソッド
def register():
    # カスタムクラスを登録する
    for regist_cls in regist_classes:
        bpy.utils.register_class(regist_cls)
    # シーン情報にカスタムプロパティを登録する
    bpy.types.Scene.holomon_decimate_mesh = \
      PointerProperty(type=HOLOMON_PROP_holomon_decimate_mesh)

# 作成クラスと定義の登録解除メソッド
def unregister():
    # シーン情報のカスタムプロパティを削除する
    del bpy.types.Scene.holomon_decimate_mesh
    # カスタムクラスを解除する
    for regist_cls in regist_classes:
        bpy.utils.unregister_class(regist_cls)



# 全メッシュを対象に指定のポリゴン数まで削減する
def apply_decimate_allmeshcount(arg_targettrianglecount:int=10000, arg_mintrianglecount:int=0) -> bool:
    """全メッシュを対象に指定のポリゴン数まで削減する

    Keyword Arguments:
        arg_targettrianglecount {int} -- 削減後の指定ポリゴン数 (default: {10000})
        arg_mintrianglecount {int} -- オブジェクトの最低ポリゴン数 (default: {0})

    Returns:
        Bool -- 実行正否
    """

    # 全メッシュの総ポリゴン(三角面)数を取得する
    current_trianglecount = count_alltriangles_mesh()
    # 削減の比率を計算する
    target_ratio = 1.0
    # 指定のポリゴン数より現在のポリゴン数が多いか確認する
    if current_trianglecount > arg_targettrianglecount:
        # 指定のポリゴン数まで削減するための比率を計算する
        target_ratio = arg_targettrianglecount / current_trianglecount
    # 全オブジェクトデータを取得する
    for obj in bpy.data.objects:
        # オブジェクトに反映する削減比率
        obj_ratio = target_ratio
        # オブジェクトのポリゴン数を取得する
        obj_trianglecount = count_triangles_mesh(obj)
        # 対象のオブジェクトが既に最低ポリゴン数を下回っていないかチェックする
        if obj_trianglecount < arg_mintrianglecount:
            # 下回っていれば対象のオブジェクトは処理しない
            continue
        # 削減後に指定の最低ポリゴン数を下回らないかチェックする
        if (obj_trianglecount * target_ratio) < arg_mintrianglecount:
            # 下回るようであれば最低ポリゴン数までの削減比率を再計算する
            obj_ratio = arg_mintrianglecount / obj_trianglecount
        # オブジェクトを指定の比率でポリゴン削減する
        apply_decimate_mesh(arg_targetobject=obj, arg_decimateratio=obj_ratio)
    return True

# 対象オブジェクトを指定の比率でポリゴン削減する
# モディファイア追加の種類とマニュアル
# （https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.gpencil_modifier_add）
def apply_decimate_mesh(arg_targetobject:bpy.types.Object, arg_decimateratio:float=1.0) -> bool:
    """対象オブジェクトを指定の比率でポリゴン削減する

    Keyword Arguments:
        arg_targetobject {bpy.types.Object} -- 対象オブジェクト
        arg_decimateratio {float} -- 削減比率 (default: {1.0})

    Returns:
        Bool -- 実行正否
    """

    # 指定オブジェクトがメッシュか確認する
    if arg_targetobject.type != 'MESH':
        # 指定オブジェクトが存在しない場合は処理しない
        return False
    # 変更オブジェクトをアクティブに変更する
    bpy.context.view_layer.objects.active = arg_targetobject
    # 「ポリゴン数削減」モディファイアを追加する
    # ポリゴン数削減モディファイアのインタフェース
    # (https://docs.blender.org/api/current/bpy.types.DecimateModifier.html)
    bpy.ops.object.modifier_add(type='DECIMATE')
    # 追加されたモディファイアを取得する
    decimate_modifier = arg_targetobject.modifiers[-1]
    # 削減の比率を設定する
    decimate_modifier.ratio = arg_decimateratio
    # 「ポリゴン数削減」モディファイアを適用する
    bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)
    return True

# 指定メッシュの三角面数を取得する
def count_alltriangles_mesh() -> int:
    """全メッシュの総三角面数を取得する
    
    Keyword Arguments:

    Returns:
        int -- 三角面数(取得失敗時:0)
    """

    # 総三角面数のカウンタ
    triangles_count = 0
    # 全メッシュデータを取得する
    for obj in bpy.data.objects:
        # 三角面数を加算する
        triangles_count += count_triangles_mesh(obj)
    return triangles_count

# 指定メッシュの三角面数を取得する
def count_triangles_mesh(arg_object:bpy.types.Object) -> int:
    """指定メッシュの三角面数を取得する
    
    Keyword Arguments:
        arg_objectname {bpy.types.Object} -- 対象オブジェクト

    Returns:
        int -- 三角面数(取得失敗時:0)
    """

    # 指定オブジェクトがメッシュか確認する
    if arg_object.type != 'MESH':
        # 指定オブジェクトが存在しない場合は処理しない
        return 0
    # Meshデータを取得する
    # メッシュアクセスのマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Mesh.html)
    msh = arg_object.data
    # 三角面を計算する(結果はloop_trianglesに保存される)
    msh.calc_loop_triangles()
    # 三角面数を取得する
    triangles_count = len(msh.loop_triangles)
    return triangles_count


