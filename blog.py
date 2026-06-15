import asyncio
import math
import random

import flet as ft

try:
    import flet_video as ftv
except ImportError:
    ftv = None


BG = "#020b06"
PANEL = "#04140c"
PURPLE = "#22c55e"
CYAN = "#7cffb2"
PINK = "#b5ff6d"
MUTED = "#9ab8a6"
WHITE = "#ffffff"
HOME_URL = "HTML-Tests/main-page.html"


BLOG_POSTS = [
    {
        "id": "01",
        "title": "BUILDING NATIVE ASYNCHRONOUS UIs IN PYTHON // AN INTRODUCTION TO FLET",
        "cat": "flet",
        "cat_label": "PYTHON_FLET",
        "pdf": "Blogs/Flet_Reactive_Terminal.pdf",
        "video": "Videos/Flet_Reactive_Terminal.mp4",
        "situation": "Traditional Python GUI frameworks require complex event loops and look completely outdated.",
        "solution": "Leverage Flet's underlying Flutter architecture to build state-driven reactive views using clean pythonic async/await loops.",
        "outcome": "Rendered a high-fidelity system terminal workspace executing UI state switches seamlessly with zero multi-threading boilerplate.",
    },
    {
        "id": "02",
        "title": "DATA DISSECTION WITH VECTORIZED MATRICES // PANDAS CORE MECHANICS",
        "cat": "pandas",
        "cat_label": "PYTHON_PANDAS",
        "pdf": "Blogs/Pandas_Vectorization.pdf",
        "video": "Videos/Pandas_Vectorization.mp4",
        "situation": "Using standard Python for-loops to clean or parse massive arrays tanks runtime execution speeds.",
        "solution": "Utilize Pandas DataFrames to offload element-wise mathematical calculations directly to optimized, vectorized C-arrays under the hood.",
        "outcome": "Processed raw data sweeps instantly, dropping structural data manipulation latency down to millisecond thresholds.",
    },
    {
        "id": "03",
        "title": "MASTERING RESPONSIVE LAYOUT ENGINES // FLET CONTAINMENT STRUCTURES",
        "cat": "flet",
        "cat_label": "PYTHON_FLET",
        "pdf": "Blogs/Flet_Responsiveness.pdf",
        "video": "Videos/Flet_Responsiveness.mp4",
        "situation": "Hardcoded UI canvas positions break application design layouts when scaled across different monitor viewports.",
        "solution": "Implement flexible grid architectures combining 'ft.Row', 'ft.Column', and precise nested container alignment properties.",
        "outcome": "Achieved a clean, fluid interface matrix that dynamically balances space whether running full-screen or as a docked module.",
    },
    {
        "id": "04",
        "title": "LOGICAL MASKING AND DATA FILTERS // PANDAS CONDITIONAL SUBSETS",
        "cat": "pandas",
        "cat_label": "PYTHON_PANDAS",
        "pdf": "Blogs/Pandas_Boolean.pdf",
        "video": "Videos/Pandas_Boolean.mp4",
        "situation": "Sifting through specific multi-variable parameters within dense records via conditional branches creates heavy, unreadable code blocks.",
        "solution": "Apply vectorized boolean indexing masks to slice through multi-dimensional DataFrames in a single declarative line.",
        "outcome": "Assembled clean, high-performance query logic capable of pulling specific target metrics from thousands of records instantly.",
    },
]


def alpha(hex_color, opacity):
    value = hex_color.lstrip("#")
    return f"#{int(opacity * 255):02x}{value}"


def alignment_center():
    return ft.Alignment(0, 0)


def padding(left=0, top=0, right=0, bottom=0):
    return ft.Padding(left=left, top=top, right=right, bottom=bottom)


def border_all(width, color):
    border_type = getattr(ft, "Border", None)
    if border_type and hasattr(border_type, "all"):
        return border_type.all(width, color)
    return ft.border.all(width, color)


def border_only(*, top=None, bottom=None):
    border_type = getattr(ft, "Border", None)
    if border_type and hasattr(border_type, "only"):
        return border_type.only(top=top, bottom=bottom)
    return ft.border.only(top=top, bottom=bottom)


def border_side(width, color):
    return ft.BorderSide(width, color)


def text(value, color=WHITE, size=14, weight=None, **kwargs):
    args = {"value": value, "color": color, "size": size, "font_family": "monospace"}
    if weight is not None:
        args["weight"] = weight
    args.update(kwargs)
    return ft.Text(**args)


