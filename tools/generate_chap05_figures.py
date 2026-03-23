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
            (90, 423, 165, 48, "FastAPI Router", ["HTTP接入", "统一路由"], LIGHT_GRAY),
            (285, 423, 165, 48, "Pydantic Models", ["请求校验", "响应序列化"], LIGHT_GRAY),
            (480, 423, 165, 48, "Task Manager", ["task_id创建", "状态维护"], LIGHT_GRAY),
            (675, 423, 165, 48, "SSE Gateway", ["事件推送", "进度回传"], LIGHT_GRAY),
        ],
    )

    draw_layer(
        c,
        40,
        235,
        940,
        140,
        "智能服务层",
        fill=HexColor("#F5F9FF"),
        modules=[
            (65, 270, 150, 72, "Dispatch Node", ["意图识别", "选择Query/Analysis Graph"], LIGHT_ORANGE),
            (250, 258, 210, 96, "Query Graph", ["context/schema/knowledge/example", "logic+cot生成", "repair/select/execute/build"], LIGHT_BLUE),
            (490, 258, 210, 96, "Analysis Graph", ["plan/project/query-call", "pandas算子", "chart/insight/package"], LIGHT_CYAN),
            (730, 270, 130, 72, "Result Builder", ["ResultPackage", "artifact/log"], LIGHT_GREEN),
            (875, 270, 90, 72, "LLM HTTP", ["本地模型", "统一调用"], LIGHT_ORANGE),
        ],
    )
    draw_badge(c, 318, 352, "第三章方法实现", fill=SKY, font_size=8)
    draw_badge(c, 558, 352, "第四章方法实现", fill=SKY, font_size=8)

    draw_layer(
        c,
        40,
        40,
        940,
        185,
        "数据层",
        fill=HexColor("#FCFCFD"),
        modules=[
            (70, 130, 135, 64, "政务业务库", ["财政/项目/公共资源", "原始业务数据"], LIGHT_ORANGE),
            (225, 130, 180, 64, "PostgreSQL + SQLAlchemy", ["session/task/log/artifact", "领域知识与元数据"], LIGHT_GRAY),
            (430, 130, 130, 64, "Milvus", ["值检索", "动态样例库F"], LIGHT_CYAN),
            (585, 130, 130, 64, "Redis", ["热点缓存", "SSE事件通道"], LIGHT_GREEN),
            (740, 130, 140, 64, "文件产物存储", ["图表文件", "导出结果"], LIGHT_GREEN),
            (905, 130, 60, 64, "Trace", ["task_id", "trace_id"], LIGHT_BLUE),
        ],
    )

    for x in (180, 390, 605, 820):
        draw_arrow(c, x, 520, x, 495, label=None, color=LINE, width=1.1)
        draw_arrow(c, x, 400, x, 375, label=None, color=LINE, width=1.1)

    draw_arrow(c, 460, 305, 490, 305, label="query_service_caller复用查询图", label_dy=10, color=BLUE)
    draw_arrow(c, 160, 235, 160, 225, color=LINE, width=1.1)
    draw_arrow(c, 355, 235, 355, 225, color=LINE, width=1.1)
    draw_arrow(c, 595, 235, 595, 225, color=LINE, width=1.1)
    draw_arrow(c, 795, 235, 795, 225, color=LINE, width=1.1)
    draw_arrow(c, 920, 235, 920, 225, color=LINE, width=1.1)

    c.save()


