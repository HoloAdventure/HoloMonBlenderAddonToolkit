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
        selecttool_row = draw_box.row()
        # 行内に要素列を作成する
        selecttooltext_column = selecttool_row.column(align=True)
        # 行内にテキストを作成する
        selecttooltext_column.label(text="選択方式")
        # 行内に要素列を作成する
        selecttoolbutton_column = selecttool_row.column(align=True)
        # 行内に要素列を作成する
        selectbox_row = selecttoolbutton_column.column(align=False)
        # 選択方式を切り替えるボタンを配置する
        selectbox_prop = selectbox_row.operator("wm.tool_set_by_id", text="ボックス")
        # 引数を指定する
        selectbox_prop.name = 'builtin.select_box'
        # 行内に要素列を作成する
        selectcircle_row = selecttoolbutton_column.column(align=False)
        # 選択方式を切り替えるボタンを配置する
        selectcircle_prop = selectcircle_row.operator("wm.tool_set_by_id", text="サークル")
        # 引数を指定する
        selectcircle_prop.name = 'builtin.select_circle'
        # 行内に要素列を作成する
        selectlasso_row = selecttoolbutton_column.column(align=False)
        # 選択方式を切り替えるボタンを配置する
        selectlasso_prop = selectlasso_row.operator("wm.tool_set_by_id", text="投げ縄")
        # 引数を指定する
        selectlasso_prop.name = 'builtin.select_lasso'

        # ボックス内に要素行を作成する
        invert_row = draw_box.row()
        # 行内に要素列を作成する
        inverttext_column = invert_row.column(align=True)
        # 行内にテキストを作成する
        inverttext_column.label(text="選択範囲の操作")
        # 行内に要素列を作成する
        invertbutton_column = invert_row.column(align=True)
        # 選択範囲の反転を実行するボタンを配置する
        select_all_prop = invertbutton_column.operator("mesh.select_all", text="反転")
        select_all_prop.action = 'INVERT'
        # 接続部分の選択を実行するボタンを配置する
        select_link_prop = invertbutton_column.operator("mesh.select_linked", text="連続部分")

        # ボックス内に要素行を作成する
        moreless_row = draw_box.row()
        # 行内に要素列を作成する
        text_column = moreless_row.column(align=True)
        # 行内にテキストを作成する
        text_column.label(text="範囲拡縮")
        # 行内に要素列を作成する
        switchbutton_row = moreless_row.row(align=True)
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
        # 行内にテキストを作成する
        ratio_row.label(text="削減比率")
        # 削減比率指定用のカスタムプロパティを配置する
        ratio_row.prop(context.scene.holomon_decimate_vertexselect, "prop_decimateratio")

        # ボックス内に要素行を作成する
        execute_row = draw_box.row()
        # 接続部分の選択を実行するボタンを配置する
        execute_row.operator(ADDON_OPERATOR_IDNAME)

        # 現在のモードが「編集モード(EDIT_MESH)」かチェックする
        if is_editmode() == False:
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
    bl_label = "選択範囲の削減を実行する"
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
        if is_editmode() == False:
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
        name = "",                                   # プロパティ名
        default=1.0,                                 # デフォルト値
        description = "三角面の削減比率を設定する",    # 説明文
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


# 編集モード中の全オブジェクトで選択中の頂点に対して割合を考慮してオブジェクトをリダクションする
def execute_decimate_vertexselect(arg_decimateratio:float) -> bool:
    """編集モード中の全オブジェクトで選択中の頂点に対して割合を考慮してオブジェクトをリダクションする
    頂点を選択していないオブジェクトまたは編集モードでないオブジェクトに対して処理は行わない

    Keyword Arguments:
        arg_decimateratio {float} -- 削減比率

    Returns:
        bool -- 実行成否
    """

    # 現在のモードが編集モードかチェックする
    # （誤操作を防ぐため）
    if is_editmode() == False:
        return False
    # 編集対象のオブジェクトリストを作成する
    targetobject_list = []
    # シーン内の全オブジェクトを走査する
    for check_obj in bpy.context.scene.objects:
        # 編集モード中のオブジェクトを対象とする
        if is_editmode_object(check_obj) == True:
            # 編集モード中であれば頂点グループ作成の対象とする
            targetobject_list.append(check_obj)
    # 対象のオブジェクトがあったか
    if len(targetobject_list) <= 0:
        # 対象のオブジェクトが無かった場合、頂点グループは作成しない
        return True
    # アクティブオブジェクトの参照を退避する
    active_object = bpy.context.view_layer.objects.active
    # オブジェクトモードに移行する
    set_objectmode()
    # 対象のオブジェクトを全て処理する
    for target_obj in targetobject_list:
        # 選択中の頂点があれば頂点グループを作成する
        made_vertexgroup = make_vertexgroup_byselectvert(target_obj)
        # 頂点グループが作成されていれば処理を行う
        if made_vertexgroup != None:
            # 頂点グループの頂点数を考慮した削減比率を再計算する
            vertexgroup_decimeate_ratio = calculate_decimatefactor_onvertexgourp(
                target_obj, made_vertexgroup, arg_decimateratio
            )
            # リダクションを行う
            apply_decimate_vertexgroup(target_obj, made_vertexgroup, vertexgroup_decimeate_ratio)
            # 頂点グループを削除する
            remove_vertexgroup(target_obj, made_vertexgroup)
    # 対象のオブジェクトを全て処理する
    for target_obj in targetobject_list:
        # 処理対象のオブジェクトが編集モードになるよう選択状態とする
        select_object(target_obj)
    # 編集モードに戻す
    set_editmode()
    # アクティブオブジェクトを戻す
    bpy.context.view_layer.objects.active = active_object
    return True

