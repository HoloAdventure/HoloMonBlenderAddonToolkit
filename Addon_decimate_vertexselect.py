# 定数の定義
ADDON_COMMONNAME = "holomon_decimate_vertexselect"
ADDON_OPERATOR_IDNAME = "holomon.decimate_vertexselect"

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
class HOLOMON_PT_holomon_decimate_vertexselect(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "指定範囲のポリゴン削減(編集モード)"
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
    bl_order = 3
    # パネルのカテゴリ名称を定義する
    # 3Dビューポートの場合、サイドバーの名称になる
    # デフォルトは名称無し
    bl_category = "HMToolkit"
 
    # 描画の定義
    def draw(self, context):
        # Operatorをボタンとして配置する
        draw_layout = self.layout
        # ボックス要素を作成する
        draw_box = draw_layout.box()
        # ボックス内に要素行を作成する
        invert_row = draw_box.row()
        # 選択範囲の反転を実行するボタンを配置する
        select_all_prop = invert_row.operator("mesh.select_all", text="選択範囲の反転")
        select_all_prop.action = 'INVERT'
        # ボックス内に要素行を作成する
        link_row = draw_box.row()
        # 接続部分の選択を実行するボタンを配置する
        link_row.operator("mesh.select_linked", text="接続部分の選択")
        # ボックス内に要素行を作成する
        moreless_column = draw_box.row()
        # 行内に要素列を作成する
        text_row = moreless_column.column(align=True)
        # 行内にテキストを作成する
        text_row.label(text="範囲拡縮")
        # 行内に要素列を作成する
        switchbutton_column = moreless_column.column(align=True)
        # 更に分割する
        switchbutton_row = switchbutton_column.row()
        # 行内に要素列を作成する
        more_row = switchbutton_row.column(align=False)
        # 範囲拡大を実行するボタンを配置する
        more_row.operator("mesh.select_more", text="＋")
        # 行内に要素列を作成する
        less_row = switchbutton_row.column(align=False)
        # 範囲拡大を実行するボタンを配置する
        less_row.operator("mesh.select_less", text="－")
        # ボックス内に要素行を作成する
        ratio_row = draw_box.row()
        # 削減比率指定用のカスタムプロパティを配置する
        ratio_row.prop(context.scene.holomon_decimate_vertexselect, "prop_decimateratio")
        # ボックス内に要素行を作成する
        execute_row = draw_box.row()
        # 接続部分の選択を実行するボタンを配置する
        execute_row.operator(ADDON_OPERATOR_IDNAME)
        # 現在のモードが「編集モード(EDIT_MESH)」かチェックする
        if check_viewmode('EDIT_MESH') == False:
            # 「編集モード(EDIT_MESH)」でない場合
            # ボックス要素を無効化する
            draw_box.enabled = False

# Operatorクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html
class HOLOMON_OT_holomon_decimate_vertexselect(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = ADDON_OPERATOR_IDNAME
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "選択範囲の削減を実行"
    # クラスの説明文
    # (マウスオーバー時に表示)
    bl_description = "現在の選択範囲に対してポリゴン数削減を行います"
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
        # 現在のモードが「編集モード(EDIT_MESH)」かチェックする
        if check_viewmode('EDIT_MESH') == False:
            # 「編集モード(EDIT_MESH)」でない場合処理しない
            return {'CANCELLED'}

        # カスタムプロパティから指定中の削減比率を取得する
        decimate_ratio = context.scene.holomon_decimate_vertexselect.prop_decimateratio

        # 選択頂点に対するポリゴン数削減を実行する
        result = execute_decimate_vertexselect(arg_decimateratio=decimate_ratio)

        # 実行結果をチェックする
        if result == False:
            # 実行に失敗した場合はエラーメッセージを表示する
            self.report({'ERROR'}, "実行に失敗しました")
            return {'CANCELLED'}

        return {'FINISHED'}

# PropertyGroupクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.PropertyGroup.html
class HOLOMON_PROP_holomon_decimate_vertexselect(PropertyGroup):
    # プロパティ設定のマニュアル
    # (https://docs.blender.org/api/current/bpy.props.html)
    
    # 削減比率指定用のカスタムプロパティを定義する
    prop_decimateratio: FloatProperty(
        name = "削減する参画面の割合",                 # プロパティ名
        default=1.0,                                  # デフォルト値
        description = "ポリゴンの削減比率を設定する",  # 説明文
    )

# 登録に関する処理
# 登録対象のクラス名
regist_classes = (
    HOLOMON_PT_holomon_decimate_vertexselect,
    HOLOMON_OT_holomon_decimate_vertexselect,
    HOLOMON_PROP_holomon_decimate_vertexselect,
)

# 作成クラスと定義の登録メソッド
def register():
    # カスタムクラスを登録する
    for regist_cls in regist_classes:
        bpy.utils.register_class(regist_cls)
    # シーン情報にカスタムプロパティを登録する
    bpy.types.Scene.holomon_decimate_vertexselect = PointerProperty(type=HOLOMON_PROP_holomon_decimate_vertexselect)


# 作成クラスと定義の登録解除メソッド
def unregister():
    # シーン情報のカスタムプロパティを削除する
    del bpy.types.Scene.holomon_decimate_vertexselect
    # カスタムクラスを解除する
    for regist_cls in regist_classes:
        bpy.utils.unregister_class(regist_cls)


def execute_decimate_vertexselect(arg_decimateratio:float) -> bool:
    """選択頂点に対するポリゴン数削減を実行する

    Keyword Arguments:
        arg_decimateratio {float} -- 指定の削減比率

    Returns:
        bool -- 実行成否
    """

    # 現在のモードが「編集モード(EDIT_MESH)」かチェックする
    if check_viewmode('EDIT_MESH') == False :
        return False
    # 対象となる現在編集中のアクティブオブジェクトの参照を取得する
    target_object = bpy.context.view_layer.objects.active
    # 頂点の削減比率を指定する
    decimate_ratio = arg_decimateratio
    # 選択中の頂点から新規頂点グループを作成して頂点グループを取得する
    made_vertexgroup = make_vertexgroup()
    # 頂点グループの頂点数を考慮した削減比率を再計算する
    vertexgroup_decimeate_ratio = calculate_decimatefactor_onvertexgourp(
        target_object, made_vertexgroup.name, decimate_ratio
    )
    # モディファイアを設定するためオブジェクトモードに切り替える
    set_mode_object()
    # リダクションを行う
    decimate_result = apply_decimate_vertexgroup(
        target_object, made_vertexgroup.name, vertexgroup_decimeate_ratio
    )
    if decimate_result == False :
        return False
    # 使用した頂点グループを削除する
    delete_vertexgroup(target_object, made_vertexgroup.name)
    # モードを編集モードに戻す
    set_mode_edit()
    
    return True

def apply_decimate_vertexgroup(
    arg_object:bpy.types.Object,
    arg_vertexgroup_name:str,
    arg_decimateratio:float) -> bool:
    """頂点グループを指定してポリゴン数削減モディファイアを適用する

    Keyword Arguments:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_vertexgroup_name {str} -- 指定の頂点グループ名
        arg_decimateratio {float} -- 削減比率

    Returns:
        bool -- 実行成否
    """

    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup_name)
    if check_vertexgroup == None:
        return False
    # 指定オブジェクトがメッシュか確認する
    if arg_object.type != 'MESH':
        # メッシュが存在しない場合は処理しない
        return False
    # 変更オブジェクトをアクティブに変更する
    bpy.context.view_layer.objects.active = arg_object
    # 「ポリゴン数削減」モディファイアを追加する
    # モディファイア追加の種類とマニュアル
    # （https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.gpencil_modifier_add）
    # ポリゴン数削減モディファイアのインタフェース
    # (https://docs.blender.org/api/current/bpy.types.DecimateModifier.html)
    bpy.ops.object.modifier_add(type='DECIMATE')
    # 追加されたモディファイアを取得する
    decimate_modifier = arg_object.modifiers[-1]
    # 削減のタイプを COLLAPSE に指定する
    decimate_modifier.decimate_type = 'COLLAPSE'
    # 削減の比率を設定する
    decimate_modifier.ratio = arg_decimateratio
    # 頂点グループを指定する
    decimate_modifier.vertex_group = arg_vertexgroup_name
    # 「ポリゴン数削減」モディファイアを適用する
    bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)
    
    # 実行成否を返却する
    return True

