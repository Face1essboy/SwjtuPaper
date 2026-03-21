#!/usr/bin/env python3
"""Generate Chapter 5 vector figures as PDF files."""

from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "figures" / "chap05"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

CN_FONT = "STSong-Light"
EN_BOLD = "Helvetica-Bold"
EN_FONT = "Helvetica"

NAVY = HexColor("#1F3B67")
BLUE = HexColor("#335C9A")
SKY = HexColor("#5E8BC1")
TEXT = HexColor("#233244")
MUTED = HexColor("#637083")
LINE = HexColor("#6B7A90")
LIGHT_BLUE = HexColor("#EAF1FB")
LIGHT_CYAN = HexColor("#E8F6F4")
LIGHT_ORANGE = HexColor("#FCEFD9")
LIGHT_GRAY = HexColor("#F4F6F8")
LIGHT_GREEN = HexColor("#EAF6EA")
LIGHT_RED = HexColor("#FCE8E6")


def new_canvas(name: str, width: int, height: int) -> canvas.Canvas:
    c = canvas.Canvas(str(OUT_DIR / name), pagesize=(width, height))
    c.setTitle(name)
    c.setAuthor("Codex")
    c.setStrokeColor(LINE)
    c.setFillColor(TEXT)
    return c


def draw_round_box(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    lines: list[str] | None = None,
    *,
    fill: Color = LIGHT_BLUE,
    stroke: Color = LINE,
    title_fill: Color = NAVY,
    body_fill: Color = TEXT,
    radius: int = 12,
    title_size: int = 12,
    body_size: int = 9,
    title_height: int = 24,
    title_font: str = CN_FONT,
    body_font: str = CN_FONT,
    align: str = "center",
) -> None:
    lines = lines or []
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

    c.setFillColor(title_fill)
    c.setFont(title_font, title_size)
    tx = x + w / 2 if align == "center" else x + 10
    if align == "center":
        c.drawCentredString(tx, y + h - title_height / 2 - 3, title)
    else:
        c.drawString(tx, y + h - title_height / 2 - 3, title)

    if lines:
        c.setFillColor(body_fill)
        c.setFont(body_font, body_size)
        line_y = y + h - title_height - 12
        leading = body_size + 4
        for line in lines:
            if align == "center":
                c.drawCentredString(x + w / 2, line_y, line)
            else:
                c.drawString(x + 10, line_y, line)
            line_y -= leading


def draw_text(
    c: canvas.Canvas,
    x: float,
    y: float,
    lines: list[str],
    *,
    font: str = CN_FONT,
    size: int = 9,
    fill: Color = TEXT,
    leading: int | None = None,
    align: str = "left",
) -> None:
    leading = leading or size + 3
    c.setFont(font, size)
    c.setFillColor(fill)
    current_y = y
    for line in lines:
        if align == "center":
            c.drawCentredString(x, current_y, line)
        else:
            c.drawString(x, current_y, line)
        current_y -= leading


def draw_badge(
    c: canvas.Canvas,
    x: float,
    y: float,
    text: str,
    *,
    fill: Color = BLUE,
    font_size: int = 8,
    padding_x: int = 6,
    padding_y: int = 3,
) -> None:
    width = max(42, len(text) * font_size + padding_x * 2)
    height = font_size + padding_y * 2 + 2
    c.setFillColor(fill)
    c.setStrokeColor(fill)
    c.roundRect(x, y, width, height, 7, fill=1, stroke=0)
    c.setFont(CN_FONT, font_size)
    c.setFillColor(white)
    c.drawCentredString(x + width / 2, y + padding_y + 1, text)