def tag(value):
    return text(value.upper(), color=CYAN, size=11, weight=ft.FontWeight.W_700)


def paragraph(value, color=MUTED, size=13):
    return text(value, color=color, size=size)


def enter_container(content=None, **kwargs):
    if content is not None:
        kwargs.setdefault("content", content)
    kwargs.setdefault("opacity", 0)
    kwargs.setdefault("scale", 0.965)
    kwargs.setdefault("animate_opacity", 700)
    kwargs.setdefault("animate_scale", 700)
    return ft.Container(**kwargs)


def starfield(width=1920, height=900, count=90):
    random.seed(108)
    controls = []
    stars = []
    for _ in range(count):
        radius = random.uniform(0.8, 1.8)
        star = ft.Container(
            left=random.randint(0, width),
            top=random.randint(0, height),
            width=radius,
            height=radius,
            bgcolor=alpha(WHITE, random.uniform(0.28, 0.72)),
            border_radius=4,
        )
        stars.append(
            {
                "x": random.randint(0, width),
                "y": random.randint(0, height),
                "speed": random.uniform(0.08, 0.28),
                "control": star,
            }
        )
        controls.append(star)
    return controls, stars


def corner_mark(color=PURPLE, bottom=False, right=False):
    return ft.Container(
        width=24,
        height=24,
        content=ft.Stack(
            [
                ft.Container(
                    right=0 if right else None,
                    left=None if right else 0,
                    top=None if bottom else 0,
                    bottom=0 if bottom else None,
                    width=24,
                    height=2,
                    bgcolor=color,
                ),
                ft.Container(
                    right=0 if right else None,
                    left=None if right else 0,
                    top=None if bottom else 0,
                    bottom=0 if bottom else None,
                    width=2,
                    height=24,
                    bgcolor=color,
                ),
            ]
        ),
    )


def schematic_node(kind, color):
    center = (
        ft.Container(left=40, top=40, width=20, height=20, border=border_all(2, color), border_radius=20)
        if kind == "circle"
        else ft.Container(left=30, top=30, width=40, height=40, border=border_all(2, color))
    )
    controls = [
        ft.Container(left=49, top=0, width=1, height=100, bgcolor=alpha(color, 0.7)),
        ft.Container(left=0, top=49, width=100, height=1, bgcolor=alpha(color, 0.7)),
        center,
    ]
    if kind != "circle":
        controls.append(ft.Container(left=45, top=45, width=10, height=10, bgcolor=color, border_radius=10))
    return ft.Container(width=100, height=100, opacity=0.22, content=ft.Stack(controls))


def title_block(label):
    return ft.Column(
        [
            text(label, color=CYAN, size=14, weight=ft.FontWeight.W_800),
            ft.Container(width=118 if len(label) > 9 else 80, height=2, bgcolor=CYAN),
        ],
        spacing=2,
        tight=True,
    )