def calculate_decimatefactor_onvertexgourp(
    arg_object:bpy.types.Object,
    arg_vertexgroup_name:str,
    arg_decimateratio:float) -> float:
    """頂点グループの頂点数に対応する削減比率を再計算する

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 指定オブジェクト
        arg_vertexgroup_name {str} -- 指定の頂点グループ名
        arg_decimateratio {float} -- 削減比率

    Returns:
        float -- 再計算後の削減比率
    """

    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup_name)
    if check_vertexgroup == None:
        return arg_decimateratio
    # 指定オブジェクトがメッシュか確認する
    if arg_object.type != 'MESH':
        # メッシュが存在しない場合は処理しない
        return arg_decimateratio
    # 頂点グループの参照から頂点グループに所属している頂点数を算出つする
    vertexgroup_count = count_weight_vertexgroup(arg_object, arg_vertexgroup_name)
    # 全体の頂点数を確認する
    vertex_count = count_data_vertex(arg_object)
    # 頂点グループの割合を算出する
    vertexgroup_ratio = vertexgroup_count / vertex_count
    # 頂点グループの割合を考慮して削減比率を再計算する
    vertexgroup_decimateratio = 1.0 - ((1.0 - arg_decimateratio) * vertexgroup_ratio)

    return vertexgroup_decimateratio