def draw_arrow(
    c: canvas.Canvas,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: Color = BLUE,
    label: str | None = None,
    label_dx: float = 0,
    label_dy: float = 0,
    dashed: bool = False,
    arrow_size: int = 7,
    width: float = 1.4,
    font_size: int = 8,
) -> None:
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(width)
    if dashed:
        c.setDash(5, 3)
    c.line(x1, y1, x2, y2)
    angle = math.atan2(y2 - y1, x2 - x1)
    left = (
        x2 - arrow_size * math.cos(angle - math.pi / 6),
        y2 - arrow_size * math.sin(angle - math.pi / 6),
    )
    right = (
        x2 - arrow_size * math.cos(angle + math.pi / 6),
        y2 - arrow_size * math.sin(angle + math.pi / 6),
    )
    path = c.beginPath()
    path.moveTo(x2, y2)
    path.lineTo(left[0], left[1])
    path.lineTo(right[0], right[1])
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.restoreState()

    if label:
        c.setFont(CN_FONT, font_size)
        c.setFillColor(color)
        mx = (x1 + x2) / 2 + label_dx
        my = (y1 + y2) / 2 + label_dy
        c.drawCentredString(mx, my, label)


def draw_dashed_line(
    c: canvas.Canvas,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: Color = LINE,
    width: float = 1.0,
) -> None:
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.setDash(4, 3)
    c.line(x1, y1, x2, y2)
    c.restoreState()


def draw_layer(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    *,
    fill: Color,
    modules: list[tuple[float, float, float, float, str, list[str], Color]],
) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 14, fill=1, stroke=1)
    draw_badge(c, x + 12, y + h - 30, label, fill=NAVY, font_size=9)
    for mx, my, mw, mh, title, lines, box_fill in modules:
        draw_round_box(
            c,
            mx,
            my,
            mw,
            mh,
            title,
            lines,
            fill=box_fill,
            body_size=8,
            title_size=10,
        )


def fig_architecture() -> None:
    c = new_canvas("fig5-1_system_architecture.pdf", 1020, 660)

    draw_layer(
        c,
        40,
        520,
        940,
        100,
        "表示层",
        fill=HexColor("#F6F8FB"),
        modules=[
            (100, 545, 180, 52, "自然语言输入", ["问数输入", "追问触发"], LIGHT_BLUE),
            (315, 545, 180, 52, "SQL与查询结果展示", ["SQL查看", "表格结果"], LIGHT_BLUE),
            (530, 545, 180, 52, "分析结果展示", ["图表可视化", "文字洞察"], LIGHT_BLUE),
            (745, 545, 180, 52, "历史与追溯入口", ["会话切换", "日志回看"], LIGHT_BLUE),
        ],
    )

    draw_layer(
        c,
        40,
        400,
        940,
        95,
        "应用层",
        fill=HexColor("#F8FAFC"),
        modules=[
            (115, 423, 160, 48, "API接入", ["请求解析", "统一响应"], LIGHT_GRAY),
            (310, 423, 160, 48, "会话管理", ["session摘要", "多轮继承"], LIGHT_GRAY),
            (505, 423, 160, 48, "任务管理", ["任务状态", "结果分发"], LIGHT_GRAY),
            (700, 423, 160, 48, "权限与校验", ["访问控制", "参数检查"], LIGHT_GRAY),
        ],
    )

    draw_layer(
        c,
        40,
        250,
        940,
        125,
        "智能服务层",
        fill=HexColor("#F5F9FF"),
        modules=[
            (85, 280, 160, 64, "调度代理", ["意图识别", "任务路由", "流程编排"], LIGHT_ORANGE),
            (290, 270, 210, 82, "查询代理", ["LA-Schema构建", "双路候选生成", "修复与判别"], LIGHT_BLUE),
            (535, 270, 210, 82, "分析代理", ["AP-Schema规划", "查询增强取数", "算子链执行"], LIGHT_CYAN),
            (780, 280, 150, 64, "结果组织代理", ["ResultPackage封装", "图表/表格/洞察整合"], LIGHT_GREEN),
        ],
    )
    draw_badge(c, 345, 352, "第三章方法", fill=SKY, font_size=8)
    draw_badge(c, 590, 352, "第四章方法", fill=SKY, font_size=8)

    draw_layer(
        c,
        40,
        40,
        940,
        185,
        "数据层",
        fill=HexColor("#FCFCFD"),
        modules=[
            (85, 130, 145, 64, "政务业务库", ["财政/项目/公共资源", "原始业务数据"], LIGHT_ORANGE),
            (260, 130, 155, 64, "系统元数据库", ["session/task", "artifact/log"], LIGHT_GRAY),
            (445, 130, 145, 64, "领域知识库", ["K={B,L,V}", "业务术语与逻辑"], LIGHT_BLUE),
            (620, 130, 145, 64, "向量/样例库", ["Milvus", "动态样例库F"], LIGHT_CYAN),
            (795, 130, 145, 64, "缓存与产物存储", ["Redis热点缓存", "图表与导出文件"], LIGHT_GREEN),
        ],
    )

    for x in (180, 390, 605, 820):
        draw_arrow(c, x, 520, x, 495, label=None, color=LINE, width=1.1)
        draw_arrow(c, x, 400, x, 375, label=None, color=LINE, width=1.1)

    draw_arrow(c, 500, 310, 535, 310, label="分析复用查询服务", label_dy=8, color=BLUE)
    draw_arrow(c, 190, 250, 190, 225, color=LINE, width=1.1)
    draw_arrow(c, 370, 250, 370, 225, color=LINE, width=1.1)
    draw_arrow(c, 640, 250, 640, 225, color=LINE, width=1.1)
    draw_arrow(c, 855, 250, 855, 225, color=LINE, width=1.1)

    c.save()


