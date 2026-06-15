import asyncio
import math
import random

import flet as ft


BG = "#130309"
PANEL = "#160711"
PURPLE = "#d5336f"
CYAN = "#ff8a4c"
PINK = "#ff5c8a"
MUTED = "#c6a9b7"
NEBULA_CORE = "#4a1020"
NEBULA_MID = "#260711"
WHITE = "#ffffff"
HOME_URL = "HTML-Tests/main-page.html"


CERTIFICATES = [
    {
        "name": "Calculations w/ Vectors & Matrices",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Calculations with Vectors and Matrices.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "Circuit Simulation Onramp",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Circuit Simulation Onramp.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "Core Matlab Skills",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Core Matlab Skills.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "Matlab Onramp",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Matlab Onramp.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "Signal Processing Onramp",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Signal Processing Onramp.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "Simulink Fundamentals",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Simulink Fundamentals.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "Simulink Onramp",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Simulink Onramp.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "Visualization in Matlab",
        "cat": "matlab",
        "url": "Certificates/Math Works/MathWorks Visualization in Matlab.pdf",
        "icon": "Image-Assets/mathworksicon.png",
    },
    {
        "name": "AutoCAD Essentials",
        "cat": "cad",
        "url": "Certificates/SourceCAD/SourceCAD AutoCAD Essentials.pdf",
        "icon": "Image-Assets/sourcecadicon.png",
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


def border_only(*, left=None, top=None, right=None, bottom=None):
    border_type = getattr(ft, "Border", None)
    if border_type and hasattr(border_type, "only"):
        return border_type.only(left=left, top=top, right=right, bottom=bottom)
    return ft.border.only(left=left, top=top, right=right, bottom=bottom)


def border_side(width, color):
    return ft.BorderSide(width, color)


def text(value, color=WHITE, size=14, weight=None, **kwargs):
    args = {"value": value, "color": color, "size": size}
    if weight is not None:
        args["weight"] = weight
    args.update(kwargs)
    return ft.Text(**args)


def tag(value):
    return text(value.upper(), color=CYAN, size=11, weight=ft.FontWeight.W_700)


def paragraph(value, color=MUTED):
    return text(value, color=color, size=13)


def nav_label(value):
    return text(value.upper(), color=WHITE, size=24, weight=ft.FontWeight.W_900)


def enter_container(content=None, **kwargs):
    if content is not None:
        kwargs.setdefault("content", content)
    kwargs.setdefault("opacity", 0)
    kwargs.setdefault("scale", 0.96)
    kwargs.setdefault("animate_opacity", 700)
    kwargs.setdefault("animate_scale", 700)
    return ft.Container(**kwargs)


def starfield(width=1920, height=900, count=150):
    random.seed(84)
    controls = []
    stars = []
    for _ in range(count):
        size = random.choice([1, 1, 1, 2])
        star = ft.Container(
            left=random.randint(0, width),
            top=random.randint(0, height),
            width=size,
            height=size,
            bgcolor=alpha(random.choice([WHITE, PINK, CYAN]), random.uniform(0.28, 0.78)),
            border_radius=3,
        )
        stars.append(
            {
                "x": random.randint(0, width),
                "y": random.randint(0, height),
                "size": size,
                "speed": random.uniform(0.15, 0.65),
                "control": star,
            }
        )
        controls.append(star)
    return controls, stars


def corner_mark(color=PURPLE, bottom=False, right=False):
    return ft.Container(
        width=22,
        height=22,
        content=ft.Stack(
            [
                ft.Container(
                    right=0 if right else None,
                    left=None if right else 0,
                    top=None if bottom else 0,
                    bottom=0 if bottom else None,
                    width=22,
                    height=2,
                    bgcolor=color,
                ),
                ft.Container(
                    right=0 if right else None,
                    left=None if right else 0,
                    top=None if bottom else 0,
                    bottom=0 if bottom else None,
                    width=2,
                    height=22,
                    bgcolor=color,
                ),
            ]
        ),
    )


def schematic_node(kind, color):
    if kind == "circle":
        center = ft.Container(
            left=40,
            top=40,
            width=20,
            height=20,
            border=border_all(2, color),
            border_radius=20,
        )
    else:
        center = ft.Container(
            left=30,
            top=30,
            width=40,
            height=40,
            border=border_all(2, color),
        )

    controls = [
        ft.Container(left=49, top=0, width=1, height=100, bgcolor=alpha(color, 0.7)),
        ft.Container(left=0, top=49, width=100, height=1, bgcolor=alpha(color, 0.7)),
        center,
    ]
    if kind != "circle":
        controls.append(ft.Container(left=45, top=45, width=10, height=10, bgcolor=color, border_radius=10))

    return ft.Container(width=100, height=100, opacity=0.3, content=ft.Stack(controls))


def build_qualifications_page(page: ft.Page, home_handler=None, projects_handler=None, blog_handler=None):
    page.title = "Qualifications // Tegameno Iyambo"
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.window_width = 1100
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK

    state = {"filter": "all", "selected": None, "menu": False}
    star_controls, stars = starfield()

    cert_grid = ft.Column(spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)
    filter_buttons = {}
    modal = ft.Container(visible=False)
    menu_layer = ft.Container(visible=False)

    def select_cert(cert):
        state["selected"] = cert
        modal.content = make_modal(cert)
        modal.visible = True
        page.update()

    def make_filter_button(label, value):
        button = ft.Container(
            height=32,
            padding=padding(left=14, right=14),
            alignment=alignment_center(),
            border=border_all(1, PURPLE),
            bgcolor=alpha("#1a1a2e", 0.85),
            content=text(label, size=11, weight=ft.FontWeight.W_800),
            on_click=lambda e: set_filter(value),
        )
        filter_buttons[value] = button
        return button

    def cert_row(cert, index):
        return ft.Container(
            height=58,
            padding=padding(left=12, top=10, right=12, bottom=10),
            border=border_only(bottom=border_side(1, alpha(WHITE, 0.07))),
            bgcolor=alpha(PURPLE, 0.04) if index % 2 else alpha(PANEL, 0.12),
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Image(src=cert["icon"], width=20, height=20, fit="contain"),
                            text(cert["name"], size=13, weight=ft.FontWeight.W_600),
                        ],
                        spacing=14,
                        expand=True,
                    ),
                    text("[ACCESS]", color=CYAN, size=11, weight=ft.FontWeight.W_800),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=lambda e: select_cert(cert),
        )

    def refresh_grid():
        active = state["filter"]
        shown = [cert for cert in CERTIFICATES if active == "all" or cert["cat"] == active]
        cert_grid.controls = [cert_row(cert, index) for index, cert in enumerate(shown)]
        for value, button in filter_buttons.items():
            selected = value == active
            button.bgcolor = PURPLE if selected else alpha("#1a1a2e", 0.85)
            button.border = border_all(1, CYAN if selected else PURPLE)
            button.content.color = WHITE if selected else MUTED

    def set_filter(value):
        state["filter"] = value
        refresh_grid()
        page.update()

    def close_modal(_=None):
        modal.visible = False
        page.update()

    def toggle_menu(_=None):
        state["menu"] = not state["menu"]
        menu_layer.visible = state["menu"]
        hamburger_button.content.value = "X" if state["menu"] else "MENU"
        page.update()

    def home_button(label):
        if home_handler:
            return ft.TextButton(content=label, on_click=home_handler)
        return ft.TextButton(content=label, url=HOME_URL)

    def projects_button(label):
        if projects_handler:
            return ft.TextButton(content=label, on_click=projects_handler)
        return ft.TextButton(content=label, url=HOME_URL)

    def blog_button(label):
        if blog_handler:
            return ft.TextButton(content=label, on_click=blog_handler)
        return ft.TextButton(content=label, url=HOME_URL)

    def make_modal(cert):
        return ft.Container(
            expand=True,
            bgcolor=alpha("#000000", 0.9),
            alignment=alignment_center(),
            content=ft.Container(
                width=620,
                padding=30,
                bgcolor=alpha(PANEL, 0.96),
                border=border_all(1, PURPLE),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                tag("CERTIFICATE ACCESS"),
                                ft.TextButton(content="[CLOSE]", on_click=close_modal, style=ft.ButtonStyle(color=PURPLE)),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        nav_label(cert["name"]),
                        paragraph("The selected certificate is available as a local PDF asset in the portfolio directory."),
                        ft.Row(
                            [
                                ft.ElevatedButton(content="OPEN PDF", url=cert["url"]),
                                ft.OutlinedButton(content="RETURN", on_click=close_modal),
                            ],
                            spacing=12,
                        ),
                    ],
                    spacing=18,
                ),
            ),
        )

    refresh_grid()

    console = enter_container(
        width=650,
        height=640,
        padding=30,
        bgcolor=alpha(PANEL, 0.92),
        border=border_all(1, PURPLE),
        content=ft.Stack(
            [
                ft.Container(left=-5, top=-5, content=corner_mark(PURPLE)),
                ft.Container(right=-5, bottom=-5, content=corner_mark(PURPLE, bottom=True, right=True)),
                ft.Container(
                    left=0,
                    right=0,
                    top=0,
                    height=2,
                    bgcolor=alpha(PURPLE, 0.35),
                    opacity=0.75,
                ),
                ft.Column(
                    [
                        ft.Container(
                            padding=padding(bottom=20),
                            bgcolor=alpha(PANEL, 0.75),
                            content=ft.Column(
                                [
                                    tag("STATUS: ONLINE // SYSTEM: V.2.0"),
                                    nav_label("Certifications"),
                                    ft.Row(
                                        [
                                            make_filter_button("ALL", "all"),
                                            make_filter_button("MATLAB", "matlab"),
                                            make_filter_button("CAD", "cad"),
                                        ],
                                        spacing=10,
                                    ),
                                ],
                                spacing=12,
                            ),
                        ),
                        ft.Container(content=cert_grid, expand=True, clip_behavior=ft.ClipBehavior.HARD_EDGE),
                        ft.TextButton(
                            content="[RETURN TO MATRIX]",
                            on_click=home_handler if home_handler else None,
                            url=None if home_handler else HOME_URL,
                            style=ft.ButtonStyle(color=PURPLE, padding=0),
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),
            ]
        ),
    )
    refresh_grid()

    node_left = enter_container(content=schematic_node("circle", PURPLE), left=70, top=150)
    node_right = enter_container(content=schematic_node("square", CYAN), right=70, bottom=150)

    hamburger_button = enter_container(
        right=58,
        top=30,
        visible=True,
        width=64,
        height=34,
        alignment=alignment_center(),
        border=border_all(1, alpha(CYAN, 0.7)),
        border_radius=6,
        bgcolor=alpha("#0c081c", 0.72),
        content=text("MENU", color=CYAN, size=12, weight=ft.FontWeight.W_800),
        on_click=toggle_menu,
    )

    menu_layer.content = ft.Container(
        width=230,
        padding=12,
        bgcolor=alpha("#0c081c", 0.95),
        border=border_all(1, alpha(PURPLE, 0.6)),
        border_radius=10,
        content=ft.Column(
            [
                home_button("Home Page"),
                projects_button("Projects Map"),
                blog_button("Technical Blogs"),
                home_button("Distinctions"),
                home_button("Evaluations"),
            ],
            spacing=4,
        ),
    )

    root = ft.Container(
        expand=True,
        bgcolor=BG,
        gradient=ft.RadialGradient(
            center=ft.Alignment(-0.25, -0.15),
            radius=1.25,
            colors=[NEBULA_CORE, NEBULA_MID, BG],
        ),
        animate_opacity=260,
        animate_scale=260,
        content=ft.Stack(
            [
                *star_controls,
                ft.Container(
                    left=-120,
                    top=80,
                    width=620,
                    height=620,
                    opacity=0.16,
                    gradient=ft.RadialGradient(
                        center=ft.Alignment(0, 0),
                        radius=0.75,
                        colors=[PINK, alpha(PINK, 0.14), alpha(BG, 0)],
                    ),
                ),
                ft.Container(
                    right=-180,
                    bottom=-80,
                    width=760,
                    height=760,
                    opacity=0.18,
                    gradient=ft.RadialGradient(
                        center=ft.Alignment(0, 0),
                        radius=0.82,
                        colors=[CYAN, alpha(PURPLE, 0.16), alpha(BG, 0)],
                    ),
                ),
                node_left,
                node_right,
                ft.Container(expand=True, alignment=alignment_center(), content=console),
                hamburger_button,
                ft.Container(content=menu_layer, right=58, top=76),
                modal,
            ],
            expand=True,
        ),
    )

    async def reveal():
        await asyncio.sleep(0.08)
        console.opacity = 1
        console.scale = 1
        hamburger_button.opacity = 1
        hamburger_button.scale = 1
        node_left.opacity = 0.3
        node_left.scale = 1
        node_right.opacity = 0.3
        node_right.scale = 1
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

        scan_y = (math.sin(tick * 0.9) + 1) / 2
        console.content.controls[2].top = 12 + scan_y * 560

        node_left.left = 70 + math.sin(tick * 0.55) * 8
        node_left.top = 150 + math.cos(tick * 0.48) * 10
        node_right.right = 70 + math.cos(tick * 0.5) * 8
        node_right.bottom = 150 + math.sin(tick * 0.44) * 10

    return root, reveal, animate


async def main(page: ft.Page):
    root, reveal, animate = build_qualifications_page(page)
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