# 選択中の頂点から新規頂点グループを作成して頂点グループを取得する
def make_vertexgroup_byselectvert(arg_object:bpy.types.Object) -> bpy.types.VertexGroup:
    """選択中の頂点から新規頂点グループを作成して頂点グループを取得する

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 対象オブジェクト

    Returns:
        bpy.types.VertexGroup -- 新規頂点グループ
    """

    # 現在のモードがオブジェクトモードかチェックする
    # （VertexGroupのAddは編集モードで実行不可のため）
    if is_objectmode() == False :
        return None
    # 指定オブジェクトがメッシュか確認する
    if arg_object.type != 'MESH':
        # メッシュでない場合は処理しない
        return None
    # インデックスリストを作成する
    index_list = []
    # 全ての頂点を走査する
    # 頂点操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.MeshVertex.html)
    for vert in arg_object.data.vertices:
        # 選択状態か否か
        if vert.select:
            # 選択中の頂点のインデックスをリストに追加する
            index_list.append(vert.index)
    # 選択中の頂点があったか
    if len(index_list) <= 0:
        # 選択中の頂点が無かった場合、頂点グループは作成しない
        return None
    # オブジェクトに新規頂点グループを追加する
    # VertexGroupsアクセスのマニュアル
    # (https://docs.blender.org/api/current/bpy.types.VertexGroups.html)
    vertexgroup = arg_object.vertex_groups.new()
    # 選択中の頂点のインデックスを頂点グループに設定する
    # VertexGroupアクセスのマニュアル
    # (https://docs.blender.org/api/current/bpy.types.VertexGroup.html#bpy.types.VertexGroup)
    vertexgroup.add(index_list, 1.0, 'REPLACE')
    # 作成した頂点グループを返却する
    return vertexgroup

# オブジェクトから指定の頂点グループを削除する
def remove_vertexgroup(arg_object:bpy.types.Object, arg_vertexgroup:bpy.types.VertexGroup) -> bool:
    """オブジェクトから指定の頂点グループを削除する

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 対象オブジェクト
        arg_vertexgroup {bpy.types.VertexGroup} -- 指定の頂点グループ

    Returns:
        bool -- 実行成否
    """
    
    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup.name)
    if check_vertexgroup == None:
        return False
    # 頂点グループを削除する
    arg_object.vertex_groups.remove(check_vertexgroup)
    # 実行成否を返却する
    return True

# 指定のオブジェクトを選択状態にする
def select_object(arg_object:bpy.types.Object) -> bool:
    """指定のオブジェクトを選択状態にする

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 対象オブジェクト

    Returns:
        bool -- 実行成否
    """
    
    # 指定のオブジェクトを選択状態にする
    arg_object.select_set(True)
    # 実行成否を返却する
    return True

# 頂点グループを指定してポリゴン数削減モディファイアを適用する
def apply_decimate_vertexgroup(
    arg_object:bpy.types.Object,
    arg_vertexgroup:bpy.types.VertexGroup,
    arg_decimateratio:float) -> bool:
    """頂点グループを指定してポリゴン数削減モディファイアを適用する

    Keyword Arguments:
        arg_object (bpy.types.Object) -- 指定オブジェクト
        arg_vertexgroup {bpy.types.VertexGroup} -- 指定の頂点グループ
        arg_decimateratio {float} -- 削減比率

    Returns:
        bool -- 実行成否
    """

    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup.name)
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
    decimate_modifier.vertex_group = check_vertexgroup.name
    # 「ポリゴン数削減」モディファイアを適用する
    bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)
    # 実行成否を返却する
    return True