def fig_dual_flow() -> None:
    c = new_canvas("fig5-2_dual_workflow.pdf", 1140, 600)

    draw_round_box(
        c,
        30,
        500,
        150,
        56,
        "用户请求",
        ["自然语言问数或分析需求"],
        fill=LIGHT_ORANGE,
        body_size=8,
    )
    draw_round_box(
        c,
        210,
        500,
        140,
        56,
        "调度代理",
        ["任务识别", "上下文注入"],
        fill=LIGHT_BLUE,
        body_size=8,
    )
    draw_arrow(c, 180, 528, 210, 528, color=BLUE)

    c.setFont(CN_FONT, 12)
    c.setFillColor(NAVY)
    c.drawString(38, 455, "查询流程")
    c.drawString(38, 230, "分析流程")
    c.setStrokeColor(HexColor("#D0D7E2"))
    c.setLineWidth(1)
    c.line(32, 438, 1105, 438)

    top_titles = [
        ("LA-Schema构建", ["模式链接", "知识注入"]),
        ("双路候选生成", ["逻辑映射生成器", "渐进分治生成器"]),
        ("查询修复", ["执行反馈", "至多三轮修复"]),
        ("候选判别", ["配对比较", "最优SQL选择"]),
        ("SQL执行", ["正式取数", "生成结果表"]),
        ("结果返回与日志落库", ["返回final_sql/result_table", "写入artifact/log"]),
    ]
    x = 60
    top_centers = []
    for title, lines in top_titles:
        w = 160 if title != "结果返回与日志落库" else 190
        draw_round_box(c, x, 325, w, 78, title, lines, fill=LIGHT_BLUE, body_size=8, title_size=10)
        top_centers.append((x + w / 2, 364))
        x += w + 20

    draw_arrow(c, 280, 500, top_centers[0][0], 403, color=BLUE, label="查询类任务", label_dy=10)
    for i in range(len(top_centers) - 1):
        draw_arrow(c, top_centers[i][0] + 80, 364, top_centers[i + 1][0] - 80, 364, color=BLUE)

    draw_round_box(
        c,
        430,
        415,
        260,
        60,
        "共享查询服务",
        ["由第三章方法统一完成LA-Schema、候选生成、修复与判别"],
        fill=LIGHT_GRAY,
        body_size=8,
        title_size=10,
    )

    bottom_titles = [
        ("AP-Schema构建", ["识别T/M/D/F/G", "生成JSON化任务规划"]),
        ("Q_A / P_A投影", ["抽取查询约束", "抽取分析操作"]),
        ("调用查询服务取数", ["组装受约束子问题", "返回D=<X,Γ,σ>"]),
        ("分析算子链执行", ["排序/占比/透视", "图表规格校正"]),
        ("结果生成", ["charts/tables/insights", "封装ResultPackage"]),
    ]
    x = 90
    bottom_centers = []
    widths = [170, 160, 180, 170, 170]
    for (title, lines), w in zip(bottom_titles, widths):
        draw_round_box(c, x, 120, w, 84, title, lines, fill=LIGHT_CYAN, body_size=8, title_size=10)
        bottom_centers.append((x + w / 2, 162))
        x += w + 28

    draw_arrow(c, 280, 500, bottom_centers[0][0], 204, color=SKY, label="分析类任务", label_dy=-12)
    for i in range(len(bottom_centers) - 1):
        draw_arrow(c, bottom_centers[i][0] + widths[i] / 2, 162, bottom_centers[i + 1][0] - widths[i + 1] / 2, 162, color=SKY)

    draw_arrow(
        c,
        bottom_centers[2][0],
        204,
        560,
        415,
        color=SKY,
        dashed=True,
        label="复用查询服务",
        label_dx=16,
        label_dy=6,
    )

    c.save()