def delete_vertexgroup(arg_object:bpy.types.Object, arg_vertexgroup_name:str) -> bool:
    """指定の頂点グループを削除する

    Keyword Arguments:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_vertexgroup_name {str} -- 指定の頂点グループ名

    Returns:
        bool -- 実行成否
    """

    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup_name)
    if check_vertexgroup == None:
        return False
    # 指定頂点グループをアクティブにする
    arg_object.vertex_groups.active_index = check_vertexgroup.index
    # 指定頂点グループを削除する
    bpy.ops.object.vertex_group_remove(all=False)

    return True

def count_data_vertex(arg_object:bpy.types.Object) -> int:
    """指定のオブジェクトの頂点の数を取得する

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 指定オブジェクト

    Returns:
        int -- 頂点数
    """

    # データに保持されている頂点の数を返却する
    return len(arg_object.data.vertices)

def count_weight_vertexgroup(
    arg_object:bpy.types.Object, arg_vertexgroup_name:str) -> int:
    """指定の頂点グループに所属している頂点の数を取得する(頂点グループの参照から算出)

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 指定オブジェクト
        arg_vertexgroup_name {str} -- 指定の頂点グループ名

    Returns:
        int -- 頂点グループに含まれる頂点数
    """

    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup_name)
    if check_vertexgroup == None:
        return 0
    # カウント用変数
    result_count = 0
    # 指定の頂点グループについて頂点グループリストでのインデックス番号を取得する
    check_vertexgroup_index = check_vertexgroup.index
    # 指定オブジェクトの全頂点を走査する
    for vert in arg_object.data.vertices:
        try:
            # ウェイト情報を参照できるならカウントアップする
            check_vertexgroup.weight(vert.index)
            result_count = result_count + 1
        except RuntimeError:
            # 頂点グループに所属していない場合はエラーが発生するのでパスする
            pass
    # カウント結果を返却する
    return result_count

# オブジェクトモードへの移行
# モード切替のマニュアル
# (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
def set_mode_object() -> bool:
    """オブジェクトモードへの移行

    Returns:
        bool -- 実行の正否
    """

    # オブジェクトモードに移行する
    # モード切替のマニュアル
    # (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
    # mode:OBJECT オブジェクトモードに切り替え
    # toggle:True の場合、既に編集モードの時、オブジェクトモードに戻る
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    return True

# 編集モードへの移行
# モード切替のマニュアル
# (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
def set_mode_edit() -> bool:
    """編集モードへの移行

    Returns:
        bool -- 実行の正否
    """

    # 編集モードに移行する
    # モード切替のマニュアル
    # (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
    # mode:EDIT 編集モードに切り替え
    # toggle:True の場合、既に編集モードの時、オブジェクトモードに戻る
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    return True

# 選択中の頂点から新規頂点グループを作成して頂点グループを取得する
def make_vertexgroup() -> bpy.types.VertexGroup:
    """選択中の頂点から新規頂点グループを作成して頂点グループを取得する

    Keyword Arguments:

    Returns:
        bpy.types.VertexGroup -- 新規頂点グループ
    """

    # 現在のモードが「編集モード(EDIT_MESH)」かチェックする
    if check_viewmode('EDIT_MESH') == False :
        return ""
    # 編集中のアクティブオブジェクトを取得する
    active_object = bpy.context.view_layer.objects.active
    # 選択中の頂点に新規頂点グループを割り当てる
    bpy.ops.object.vertex_group_assign_new()
    # 作成した頂点グループのインデックス番号を取得する
    make_index = active_object.vertex_groups.active_index
    # 作成した頂点グループの頂点グループを返却する
    return active_object.vertex_groups[make_index]

# 現在のモードが指定のモードかチェックする
def check_viewmode(arg_checktype:str) -> bool:
    """現在のモードが指定のモードかチェックする

    Keyword Arguments:
        arg_checktype {str} -- 比較するモード名

    Returns:
        str -- 現在のモード
    """

    # 現在のモードをチェックする
    # (https://docs.blender.org/api/current/bpy.context.html#bpy.context.mode)
    modetype = bpy.context.mode
    return (arg_checktype == modetype)


