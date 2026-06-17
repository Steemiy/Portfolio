import asyncio
import math
import random


import flet as ft

try:
    import flet_video as ftv
except ImportError:
    ftv = None


# Projects uses a soft yellow background to visually differentiate from other pages
BG = "#2c2d0e"        # deep warm yellow/brown
PANEL = "#261b0a"    # slightly lighter panel surface
HEADER = "#1a1506"

# Yellow-first palette to make Projects page stand out from other pages
YELLOW = "#fbbf24"          # bright amber
GOLD = "#f59e0b"            # deeper amber
SUNSET = "#f97316"          # warm orange accent
LIME = "#eab308"            # extra punch

PURPLE = "#d946ef"          # retained for subtle contrast (menu accents)
LAVENDER = "#facc15"        # used as the main highlight color
BLUE = "#7dd3fc"            # for secondary borders
PINK = "#fb7185"            # for code snippets/buttons
WHITE = "#ffffff"
TEXT = "#fef3c7"            # slightly warm white
MUTED = "#fde68a"           # warm muted text

HOME_URL = "HTML-Tests/main-page.html"
QUALIFICATIONS_URL = "HTML-Tests/qualifications.html"


THEME_ROWS = [
    ("Light", "#F3F6FC", "#FFFFFF", "#D4833D", "#212B36"),
    ("Dark", "#101926", "#182536", "#EBA350", "#DCE2EB"),
    ("Warm", "#F4EEE6", "#FFFFFF", "#8D5B38", "#2E2621"),
    ("Night", "#0D1B26", "#152736", "#DEA14E", "#D2DCE6"),
]