def fig_agents_context() -> None:
    c = new_canvas("fig5-3_agent_context.pdf", 1020, 600)

    draw_round_box(
        c,
        365,
        225,
        290,
        150,
        "会话上下文中心",
        [
            "history_summary",
            "recent_sql",
            "recent_result_digest",
            "ap_schema_digest",
            "user_feedback / selected_constraints",
        ],
        fill=LIGHT_GRAY,
        align="left",
        body_size=9,
        title_size=12,
    )

    draw_round_box(c, 410, 470, 200, 74, "调度代理", ["意图分类", "任务路由", "结果汇总"], fill=LIGHT_ORANGE, body_size=9)
    draw_round_box(c, 105, 300, 200, 84, "查询代理", ["第三章完整查询管线", "输出final_sql与result_table"], fill=LIGHT_BLUE, body_size=9)
    draw_round_box(c, 715, 300, 200, 84, "分析代理", ["第四章规划与算子执行", "内部调用查询代理取数"], fill=LIGHT_CYAN, body_size=9)
    draw_round_box(c, 395, 60, 230, 84, "结果组织代理", ["统一封装charts/tables/insights/logs", "面向前端输出ResultPackage"], fill=LIGHT_GREEN, body_size=9)
    draw_round_box(c, 40, 470, 230, 60, "领域知识与样例支撑", ["K={B,L,V}    动态样例库F"], fill=LIGHT_BLUE, body_size=9)
    draw_round_box(c, 748, 470, 220, 60, "业务数据与系统存储", ["政务业务库 / 元数据库 / 缓存"], fill=LIGHT_ORANGE, body_size=9)
    draw_round_box(c, 35, 90, 250, 72, "前端与应用层", ["自然语言请求、会话切换、结果查看"], fill=LIGHT_GRAY, body_size=9)

    draw_arrow(c, 285, 126, 395, 126, color=BLUE, label="请求进入", label_dy=10)
    draw_arrow(c, 510, 144, 510, 225, color=LINE)
    draw_arrow(c, 510, 470, 510, 375, color=BLUE, label="读写上下文", label_dx=55)
    draw_arrow(c, 305, 342, 365, 320, color=SKY, label="写入查询结果摘要", label_dy=10)
    draw_arrow(c, 655, 320, 715, 342, color=SKY, label="读取历史状态", label_dy=10)
    draw_arrow(c, 305, 342, 410, 507, color=BLUE, label="受调度执行", label_dx=-10, label_dy=10)
    draw_arrow(c, 610, 507, 715, 342, color=BLUE, label="分析任务路由", label_dx=12)
    draw_arrow(c, 715, 286, 305, 286, color=BLUE, label="分析代理调用查询代理取数", label_dy=10)
    draw_arrow(c, 205, 470, 205, 384, color=LINE, dashed=True, label="知识增强", label_dx=-28, label_dy=8)
    draw_arrow(c, 858, 470, 858, 384, color=LINE, dashed=True, label="数据读写", label_dx=30, label_dy=8)
    draw_arrow(c, 510, 225, 510, 144, color=LINE, label="产物落库与回显", label_dx=58)
    draw_arrow(c, 510, 225, 510, 144, color=LINE)

    c.save()