def video_embed(src, title, *, height=190):
    if ftv:
        return ft.Container(
            height=height,
            border=border_all(1, alpha(CYAN, 0.55)),
            border_radius=10,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            bgcolor=alpha("#000000", 0.35),
            content=ftv.Video(
                playlist=[ftv.VideoMedia(src)],
                expand=True,
            ),
        )

    return ft.Container(
        height=height,
        padding=16,
        border=border_all(1, alpha(CYAN, 0.55)),
        border_radius=10,
        bgcolor=alpha("#000000", 0.35),
        alignment=alignment_center(),
        content=ft.Column(
            [
                tag("VIDEO MODULE"),
                paragraph(f"{title} preview is available as a local video asset.", size=12),
                ft.OutlinedButton(content=text("[OPEN_VIDEO]", color=CYAN, size=12, weight=ft.FontWeight.BOLD), url=src),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


def build_blog_page(page: ft.Page, home_handler=None, projects_handler=None, qualifications_handler=None):
    page.title = "Journal // Tegameno Iyambo"
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.window_width = 1240
    page.window_height = 820
    page.theme_mode = ft.ThemeMode.DARK

    state = {"filter": "all", "menu": False}
    star_controls, stars = starfield()
    category_buttons = {}
    logs_stream = ft.Column(spacing=20, expand=True, scroll=ft.ScrollMode.AUTO)
    menu_layer = ft.Container(visible=False)

    def home_button(label):
        if home_handler:
            return ft.TextButton(content=text(label, color=PURPLE, size=13), on_click=home_handler)
        return ft.TextButton(content=text(label, color=PURPLE, size=13), url=HOME_URL)

    def projects_button(label):
        if projects_handler:
            return ft.TextButton(content=text(label, color=MUTED, size=13), on_click=projects_handler)
        return ft.TextButton(content=text(label, color=MUTED, size=13), url=HOME_URL)

    def qualifications_button(label):
        if qualifications_handler:
            return ft.TextButton(content=text(label, color=MUTED, size=13), on_click=qualifications_handler)
        return ft.TextButton(content=text(label, color=MUTED, size=13), url=HOME_URL)

    def toggle_menu(_=None):
        state["menu"] = not state["menu"]
        menu_layer.visible = state["menu"]
        hamburger_label.value = "X" if state["menu"] else "MENU"
        page.update()

    def make_category(label, value):
        btn_label = text(label, color=MUTED, size=12, weight=ft.FontWeight.W_700)
        button = ft.TextButton(
            content=ft.Container(
                width=260,
                padding=padding(left=12, top=12, right=12, bottom=12),
                border=border_all(1, alpha(PURPLE, 0.3)),
                border_radius=8,
                bgcolor=alpha("#062015", 0.62),
                content=btn_label,
            ),
            style=ft.ButtonStyle(padding=0),
            on_click=lambda e: set_filter(value),
        )
        category_buttons[value] = (button, btn_label)
        return button

    def line(label, value):
        return ft.Text(
            spans=[
                ft.TextSpan(label, style=ft.TextStyle(color=CYAN, weight=ft.FontWeight.BOLD)),
                ft.TextSpan(f" {value}", style=ft.TextStyle(color=WHITE)),
            ],
            size=13,
            font_family="monospace",
        )

    def log_card(post, delay_index):
        card = enter_container(
            opacity=1,
            scale=1,
            animate_opacity=350,
            animate_scale=350,
            padding=20,
            bgcolor=alpha(PANEL, 0.8),
            border=border_all(1, PURPLE),
            border_radius=12,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            text(f"DECRYPTION_KEY: JOURNAL_REF_#{post['id']}", color=alpha(CYAN, 0.65), size=12),
                            text(f"> Category: {post['cat_label']}", color=PINK, size=12, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    text(post["title"], size=16, weight=ft.FontWeight.W_800),
                    video_embed(post["video"], post["title"]),
                    ft.Column(
                        [
                            line("> Situation:", post["situation"]),
                            line("> Solution:", post["solution"]),
                            line("> Outcome:", post["outcome"]),
                        ],
                        spacing=6,
                    ),
                    ft.Row(
                        [
                            ft.OutlinedButton(content=text("[DECRYPT_ARTICLE]", color=CYAN, size=12, weight=ft.FontWeight.BOLD), url=post["pdf"]),
                            ft.OutlinedButton(content=text("[CODEBASE_REFERENCE]", color=CYAN, size=12, weight=ft.FontWeight.BOLD)),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=14,
            ),
        )
        card.data = delay_index
        return card

    def refresh_logs():
        active = state["filter"]
        shown = [post for post in BLOG_POSTS if active == "all" or post["cat"] == active]
        logs_stream.controls = [log_card(post, index) for index, post in enumerate(shown, start=1)]

        for value, (button, label_control) in category_buttons.items():
            selected = value == active
            surface = button.content
            surface.border = border_all(1, CYAN if selected else alpha(PURPLE, 0.3))
            surface.bgcolor = alpha(CYAN, 0.1) if selected else alpha("#062015", 0.62)
            label_control.color = CYAN if selected else MUTED
            label_control.weight = ft.FontWeight.BOLD if selected else ft.FontWeight.W_700

    def set_filter(value):
        state["filter"] = value
        refresh_logs()
        page.update()

    index_panel = ft.Column(
        [
            ft.Column(
                [
                    title_block("JOURNAL_INDEX"),
                    paragraph("> ROOT // TECHNICAL_LOGS /", size=12),
                ],
                spacing=12,
            ),
            ft.Column(
                [
                    make_category("> ALL CATEGORIES", "all"),
                    make_category("  PYTHON_FLET (2)", "flet"),
                    make_category("  PYTHON_PANDAS (2)", "pandas"),
                ],
                spacing=10,
            ),
            ft.Container(expand=True),
            home_button("[RETURN TO MATRIX]"),
        ],
        spacing=18,
        width=300,
    )

    feed_panel = ft.Column(
        [
            ft.Column(
                [
                    title_block("LOGS_FEED"),
                    paragraph("DISPLAYING_MOST_RECENT_LOGS...", size=12),
                ],
                spacing=12,
            ),
            ft.Container(content=logs_stream, expand=True, clip_behavior=ft.ClipBehavior.HARD_EDGE),
        ],
        spacing=15,
        expand=True,
    )

    refresh_logs()

    scanner = ft.Container(left=0, right=0, top=0, height=2, bgcolor=alpha(PURPLE, 0.25))

    console = enter_container(
        width=1200,
        height=720,
        padding=25,
        bgcolor=alpha(PANEL, 0.9),
        border=border_all(1, PURPLE),
        content=ft.Stack(
            [
                scanner,
                ft.Container(left=-5, top=-5, content=corner_mark(PURPLE)),
                ft.Container(right=-5, bottom=-5, content=corner_mark(PURPLE, bottom=True, right=True)),
                ft.Column(
                    [
                        ft.Container(
                            padding=padding(bottom=20),
                            border=border_only(bottom=border_side(1, alpha(PURPLE, 0.2))),
                            content=tag("SYSTEM_STATUS: ONLINE // SUB_SECTOR: /JOURNAL_ARCHIVE"),
                        ),
                        ft.Row(
                            [index_panel, feed_panel],
                            spacing=25,
                            expand=True,
                            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                        ),
                    ],
                    spacing=20,
                    expand=True,
                ),
            ]
        ),
    )

    node_left = enter_container(content=schematic_node("circle", PURPLE), left=55, top=120)
    node_right = enter_container(content=schematic_node("square", CYAN), right=55, bottom=120)

    hamburger_label = text("MENU", color=CYAN, size=12, weight=ft.FontWeight.W_800)
    hamburger_button = enter_container(
        right=58,
        top=30,
        width=64,
        height=34,
        alignment=alignment_center(),
        border=border_all(1, alpha(CYAN, 0.7)),
        border_radius=6,
        bgcolor=alpha("#062015", 0.78),
        content=ft.TextButton(
            content=hamburger_label,
            on_click=toggle_menu,
            style=ft.ButtonStyle(padding=0),
        ),
    )

    menu_layer.content = ft.Container(
        width=230,
        padding=12,
        bgcolor=alpha("#062015", 0.95),
        border=border_all(1, alpha(PURPLE, 0.6)),
        border_radius=10,
        content=ft.Column(
            [
                home_button("Home Page"),
                projects_button("Projects Map"),
                qualifications_button("Qualifications"),
                home_button("Distinctions"),
                home_button("Evaluations"),
            ],
            spacing=4,
        ),
    )

    root = ft.Container(
        expand=True,
        bgcolor=BG,
        animate_opacity=260,
        animate_scale=260,
        content=ft.Stack(
            [
                *star_controls,
                node_left,
                node_right,
                ft.Container(expand=True, alignment=alignment_center(), content=console),
                hamburger_button,
                ft.Container(content=menu_layer, right=58, top=76),
            ],
            expand=True,
        ),
    )

    async def reveal():
        await asyncio.sleep(0.08)
        console.opacity = 1
        console.scale = 1
        node_left.opacity = 0.22
        node_left.scale = 1
        node_right.opacity = 0.22
        node_right.scale = 1
        hamburger_button.opacity = 1
        hamburger_button.scale = 1
        page.update()

    def animate(tick):
        viewport_w = page.width or 1200
        viewport_h = page.height or 800

        for star in stars:
            star["x"] -= star["speed"]
            if star["x"] < -4:
                star["x"] = viewport_w + random.randint(0, 80)
                star["y"] = random.randint(0, int(viewport_h))
            star["control"].left = star["x"]
            star["control"].top = star["y"]

        scanner.top = (math.sin(tick * 0.9) + 1) / 2 * 680
        node_left.left = 55 + math.sin(tick * 0.55) * 8
        node_left.top = 120 + math.cos(tick * 0.48) * 10
        node_right.right = 55 + math.cos(tick * 0.5) * 8
        node_right.bottom = 120 + math.sin(tick * 0.44) * 10

    return root, reveal, animate


async def main(page: ft.Page):
    root, reveal, animate = build_blog_page(page)
    page.add(root)
    await reveal()

    tick = 0.0
    while True:
        tick += 0.06
        animate(tick)
        page.update()
        await asyncio.sleep(0.06)


if __name__ == "__main__":
    ft.app(target=main, assets_dir=".", view=ft.AppView.WEB_BROWSER)