TRACE_ROWS = [
    ("FR-001 / 002", "Auth Pipelines", "Designed targeted role-based login interfaces feeding into adaptive application structures."),
    ("FR-003 / 015", "Hazard Ingestion", "Created the native form workflow, media picker, and quick-select severity tokens."),
    ("FR-005 / 006", "Live Map Engine", "Established green/yellow/red overlay matrices for active geospatial hazard fields."),
    ("FR-007", "Fall Detection", "Built the automated intercept countdown modal with global override triggers."),
    ("FR-008", "Noise Telemetry", "Implemented the real-time sensor dashboard with contextual alert color bars."),
    ("FR-009 / 010", "SOS Broadcasts", "Engineered the isolated emergency layout layer and global push banners."),
    ("FR-011 / 013", "Supervisor Suite", "Formatted data visualizations matching brand accents."),
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


def border_only(*, top=None, bottom=None, left=None):
    border_type = getattr(ft, "Border", None)
    if border_type and hasattr(border_type, "only"):
        return border_type.only(top=top, bottom=bottom, left=left)
    return ft.border.only(top=top, bottom=bottom, left=left)


def border_side(width, color):
    return ft.BorderSide(width, color)


def text(value, color=TEXT, size=14, weight=None, **kwargs):
    args = {"value": value, "color": color, "size": size}
    if weight is not None:
        args["weight"] = weight
    args.update(kwargs)
    return ft.Text(**args)


def paragraph(value, color=MUTED, size=13):
    return text(value, color=color, size=size)



def code(value):
    return ft.Container(
        padding=padding(left=6, top=2, right=6, bottom=2),
        bgcolor=alpha(WHITE, 0.06),
        border_radius=4,
        content=text(value, color=PINK, size=12, weight=ft.FontWeight.W_600),
    )


def bullet(value):
    return ft.Row(
        [
            text("•", color=LAVENDER, size=18, weight=ft.FontWeight.W_700),
            paragraph(value),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def section_heading(value):
    return ft.Container(
        padding=padding(left=12),
        border=border_only(left=border_side(3, LIME)),
        content=text(value, color=WHITE, size=18, weight=ft.FontWeight.W_600),
    )



def subheading(value):
    return text(value, color=WHITE, size=15, weight=ft.FontWeight.W_600)


def table(headers, rows):
    header = ft.Row(
        [
            ft.Container(
                content=text(item, color=WHITE, size=12, weight=ft.FontWeight.W_700),
                padding=padding(left=10, top=9, right=10, bottom=9),
                expand=True,
            )
            for item in headers
        ],
        spacing=0,
    )
    body = []
    for row in rows:
        body.append(
            ft.Row(
                [
                    ft.Container(
                        content=text(str(item), color=MUTED if index else WHITE, size=12, weight=ft.FontWeight.W_600 if index == 0 else None),
                        padding=padding(left=10, top=9, right=10, bottom=9),
                        expand=True,
                    )
                    for index, item in enumerate(row)
                ],
                spacing=0,
            )
        )

    return ft.Container(
        border=border_all(1, alpha(WHITE, 0.08)),
        border_radius=8,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column(
            [
                ft.Container(bgcolor="#1a2201", content=header),
                *[
                    ft.Container(
                        bgcolor=alpha("#312700", 0.42),
                        border=border_only(top=border_side(1, alpha(WHITE, 0.05))),
                        content=row_control,
                    )
                    for row_control in body
                ],
            ],
            spacing=0,
        ),
    )


def starfield(width=1920, height=1200, count=120):
    random.seed(128)
    controls = []
    stars = []
    for _ in range(count):
        radius = random.uniform(0.6, 1.8)
        star = ft.Container(
            left=random.randint(0, width),
            top=random.randint(0, height),
            width=radius,
            height=radius,
            bgcolor=alpha(WHITE, random.uniform(0.35, 0.85)),
            border_radius=3,
        )
        stars.append(
            {
                "x": random.randint(0, width),
                "y": random.randint(0, height),
                "speed_x": random.uniform(-0.18, 0.18),
                "speed_y": random.uniform(0.08, 0.32),
                "control": star,
            }
        )
        controls.append(star)
    return controls, stars


def video_embed(src, title, *, height=280):
    if ftv:
        return ft.Container(
            height=height + 80,
            padding=padding(left=16, top=16, right=16, bottom=16),
            border=border_all(1, alpha(LAVENDER, 0.55)),
            border_radius=12,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            bgcolor=alpha("#000000", 0.35),
            content=ft.Column(
                [
                    text(title, color=WHITE, size=14, weight=ft.FontWeight.W_700),
                    paragraph(f"Source: {src}", color=MUTED, size=12),
                    ft.Container(
                        height=height,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ftv.Video(
                            playlist=[ftv.VideoMedia(src)],
                            expand=True,
                        ),
                    ),
                ],
                spacing=10,
            ),
        )

    return ft.Container(
        height=height,
        padding=20,
        border=border_all(1, alpha(LAVENDER, 0.55)),
        border_radius=12,
        bgcolor=alpha("#000000", 0.35),
        alignment=alignment_center(),
        content=ft.Column(
            [
                section_heading("Video Module"),
                paragraph(f"{title} is available as a local video asset."),
                ft.OutlinedButton(content="OPEN VIDEO", url=src),
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


def build_mineshield_content():
    return ft.Column(
        [
            section_heading("1. Executive Summary"),
            paragraph(
                "As the UI/UX Lead for MineShield, I was responsible for the end-to-end visual and interactive architecture of the application, translating complex safety requirements into production-ready React Native components."
            ),
            bullet("Key deliverables: Figma Design System, Cross-Platform Component Library, Global Theme Engine, and Technical System Documentation."),
            video_embed("Videos/MineShield_Contributions.mp4", "MineShield Contributions"),
            section_heading("2. Figma Design System & Iteration"),
            subheading("2.1 Environmental Design Factors"),
            bullet("Expanded critical touch targets to a minimum of 64 x 64 dp for workers wearing protective gear."),
            bullet("Refactored the base canvas to a high-visibility light theme (#F3F6FC) after glare testing."),
            bullet("Redesigned the SOS trigger with a 3-second press-and-hold gesture and a visible countdown progress bar."),
            subheading("2.2 Interactive High-Fidelity Prototypes"),
            paragraph("I engineered interconnected clickable user journeys across 20+ unique screen states, mapping cross-role safety pipelines."),
            ft.Container(
                bgcolor=alpha(PURPLE, 0.08),
                border=border_only(left=border_side(3, BLUE)),
                border_radius=8,
                padding=padding(left=16, top=12, right=16, bottom=12),
                content=paragraph(
                    "Core workflow: Worker logs a hazard via ReportHazardScreen -> Live Firestore sync -> Active marker appears on the Supervisor LiveMapScreen."
                ),
            ),
            section_heading("3. Core Architecture & Code Implementation"),
            paragraph(
                "All production components are written in React Native (Expo) and hook directly into a central context engine. Safety colors remain fixed across visual overrides."
            ),
            subheading("3.1 The Dynamic Theme Engine"),
            paragraph("src/contexts/ThemeContext.js manages global spacing tokens, border radii, and a four-tier theme system saved via AsyncStorage."),
            table(["Theme Mode", "Canvas Base", "Card Surface", "Active Accent", "Primary Text"], THEME_ROWS),
            subheading("3.2 Key Reusable UI Components"),
            bullet("Button.js: strict WCAG-compliant touch layouts, async loading layout, and adaptive state variants."),
            bullet("Card.js: semantic layout container with absolute safety alert fills for danger states."),
            bullet("Header.js: structured navigation with contextual back-navigation, view slots, and action indicators."),
            section_heading("4. Functional Traceability Matrix"),
            table(["Requirement ID", "System Target", "Design & UI/UX Execution"], TRACE_ROWS),
            section_heading("5. Engineering Leadership & Technical Challenges"),
            subheading("Overcoming Fragmented Styling Styles"),
            paragraph("The problem: developers initially bypassed UI layouts by hardcoding styling rules directly into functional loops."),
            paragraph(
                "The solution: I established a project gatekeeping workflow where no component pull requests were merged without an approved mapped Figma design token."
            ),
            ft.Row(
                [
                    ft.ElevatedButton(content="VIEW FULL TECHNICAL DOCUMENTATION", url="DOCS/MineShield_Doc.pdf"),
                    ft.OutlinedButton(
                        content="EXPLORE FIGMA PROTOTYPES",
                        url="https://www.figma.com/design/grItLPUGBHKbbvTEcvasPH/Mine-Shield?node-id=0-1&t=SvsNRWHne8udo77r-1",
                    ),
                    ft.OutlinedButton(
                        content="EXPLORE GITHUB REPOSITORY",
                        url="https://github.com/raunanehale06-png/UNAM-I3691CP-Group-16-Mineshield",
                    ),
                ],
                spacing=16,
                wrap=True,
            ),
        ],
        spacing=14,
    )


def build_bitlink_content():
    return ft.Column(
        [
            section_heading("Documentation coming soon."),
            paragraph("Bitlink is a scheduling webapp designed for the academic scene. It is currently under development and will be released in the near future."),
        ],
        spacing=14,
    )


def build_projects_page(page: ft.Page, home_handler=None, qualifications_handler=None, blog_handler=None):
    page.title = "Projects // Tegameno Iyambo"
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.window_width = 1100
    page.window_height = 850
    page.theme_mode = ft.ThemeMode.DARK

    state = {"expanded": None, "menu": False}
    star_controls, stars = starfield()
    menu_layer = ft.Container(visible=False)

    def navigate_home(_=None):
        if home_handler:
            home_handler()

    def navigate_qualifications(_=None):
        if qualifications_handler:
            qualifications_handler()

    def navigate_blog(_=None):
        if blog_handler:
            blog_handler()

    def toggle_menu(_=None):
        state["menu"] = not state["menu"]
        menu_layer.visible = state["menu"]
        hamburger_button.content.value = "X" if state["menu"] else "MENU"
        page.update()

    def menu_button(label, handler=None, url=None):
        return ft.TextButton(content=label, on_click=handler, url=url)

    def set_expanded(section_id):
        state["expanded"] = None if state["expanded"] == section_id else section_id
        refresh_sections()
        page.update()

    sections_column = ft.Column(spacing=30, expand=True, scroll=ft.ScrollMode.AUTO)

    def project_section(section_id, title, subtitle, body):
        expanded = state["expanded"] == section_id
        icon = "+" if not expanded else "×"
        return ft.Container(
            bgcolor=alpha(PANEL, 0.75),
            border=border_all(1, alpha(LIME if expanded else WHITE, 0.32 if expanded else 0.08)),

            border_radius=16,

            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(blur_radius=35, color=alpha("#000000", 0.55), offset=ft.Offset(0, 16)),
            content=ft.Column(
                [
                    ft.Container(
                        bgcolor=alpha(HEADER, 0.55),
                        padding=padding(left=32, top=24, right=32, bottom=24),
                        on_click=lambda e: set_expanded(section_id),
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        text(title, color=WHITE, size=22, weight=ft.FontWeight.W_700),
                                        text(subtitle.upper(), color=LAVENDER, size=12, weight=ft.FontWeight.W_600),
                                    ],
                                    spacing=4,
                                    expand=True,
                                ),
                                ft.Container(
                                    width=32,
                                    height=32,
                                    border_radius=32,
                                    bgcolor=alpha(PURPLE, 0.18 if expanded else 0.05),
                                    alignment=alignment_center(),
                                    content=text(icon, color=LAVENDER if expanded else MUTED, size=20, weight=ft.FontWeight.W_700),
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                    ft.Container(
                        visible=expanded,
                        padding=padding(left=32, top=32, right=32, bottom=32),
                        border=border_only(top=border_side(1, alpha(WHITE, 0.06))),
                        content=body,
                    ),
                ],
                spacing=0,
            ),
        )

    def refresh_sections():
        sections_column.controls = [
            project_section(
                "section-mineshield",
                "MineShield",
                "Semester Project • UI/UX Lead & Frontend Developer",
                build_mineshield_content(),
            ),
            project_section(
                "section-bitlink",
                "Bitlink (W.I.P.)",
                "Semester Project • Lead Frontend and Backend Developer",
                build_bitlink_content(),
            ),
        ]

    refresh_sections()

    hamburger_button = ft.Container(
        right=58,
        top=30,
        width=64,
        height=34,
        opacity=0,
        scale=0.96,
        animate_opacity=650,
        animate_scale=650,
        alignment=alignment_center(),
        border=border_all(1, alpha(LAVENDER, 0.75)),
        border_radius=6,
        bgcolor=alpha("#1a1c08", 0.72),
        content=text("MENU", color=LAVENDER, size=12, weight=ft.FontWeight.W_800),
        on_click=toggle_menu,
    )

    menu_layer.content = ft.Container(
        width=230,
        padding=12,
        bgcolor=alpha("#1a1c08", 0.95),
        border=border_all(1, alpha(PURPLE, 0.6)),
        border_radius=10,
        content=ft.Column(
            [
                menu_button("Home Page", handler=navigate_home if home_handler else None, url=None if home_handler else HOME_URL),
                menu_button("Qualifications", handler=navigate_qualifications if qualifications_handler else None, url=None if qualifications_handler else QUALIFICATIONS_URL),
                menu_button("Technical Blogs", handler=navigate_blog if blog_handler else None, url=None if blog_handler else HOME_URL),
                menu_button("Distinctions", handler=navigate_home if home_handler else None, url=None if home_handler else HOME_URL),
                menu_button("Evaluations", handler=navigate_home if home_handler else None, url=None if home_handler else HOME_URL),
            ],
            spacing=4,
        ),
    )

    content = ft.Container(
        width=900,
        padding=padding(left=20, top=40, right=20, bottom=40),
        content=ft.Column(
            [
                sections_column,
                ft.TextButton(
                    content="[RETURN TO MATRIX]",
                    on_click=navigate_home if home_handler else None,
                    url=None if home_handler else HOME_URL,
                    style=ft.ButtonStyle(color=LAVENDER, padding=0),
                ),
            ],
            spacing=18,
            expand=True,
        ),
    )

    # Floating props (decorative animated icons) - parity with main-page.py
    def floating_icon(src, size=52, opacity=0.72):
        return ft.Container(
            width=size,
            height=size,
            opacity=opacity,
            content=ft.Image(src=src, width=size, height=size, fit="contain"),
        )

    prop_a = enter_container(content=floating_icon("Image-Assets/circuit_icon.svg", 54, 0.78), visible=False)
    prop_b = enter_container(content=floating_icon("Image-Assets/connection_icon.svg", 44, 0.62), visible=False)
    prop_c = enter_container(content=floating_icon("Image-Assets/cube_icon.svg", 64, 0.52), visible=False)

    floating_props = [
        {"control": prop_a, "x": 0.78, "y": 0.22, "amp_x": 16, "amp_y": 14, "phase": 0.3, "speed": 0.62, "w": 54},
        {"control": prop_b, "x": 0.12, "y": 0.72, "amp_x": 12, "amp_y": 18, "phase": 1.9, "speed": 0.48, "w": 44},
        {"control": prop_c, "x": 0.90, "y": 0.68, "amp_x": 20, "amp_y": 12, "phase": 3.1, "speed": 0.44, "w": 64},
    ]

    root = ft.Container(
        expand=True,
        bgcolor=BG,
        opacity=1,
        scale=1,
        animate_opacity=260,
        animate_scale=260,
        gradient=ft.RadialGradient(
            center=ft.Alignment(0.08, -0.18),
            radius=1.25,
            colors=["#3c2f10", "#1c2c0b", BG],
        ),
        content=ft.Stack(
            [
                *star_controls,
                prop_a,
                prop_b,
                prop_c,
                ft.Container(expand=True, alignment=alignment_center(), content=content),
                hamburger_button,
                ft.Container(content=menu_layer, right=58, top=76),
            ],
            expand=True,
        ),
    )


    async def reveal():
        await asyncio.sleep(0.08)
        hamburger_button.opacity = 1
        hamburger_button.scale = 1

        for prop in floating_props:
            prop["control"].visible = True
            prop["control"].opacity = 0
            prop["control"].scale = 0.82

        page.update()
        await asyncio.sleep(0.06)

        for prop in floating_props:
            prop["control"].opacity = 1
            prop["control"].scale = 1

        page.update()


    def animate(tick):
        viewport_w = page.width or 1200
        viewport_h = page.height or 900
        for star in stars:
            star["x"] += star["speed_x"]
            star["y"] += star["speed_y"]
            if star["y"] > viewport_h:
                star["y"] = 0
                star["x"] = random.randint(0, int(viewport_w))
            if star["x"] < 0:
                star["x"] = viewport_w
            elif star["x"] > viewport_w:
                star["x"] = 0
            star["control"].left = star["x"]
            star["control"].top = star["y"]

        # drift/rotate decorative props
        for prop in floating_props:
            control = prop["control"]
            if not control.visible:
                continue
            drift_x = math.sin(tick * prop["speed"] + prop["phase"]) * prop["amp_x"]
            drift_y = math.cos(tick * (prop["speed"] * 0.83) + prop["phase"]) * prop["amp_y"]
            control.left = viewport_w * prop["x"] - prop["w"] / 2 + drift_x
            control.top = viewport_h * prop["y"] - prop["w"] / 2 + drift_y
            control.rotate = ft.Rotate(math.sin(tick * prop["speed"] + prop["phase"]) * 0.12)

    return root, reveal, animate



async def main(page: ft.Page):
    root, reveal, animate = build_projects_page(page)
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