def fig_sequence() -> None:
    c = new_canvas("fig5-4_analysis_sequence.pdf", 1140, 680)

    participants = [
        ("前端页面", 95),
        ("应用层", 240),
        ("调度代理", 390),
        ("分析代理", 545),
        ("查询代理", 705),
        ("政务业务库", 865),
        ("结果组织代理", 1025),
    ]
    top_y = 625
    bottom_y = 70

    for name, x in participants:
        draw_round_box(c, x - 52, 630, 104, 34, name, [], fill=LIGHT_GRAY, title_size=10, title_height=18)
        draw_dashed_line(c, x, 625, x, bottom_y)

    messages = [
        (95, 240, 590, "提交分析请求"),
        (240, 390, 555, "附带session_summary"),
        (390, 545, 520, "路由至分析代理"),
        (545, 545, 485, "构建AP-Schema"),
        (545, 705, 445, "发送query_projection(Q_A)"),
        (705, 865, 405, "执行最优SQL"),
        (865, 705, 365, "返回result_table + status"),
        (705, 545, 320, "返回D=<X,Γ,σ>"),
        (545, 1025, 275, "生成charts/tables/insights"),
        (1025, 240, 230, "返回ResultPackage"),
        (240, 95, 190, "渲染图表与文字洞察"),
    ]

    for x1, x2, y, label in messages:
        draw_arrow(c, x1, y, x2, y, color=BLUE if x1 != x2 else SKY, label=label, label_dy=8)
        if x1 == x2:
            c.setStrokeColor(SKY)
            c.line(x1, y, x1 + 55, y)
            draw_arrow(c, x1 + 55, y, x1, y - 25, color=SKY)

    draw_text(
        c,
        545,
        135,
        ["分析代理在规划完成后并不直接生成SQL，", "而是通过标准查询接口复用第三章的取数能力。"],
        size=9,
        fill=MUTED,
        align="center",
    )

    c.save()