# 頂点グループの頂点数に対応する削減比率を再計算する
def calculate_decimatefactor_onvertexgourp(
    arg_object:bpy.types.Object,
    arg_vertexgroup:bpy.types.VertexGroup,
    arg_decimateratio:float) -> float:
    """頂点グループの頂点数に対応する削減比率を再計算する

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 指定オブジェクト
        arg_vertexgroup {bpy.types.VertexGroup} -- 指定の頂点グループ
        arg_decimateratio {float} -- 削減比率

    Returns:
        float -- 再計算後の削減比率
    """

    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup.name)
    if check_vertexgroup == None:
        return 1.0
    # 指定オブジェクトがメッシュか確認する
    if arg_object.type != 'MESH':
        # メッシュが存在しない場合は処理しない
        return arg_decimateratio
    # 頂点グループの参照から頂点グループに所属している頂点数を算出つする
    vertexgroup_count = count_weight_vertexgroup(arg_object, check_vertexgroup)
    # 全体の頂点数を確認する
    vertex_count = count_data_vertex(arg_object)
    # 頂点グループの割合を算出する
    vertexgroup_ratio = vertexgroup_count / vertex_count
    # 頂点グループの割合を考慮して削減比率を再計算する
    vertexgroup_decimateratio = 1.0 - ((1.0 - arg_decimateratio) * vertexgroup_ratio)
    # 再計算後の削減比率を返す
    return vertexgroup_decimateratio

# 指定のオブジェクトの頂点の数を取得する
def count_data_vertex(arg_object:bpy.types.Object) -> int:
    """指定のオブジェクトの頂点の数を取得する

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 指定オブジェクト

    Returns:
        int -- 頂点数
    """

    # データに保持されている頂点の数を返却する
    return len(arg_object.data.vertices)

# 指定の頂点グループに所属している頂点の数を取得する(頂点グループの参照から算出)
def count_weight_vertexgroup(
    arg_object:bpy.types.Object,
     arg_vertexgroup:bpy.types.VertexGroup) -> int:
    """指定の頂点グループに所属している頂点の数を取得する(頂点グループの参照から算出)

    Keyword Arguments:
        arg_object {bpy.types.Object} -- 指定オブジェクト
        arg_vertexgroup {bpy.types.VertexGroup} -- 指定の頂点グループ

    Returns:
        int -- 頂点グループに含まれる頂点数
    """

    # 指定オブジェクトに指定の頂点グループが含まれるかチェックする
    check_vertexgroup = arg_object.vertex_groups.get(arg_vertexgroup.name)
    if check_vertexgroup == None:
        return 0
    # カウント用変数
    result_count = 0
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

# 指定のオブジェクトが編集モードかチェックする
def is_editmode_object(arg_object:bpy.types.Object) -> bool:
    """指定のオブジェクトが編集モードかチェックする
    
    Keyword Arguments:
        arg_object {bpy.types.Object} -- 対象オブジェクト

    Returns:
        bool -- 編集モードか否か
    """

    # オブジェクト毎のモードをチェックする
    # (https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.mode)
    return ('EDIT' == arg_object.mode)

# オブジェクトモードに移行する
def set_objectmode():
    """オブジェクトモードに移行する

    Keyword Arguments:

    Returns:
    """

    # オブジェクトモードに移行する
    # モード切替のマニュアル
    # (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    return

# 現在のモードがオブジェクトモードかチェックする
def is_objectmode() -> bool:
    """現在のモードがオブジェクトモードかチェックする

    Keyword Arguments:

    Returns:
        bool -- オブジェクトモードか否か
    """

    # 現在のモードをチェックする
    # (https://docs.blender.org/api/current/bpy.context.html#bpy.context.mode)
    return ('OBJECT' == bpy.context.mode)

# 編集モードに移行する
def set_editmode():
    """編集モードに移行する

    Keyword Arguments:

    Returns:
    """

    # 編集モードに移行する
    # モード切替のマニュアル
    # (https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.mode_set)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    return

# 現在のモードが編集モードかチェックする
def is_editmode() -> bool:
    """現在のモードが編集モードかチェックする

    Keyword Arguments:

    Returns:
        bool -- 編集モードか否か
    """

    # 現在のモードをチェックする
    # (https://docs.blender.org/api/current/bpy.context.html#bpy.context.mode)
    return ('EDIT_MESH' == bpy.context.mode)