def fig_dual_flow() -> None:
    c = new_canvas("fig5-2_dual_workflow.pdf", 1140, 660)

    draw_round_box(c, 30, 560, 130, 54, "前端页面", ["问数输入", "结果查看"], fill=LIGHT_ORANGE, body_size=8)
    draw_round_box(c, 190, 555, 150, 64, "FastAPI Router", ["HTTP路由", "统一异常处理"], fill=LIGHT_GRAY, body_size=8)
    draw_round_box(c, 375, 555, 145, 64, "Pydantic", ["请求/响应模型", "参数校验"], fill=LIGHT_GRAY, body_size=8)
    draw_round_box(c, 555, 555, 150, 64, "Task Manager", ["task_id创建", "PENDING/RUNNING"], fill=LIGHT_BLUE, body_size=8)
    draw_round_box(c, 740, 555, 150, 64, "SSE Gateway", ["事件编码", "流式回传"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 925, 555, 170, 64, "状态/结果接口", ["GET /tasks/{id}", "result / events"], fill=LIGHT_GREEN, body_size=8)

    draw_arrow(c, 160, 587, 190, 587, color=BLUE)
    draw_arrow(c, 340, 587, 375, 587, color=BLUE)
    draw_arrow(c, 520, 587, 555, 587, color=BLUE)
    draw_arrow(c, 705, 587, 740, 587, color=BLUE)
    draw_arrow(c, 890, 587, 925, 587, color=BLUE)

    draw_text(c, 115, 515, ["应用层接口"], size=12, fill=NAVY, align="center")
    draw_round_box(c, 55, 455, 220, 60, "POST /api/v1/query", ["同步查询；stream=true时返回SSE"], fill=LIGHT_BLUE, body_size=8)
    draw_round_box(c, 305, 455, 250, 60, "POST /api/v1/analysis/tasks", ["创建异步分析任务并返回task_id/event_channel"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 585, 455, 250, 60, "GET /api/v1/tasks/{task_id}", ["查询状态、结果与事件流入口"], fill=LIGHT_GREEN, body_size=8)
    draw_round_box(c, 865, 455, 220, 60, "统一响应对象", ["QueryResponse / AnalysisResultResponse"], fill=LIGHT_GRAY, body_size=8)

    c.setStrokeColor(HexColor("#D0D7E2"))
    c.setLineWidth(1)
    c.line(32, 425, 1105, 425)

    draw_text(c, 125, 392, ["智能服务层实现"], size=12, fill=NAVY, align="center")
    draw_round_box(c, 55, 300, 265, 96, "Query Graph", ["context_loader -> schema_retriever -> knowledge_retriever", "example_retriever -> logic_sql_generator -> cot_sql_generator", "sql_repair -> candidate_selector -> db_executor -> query_result_builder"], fill=LIGHT_BLUE, body_size=8, align="left")
    draw_round_box(c, 360, 300, 300, 96, "Analysis Graph", ["analysis_planner -> qa_projector -> query_service_caller", "operator_executor -> chart_spec_builder -> insight_generator", "result_package_builder"], fill=LIGHT_CYAN, body_size=8, align="left")
    draw_round_box(c, 705, 300, 180, 96, "Support Tools", ["LLM HTTP Client", "Structured Logger", "Artifact Writer"], fill=LIGHT_GRAY, body_size=8)
    draw_round_box(c, 920, 300, 170, 96, "Result Callback", ["写入task/log/artifact", "回传JSON或SSE事件"], fill=LIGHT_GREEN, body_size=8)

    draw_arrow(c, 165, 455, 165, 396, color=BLUE)
    draw_arrow(c, 430, 455, 510, 396, color=SKY, label="analysis task", label_dy=8)
    draw_arrow(c, 710, 455, 1005, 396, color=LINE, label="status/result/events", label_dy=8)
    draw_arrow(c, 320, 348, 360, 348, color=BLUE, label="query_service_caller复用查询服务", label_dy=10)
    draw_arrow(c, 660, 348, 705, 348, color=LINE)
    draw_arrow(c, 885, 348, 920, 348, color=LINE)

    draw_round_box(c, 95, 135, 160, 78, "PostgreSQL", ["元数据、session、task、log", "SQLAlchemy统一读写"], fill=LIGHT_ORANGE, body_size=8)
    draw_round_box(c, 300, 135, 150, 78, "Milvus", ["值检索", "动态样例检索"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 495, 135, 150, 78, "Redis", ["热点缓存", "事件通道"], fill=LIGHT_GREEN, body_size=8)
    draw_round_box(c, 690, 135, 160, 78, "本地大模型HTTP服务", ["Qwen推理接口", "结构化提示调用"], fill=LIGHT_ORANGE, body_size=8)
    draw_round_box(c, 895, 135, 165, 78, "ECharts / 文件产物", ["option生成", "图表与导出落盘"], fill=LIGHT_GRAY, body_size=8)

    draw_arrow(c, 190, 300, 175, 213, color=LINE, dashed=True, label="ORM/元数据", label_dx=-8, label_dy=8)
    draw_arrow(c, 250, 300, 375, 213, color=LINE, dashed=True, label="向量检索", label_dy=8)
    draw_arrow(c, 510, 300, 570, 213, color=LINE, dashed=True, label="任务热状态", label_dy=8)
    draw_arrow(c, 780, 300, 770, 213, color=LINE, dashed=True, label="模型调用", label_dx=28, label_dy=8)
    draw_arrow(c, 1000, 300, 980, 213, color=LINE, dashed=True, label="图表产物", label_dx=26, label_dy=8)

    c.save()


def fig_agents_context() -> None:
    c = new_canvas("fig5-3_agent_context.pdf", 1020, 600)

    draw_round_box(c, 395, 500, 230, 62, "LangGraph Router", ["intent -> Query Graph / Analysis Graph"], fill=LIGHT_ORANGE, body_size=9)

    draw_round_box(
        c,
        70,
        265,
        300,
        160,
        "Query Graph",
        [
            "context_loader",
            "schema_retriever / knowledge_retriever / example_retriever",
            "logic_sql_generator / cot_sql_generator",
            "sql_repair / candidate_selector",
            "db_executor / query_result_builder",
        ],
        fill=LIGHT_BLUE,
        align="left",
        body_size=8,
        title_size=11,
    )

    draw_round_box(
        c,
        650,
        265,
        300,
        160,
        "Analysis Graph",
        [
            "analysis_planner / qa_projector",
            "query_service_caller",
            "operator_executor / chart_spec_builder",
            "insight_generator / result_package_builder",
        ],
        fill=LIGHT_CYAN,
        align="left",
        body_size=8,
        title_size=11,
    )

    draw_round_box(
        c,
        315,
        230,
        390,
        110,
        "共享状态 GraphState",
        [
            "session_id, task_id, trace_id, intent, nl_query, session_summary",
            "la_schema_snapshot, ap_schema, query_result, result_package, status, error",
        ],
        fill=LIGHT_GRAY,
        align="left",
        body_size=9,
        title_size=11,
    )

    draw_round_box(c, 60, 105, 170, 84, "Tool: metadata_reader", ["PostgreSQL / SQLAlchemy", "schema_* / knowledge / session"], fill=LIGHT_ORANGE, body_size=8)
    draw_round_box(c, 255, 105, 160, 84, "Tool: vector_searcher", ["Milvus值检索", "动态样例库F"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 440, 105, 150, 84, "Tool: llm_http_client", ["本地模型HTTP推理", "结构化提示模板"], fill=LIGHT_ORANGE, body_size=8)
    draw_round_box(c, 615, 105, 160, 84, "Tool: db_executor", ["目标政务业务库", "正式SQL执行"], fill=LIGHT_GREEN, body_size=8)
    draw_round_box(c, 800, 105, 160, 84, "Tool: operator/chart/log", ["Pandas / ECharts", "artifact_writer / logger"], fill=LIGHT_GREEN, body_size=8)

    draw_arrow(c, 455, 500, 220, 425, color=BLUE, label="查询任务", label_dx=-16, label_dy=10)
    draw_arrow(c, 565, 500, 800, 425, color=SKY, label="分析任务", label_dx=20, label_dy=10)
    draw_arrow(c, 220, 265, 410, 340, color=LINE, label="写入LA-Schema / QueryResponse", label_dx=20, label_dy=8)
    draw_arrow(c, 800, 265, 610, 340, color=LINE, label="写入AP-Schema / ResultPackage", label_dx=-30, label_dy=8)
    draw_arrow(c, 650, 345, 370, 345, color=BLUE, label="query_service_caller", label_dy=10)

    draw_arrow(c, 145, 189, 145, 265, color=LINE, dashed=True)
    draw_arrow(c, 335, 189, 250, 265, color=LINE, dashed=True)
    draw_arrow(c, 515, 189, 515, 230, color=LINE, dashed=True)
    draw_arrow(c, 695, 189, 695, 265, color=LINE, dashed=True)
    draw_arrow(c, 880, 189, 880, 265, color=LINE, dashed=True)

    draw_text(c, 510, 38, ["系统中的“多智能体”并非自由自治对话，而是基于StateGraph的确定性节点编排与工具绑定调用。"], size=9, fill=MUTED, align="center")

    c.save()


def fig_sequence() -> None:
    c = new_canvas("fig5-4_analysis_sequence.pdf", 1160, 720)

    participants = [
        ("前端页面", 90),
        ("FastAPI", 250),
        ("Task Manager", 415),
        ("Query Graph", 590),
        ("Analysis Graph", 760),
        ("Redis / SSE", 930),
        ("PostgreSQL / Artifact", 1085),
    ]
    bottom_y = 80

    for name, x in participants:
        draw_round_box(c, x - 58, 670, 116, 36, name, [], fill=LIGHT_GRAY, title_size=10, title_height=18)
        draw_dashed_line(c, x, 668, x, bottom_y)

    c.setFont(CN_FONT, 12)
    c.setFillColor(NAVY)
    c.drawString(40, 620, "同步查询")
    c.drawString(40, 345, "异步分析与流式回传")
    c.setStrokeColor(HexColor("#D0D7E2"))
    c.setLineWidth(1)
    c.line(35, 332, 1120, 332)

    top_messages = [
        (90, 250, 580, "POST /api/v1/query"),
        (250, 415, 545, "创建query_task与task_id"),
        (250, 590, 505, "执行Query Graph"),
        (590, 1085, 465, "写入result_artifact / execution_log"),
        (590, 930, 425, "stream=true时写入事件"),
        (590, 250, 385, "返回QueryResponse"),
        (250, 90, 345, "同步返回SQL与结果表"),
    ]
    for x1, x2, y, label in top_messages:
        draw_arrow(c, x1, y, x2, y, color=BLUE, label=label, label_dy=8)

    bottom_messages = [
        (90, 250, 285, "POST /api/v1/analysis/tasks"),
        (250, 415, 250, "创建analysis_task=PENDING"),
        (250, 90, 215, "返回task_id + event_channel"),
        (415, 760, 180, "后台触发Analysis Graph"),
        (760, 930, 145, "写入node_completed / result_ready"),
        (930, 90, 110, "GET /events 持续接收SSE"),
        (760, 1085, 255, "写入ap_schema / ResultPackage"),
        (90, 250, 75 + 35, "GET /tasks/{id}/result"),
        (250, 1085, 75, "读取最终结果与状态"),
    ]
    for x1, x2, y, label in bottom_messages:
        draw_arrow(c, x1, y, x2, y, color=SKY if y < 200 else BLUE, label=label, label_dy=8)

    draw_text(c, 575, 305, ["查询接口同步返回结果，但仍创建task_id以支撑统一追溯；", "分析接口先返回任务标识，再通过状态接口和SSE完成异步回传。"], size=9, fill=MUTED, align="center")

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

    draw_round_box(c, 35, 420, 150, 58, "任务创建", ["状态=PENDING"], fill=LIGHT_ORANGE, body_size=9)
    draw_round_box(c, 230, 420, 170, 58, "子图执行", ["状态=RUNNING", "节点持续写日志"], fill=LIGHT_BLUE, body_size=9)
    draw_round_box(c, 450, 415, 140, 68, "是否成功", ["success ?"], fill=LIGHT_GRAY, body_size=10)
    draw_round_box(c, 640, 420, 170, 58, "结果回传", ["写ResultPackage", "推送result_ready"], fill=LIGHT_GREEN, body_size=9)
    draw_round_box(c, 860, 420, 145, 58, "任务完成", ["状态=SUCCESS"], fill=LIGHT_GREEN, body_size=9)

    draw_round_box(c, 225, 245, 180, 58, "异常拦截", ["FastAPI异常 / 节点异常"], fill=LIGHT_ORANGE, body_size=8)
    draw_round_box(c, 450, 245, 140, 58, "是否可恢复", ["recoverable ?"], fill=LIGHT_GRAY, body_size=10)
    draw_round_box(c, 635, 235, 185, 78, "修复与重试", ["sql_repair / 参数修正", "状态保持RUNNING"], fill=LIGHT_CYAN, body_size=8)
    draw_round_box(c, 860, 235, 145, 78, "失败回传", ["状态=FAILED", "推送task_failed"], fill=LIGHT_RED, body_size=8)

    draw_round_box(c, 120, 60, 800, 110, "日志、产物与可追溯状态", ["execution_log记录trace_id、node_name、status与error；", "result_artifact保存成功产物或失败说明；session_context同步更新最近结果摘要与用户可追问状态。"], fill=LIGHT_GRAY, body_size=10)

    draw_arrow(c, 185, 449, 230, 449, color=BLUE)
    draw_arrow(c, 400, 449, 450, 449, color=BLUE)
    draw_arrow(c, 590, 449, 640, 449, color=BLUE, label="是", label_dy=10)
    draw_arrow(c, 810, 449, 860, 449, color=BLUE)

    draw_arrow(c, 520, 415, 520, 303, color=SKY, label="否", label_dx=18)
    draw_arrow(c, 405, 274, 450, 274, color=SKY)
    draw_arrow(c, 590, 274, 635, 274, color=SKY, label="是", label_dy=10)
    draw_arrow(c, 820, 274, 860, 274, color=SKY, label="否", label_dy=10)
    draw_arrow(c, 635, 303, 400, 420, color=SKY, dashed=True, label="重试后继续执行子图", label_dx=16, label_dy=8)

    for x in (110, 315, 520, 725, 930):
        draw_arrow(c, x, 235, x, 170, color=LINE, dashed=True)

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