def fig_metadata_flow() -> None:
    c = new_canvas("fig5-5_metadata_extraction.pdf", 1040, 580)

    draw_round_box(c, 40, 380, 170, 72, "外部政务数据源", ["财政库", "项目库", "公共资源库"], fill=LIGHT_ORANGE, body_size=9)
    draw_round_box(c, 255, 385, 150, 62, "JDBC / ODBC接入", ["连接管理", "库级鉴权"], fill=LIGHT_GRAY, body_size=9)
    draw_round_box(c, 445, 385, 165, 62, "元数据抽取器", ["表结构抓取", "注释与类型解析"], fill=LIGHT_BLUE, body_size=9)
    draw_round_box(c, 650, 415, 150, 54, "关系抽取", ["主外键发现"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 650, 340, 150, 54, "样例值抽取", ["枚举值与样例值"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 840, 415, 150, 54, "PostgreSQL", ["data_source", "schema_*"], fill=LIGHT_GREEN, body_size=8)
    draw_round_box(c, 840, 340, 150, 54, "Milvus", ["值向量索引", "样例检索索引"], fill=LIGHT_GREEN, body_size=8)
    draw_round_box(c, 365, 190, 310, 78, "统一元数据描述", ["表、字段、关系、注释、值域与样例共同构成", "可供LA-Schema与动态样例检索使用的结构化底座"], fill=LIGHT_GRAY, body_size=9)
    draw_round_box(c, 735, 180, 225, 90, "查询服务在线使用", ["模式链接阶段读取schema_table/schema_column/schema_relation", "并结合K={B,L,V}构建LA-Schema"], fill=LIGHT_BLUE, body_size=8)

    draw_arrow(c, 210, 416, 255, 416, color=BLUE)
    draw_arrow(c, 405, 416, 445, 416, color=BLUE)
    draw_arrow(c, 610, 416, 650, 442, color=BLUE)
    draw_arrow(c, 610, 416, 650, 367, color=SKY)
    draw_arrow(c, 800, 442, 840, 442, color=BLUE)
    draw_arrow(c, 800, 367, 840, 367, color=SKY)
    draw_arrow(c, 520, 385, 520, 268, color=LINE)
    draw_arrow(c, 915, 340, 915, 270, color=LINE)
    draw_arrow(c, 675, 230, 735, 225, color=BLUE, label="在线读取", label_dy=10)

    c.save()


def draw_entity(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    title: str,
    fields: list[str],
    *,
    fill: Color = LIGHT_GRAY,
) -> None:
    height = 30 + 18 * len(fields)
    draw_round_box(
        c,
        x,
        y,
        w,
        height,
        title,
        fields,
        fill=fill,
        align="left",
        body_size=8,
        title_size=10,
        title_height=22,
    )


def fig_er() -> None:
    c = new_canvas("fig5-6_metadata_er.pdf", 1180, 680)

    draw_entity(c, 60, 500, 220, "data_source", ["PK source_id", "source_name", "db_type", "conn_config"], fill=LIGHT_ORANGE)
    draw_entity(c, 60, 340, 220, "schema_table", ["PK table_id", "FK source_id", "table_name", "table_comment"], fill=LIGHT_BLUE)
    draw_entity(c, 60, 130, 220, "schema_column", ["PK column_id", "FK table_id", "column_name", "data_type", "column_comment", "sample_values"], fill=LIGHT_CYAN)
    draw_entity(c, 335, 300, 230, "schema_relation", ["PK relation_id", "FK source_table_id", "FK target_table_id", "join_condition"], fill=LIGHT_GREEN)

    draw_entity(c, 630, 520, 230, "session_context", ["PK session_id", "user_id", "history_summary", "last_artifact_id"], fill=LIGHT_ORANGE)
    draw_entity(c, 525, 330, 230, "query_task", ["PK task_id", "FK session_id", "nl_query", "final_sql", "status"], fill=LIGHT_BLUE)
    draw_entity(c, 800, 330, 230, "analysis_task", ["PK task_id", "FK session_id", "nl_query", "ap_schema(JSON)", "status"], fill=LIGHT_CYAN)
    draw_entity(c, 520, 110, 220, "result_artifact", ["PK artifact_id", "task_type", "task_id", "artifact_type", "storage_uri"], fill=LIGHT_GREEN)
    draw_entity(c, 780, 105, 220, "execution_log", ["PK log_id", "task_type", "task_id", "agent_name", "step_name", "status"], fill=LIGHT_GRAY)
    draw_entity(c, 965, 500, 170, "cache_entry", ["PK cache_id", "cache_key", "cache_scope", "expired_at"], fill=LIGHT_GREEN)

    draw_arrow(c, 170, 500, 170, 428, color=BLUE, label="1:N", label_dx=26, label_dy=10)
    draw_arrow(c, 170, 340, 170, 238, color=BLUE, label="1:N", label_dx=26, label_dy=10)
    draw_arrow(c, 280, 395, 335, 395, color=LINE, label="表关系", label_dy=10)

    draw_arrow(c, 745, 520, 640, 425, color=BLUE, label="1:N", label_dx=-20, label_dy=8)
    draw_arrow(c, 745, 520, 915, 425, color=SKY, label="1:N", label_dx=18, label_dy=8)
    draw_arrow(c, 640, 330, 630, 214, color=LINE, label="1:N", label_dx=-20, label_dy=8)
    draw_arrow(c, 915, 330, 890, 214, color=LINE, label="1:N", label_dx=16, label_dy=8)
    draw_arrow(c, 705, 330, 820, 214, color=LINE, dashed=True, label="任务日志", label_dy=8)
    draw_arrow(c, 1030, 500, 1030, 436, color=LINE, dashed=True, label="热点缓存", label_dx=36, label_dy=8)

    draw_text(
        c,
        905,
        42,
        ["result_artifact、execution_log与cache_entry共同支撑", "结果复用、异常追溯和高频请求加速。"],
        size=9,
        fill=MUTED,
        align="center",
    )

    c.save()


def fig_exception_flow() -> None:
    c = new_canvas("fig5-7_exception_trace.pdf", 1040, 560)

    draw_round_box(c, 40, 415, 150, 58, "执行请求", ["查询或分析任务"], fill=LIGHT_ORANGE, body_size=9)
    draw_round_box(c, 230, 415, 170, 58, "执行SQL / 分析脚本", ["调用数据库或算子链"], fill=LIGHT_BLUE, body_size=9)
    draw_round_box(c, 460, 410, 130, 68, "是否成功", ["success ?"], fill=LIGHT_GRAY, body_size=10)
    draw_round_box(c, 640, 415, 170, 58, "产物封装", ["生成结果并更新上下文"], fill=LIGHT_GREEN, body_size=9)
    draw_round_box(c, 860, 415, 140, 58, "返回前端", ["展示结果"], fill=LIGHT_GREEN, body_size=9)

    draw_round_box(c, 230, 245, 170, 58, "异常分类", ["SQL错误 / 空结果 / 脚本异常 / 超时"], fill=LIGHT_ORANGE, body_size=8)
    draw_round_box(c, 455, 245, 140, 58, "是否可恢复", ["recoverable ?"], fill=LIGHT_GRAY, body_size=10)
    draw_round_box(c, 640, 245, 170, 58, "修复与重试", ["查询修复器或参数调整", "retry < β"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 860, 235, 140, 78, "失败终止", ["记录失败状态", "返回解释性错误信息"], fill=LIGHT_RED, body_size=8)

    draw_round_box(c, 130, 55, 780, 110, "结果追溯与留痕", ["每个关键步骤均写入execution_log；成功与失败产物统一登记至result_artifact；", "session_context同步维护最近SQL、结果摘要和失败原因，从而支持问题定位、结果复现与后续追问。"], fill=LIGHT_GRAY, body_size=10)

    draw_arrow(c, 190, 444, 230, 444, color=BLUE)
    draw_arrow(c, 400, 444, 460, 444, color=BLUE)
    draw_arrow(c, 590, 444, 640, 444, color=BLUE, label="是", label_dy=10)
    draw_arrow(c, 810, 444, 860, 444, color=BLUE)

    draw_arrow(c, 525, 410, 525, 303, color=SKY, label="否", label_dx=18)
    draw_arrow(c, 400, 274, 455, 274, color=SKY)
    draw_arrow(c, 595, 274, 640, 274, color=SKY, label="是", label_dy=10)
    draw_arrow(c, 810, 274, 860, 274, color=SKY, label="否", label_dy=10)
    draw_arrow(c, 640, 303, 400, 415, color=SKY, dashed=True, label="重试后回到执行阶段", label_dx=14, label_dy=8)

    for x in (115, 315, 525, 725, 925):
        draw_arrow(c, x, 235, x, 165, color=LINE, dashed=True)

    c.save()


def draw_window(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str) -> None:
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 12, fill=1, stroke=1)
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(x, y + h - 28, w, 28, 12, fill=1, stroke=0)
    c.setFillColor(TEXT)
    c.setFont(CN_FONT, 10)
    c.drawString(x + 14, y + h - 18, title)
    for i in range(3):
        c.setFillColor(HexColor(["#F97066", "#FDB022", "#32D583"][i]))
        c.circle(x + 10 + i * 12, y + h - 14, 3, fill=1, stroke=0)


def fig_wireframe() -> None:
    c = new_canvas("fig5-8_ui_wireframe.pdf", 1160, 700)

    # Panel 1
    draw_window(c, 40, 380, 510, 260, "页面一：自然语言输入与历史会话")
    c.setFillColor(LIGHT_GRAY)
    c.rect(58, 400, 110, 210, fill=1, stroke=0)
    draw_text(c, 72, 588, ["会话A", "会话B", "会话C", "历史记录"], size=9)
    c.setFillColor(LIGHT_BLUE)
    c.roundRect(188, 555, 330, 42, 8, fill=1, stroke=0)
    draw_text(c, 204, 578, ["请输入查询或分析需求……"], size=9, fill=MUTED)
    c.setFillColor(LIGHT_ORANGE)
    c.roundRect(188, 500, 330, 42, 8, fill=1, stroke=0)
    draw_text(c, 204, 523, ["用户：查询2024年各区一般公共预算收入"], size=9)
    c.setFillColor(LIGHT_CYAN)
    c.roundRect(220, 440, 298, 44, 8, fill=1, stroke=0)
    draw_text(c, 236, 464, ["系统：已识别为查询任务，开始调用查询代理"], size=9)

    # Panel 2
    draw_window(c, 610, 380, 510, 260, "页面二：SQL与查询结果展示")
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(628, 510, 474, 90, 8, fill=1, stroke=0)
    draw_text(c, 642, 580, ["SELECT district, SUM(ybsr) AS budget_income", "FROM fiscal_income WHERE year = 2024", "GROUP BY district ORDER BY budget_income DESC;"], font=EN_FONT, size=9)
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.rect(628, 408, 474, 84, fill=1, stroke=1)
    for col_x in (628, 770, 920):
        c.line(col_x, 408, col_x, 492)
    for row_y in (474, 456, 438, 420):
        c.line(628, row_y, 1102, row_y)
    draw_text(c, 646, 480, ["区县", "A区", "B区", "C区"], size=8)
    draw_text(c, 788, 480, ["收入", "18.3亿", "15.7亿", "11.2亿"], size=8)
    draw_text(c, 938, 480, ["趋势分析", "发起分析", "导出结果", "查看日志"], size=8)

    # Panel 3
    draw_window(c, 40, 50, 510, 280, "页面三：分析图表与文字洞察")
    c.setFillColor(LIGHT_ORANGE)
    c.roundRect(58, 230, 474, 80, 8, fill=1, stroke=0)
    draw_text(c, 72, 292, ["洞察1：A区收入规模最高，处于第一梯队。", "洞察2：B区与A区差距收敛，存在追赶趋势。", "洞察3：C区占比不足两成，需结合产业结构进一步分析。"], size=9)
    c.setStrokeColor(BLUE)
    c.rect(58, 100, 220, 110, fill=0, stroke=1)
    c.line(78, 120, 248, 120)
    c.line(78, 120, 120, 170)
    c.line(120, 170, 165, 160)
    c.line(165, 160, 228, 195)
    c.setStrokeColor(SKY)
    c.rect(310, 100, 222, 110, fill=0, stroke=1)
    bar_x = 330
    for height in (40, 70, 52, 85):
        c.setFillColor(LIGHT_CYAN)
        c.rect(bar_x, 110, 26, height, fill=1, stroke=0)
        bar_x += 42
    draw_text(c, 88, 205, ["趋势图"], size=9)
    draw_text(c, 360, 205, ["对比图"], size=9)

    # Panel 4
    draw_window(c, 610, 50, 510, 280, "页面四：任务日志与结果追溯")
    c.setFillColor(LIGHT_GRAY)
    c.rect(628, 80, 140, 220, fill=1, stroke=0)
    draw_text(c, 642, 280, ["任务开始", "LA-Schema构建", "候选生成", "查询修复", "候选判别", "结果封装"], size=9)
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.rect(790, 170, 312, 130, fill=1, stroke=1)
    draw_text(c, 806, 282, ["当前步骤：候选判别", "winner = candidate_7", "execution_status = success", "artifact_uri = /output/..."], size=9)
    c.rect(790, 80, 312, 70, fill=1, stroke=1)
    draw_text(c, 806, 132, ["可追溯产物：final_sql / result_table / logs / charts"], size=9)

    c.save()


def main() -> None:
    fig_architecture()
    fig_dual_flow()
    fig_agents_context()
    fig_sequence()
    fig_metadata_flow()
    fig_er()
    fig_exception_flow()
    fig_wireframe()
    print(f"Generated figures in {OUT_DIR}")


if __name__ == "__main__":
    main()
