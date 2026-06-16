import asyncio
import math
import random

import flet as ft
from projects import build_projects_page
from qualifications import build_qualifications_page
from blog import build_blog_page

# System Architecture Colors
BG = "#03020d"
PANEL = "#070514"
PURPLE = "#a100ff"
CYAN = "#4c4cfe"
PINK = "#ff7bf5"
MUTED = "#a5a5c0"
WHITE = "#aca9ff"

# Color Palette Mapping for Skills (Matching the Tag Screenshot Aesthetic)
TAG_COLORS = [
    {"bg": "#1e293b", "text": "#38bdf8"},  # Slate / Cyan Accent
    {"bg": "#2e1065", "text": "#c084fc"},  # Dark Purple / Lavender
    {"bg": "#1c1917", "text": "#f59e0b"},  # Dark Amber / Gold
    {"bg": "#064e3b", "text": "#34d399"},  # Emerald / Mint Green
    {"bg": "#4c0519", "text": "#fb7185"},  # Rose / Light Pink
]

CARDS = [
    {"title": "Projects Engine", "icon": "Image-Assets/projects-icon.svg", "route": "/projects"},
    {"title": "Qualifications", "icon": "Image-Assets/qualifications-icon.svg", "route": "/qualifications"},
    {"title": "Awards & Honors(WIP)", "icon": "Image-Assets/awards-icon.svg", "route": None},
    {"title": "Testimonies(WIP)", "icon": "Image-Assets/testimonies-icon.svg", "route": None},
    {"title": "Technical Blogs", "icon": "Image-Assets/blog_icon_white.svg", "route": "/blog"},
    {"title": "Handles(WIP)", "icon": "Image-Assets/handles_icon_white.svg", "route": None},
]

CONTACTS = [
    ("EMAIL ARCHIVE //", "tegamenoi@gmail.com", "mailto:tegamenoi@gmail.com"),
    ("LINKEDIN NETWORK //", "linkedin.com/in/tegameno-iyambo", "https://www.linkedin.com/in/tegameno-iyambo"),
    ("GITHUB ARCHIVE //", "github.com/Steemiy", "https://github.com/Steemiy"),
    ("MOBILE LINE //", "+264 81 200-3112", None),
]

SKILLS = [
    "#UIDesign","#Flet FrontEnd", "#Intermediate Python", "#AI Development", "#Computational Sciences", "#Unity Game Development", 
    "#Roblox Studio Game Development", "#Natron Video Editing", "#Affinity Graphics Design", "#MATLAB", 
    "#Simulink", "#KiCAD", "#AutoCAD", "#FusionCAD", "#3D Modeling", "#Data Analysis",
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

def paragraph(value, color=MUTED):
    return text(value, color=color, size=13)

def glass_box(content, border_color=PURPLE, pad=24, expand=False, height=None):
    return ft.Container(
        content=content,
        bgcolor=alpha(PANEL, 0.65),
        border=border_all(2, border_color),
        border_radius=6,
        padding=pad,
        expand=expand,
        height=height,
    )

def nav_label(value):
    return text(value.upper(), color=WHITE, size=23, weight=ft.FontWeight.W_900)

def decorative_star(color, size):
    src = "Image-Assets/canva-star-cyan.svg" if color == CYAN else "Image-Assets/canva-star-pink.svg"
    return ft.Container(
        width=size,
        height=size,
        opacity=0.85,
        content=ft.Image(src=src, width=size, height=size, fit="contain"),
    )

def ring_planet():
    return ft.Container(
        width=140,
        height=140,
        opacity=0.95,
        content=ft.Image(src="Image-Assets/ring-planet.svg", width=140, height=140, fit="contain"),
    )

def image_prop(src, width, height=None, opacity=0.9):
    return ft.Container(
        width=width,
        height=height or width,
        opacity=opacity,
        content=ft.Image(src=src, width=width, height=height or width, fit="contain"),
    )

def enter_container(content=None, **kwargs):
    if content is not None:
        kwargs.setdefault("content", content)
    kwargs.setdefault("opacity", 0)
    kwargs.setdefault("scale", 0.94)
    kwargs.setdefault("animate_opacity", 750)
    kwargs.setdefault("animate_scale", 750)
    return ft.Container(**kwargs)

def starfield(width=1920, height=900):
    random.seed(42)
    controls = []
    stars = []
    for _ in range(75):
        size = random.choice([1, 1, 1, 2, 2, 3])
        trail = ft.Container(
            left=0, top=0, width=1, height=1,
            bgcolor=alpha(WHITE, 0.65), border_radius=3, visible=False,
        )
        star = ft.Container(
            left=random.randint(0, width),
            top=random.randint(0, height),
            width=size * 1.2, height=size * 1.2,
            bgcolor=alpha(WHITE, random.uniform(0.35, 0.9)),
            border_radius=3,
        )
        stars.append({
            "x": (random.random() - 0.5) * width,
            "y": (random.random() - 0.5) * height,
            "z": random.random() * 900 + 100,
            "control": star,
            "trail": trail,
            "trail_count": 0,
        })
        controls.extend([trail, star])
    return controls, stars

async def main(page: ft.Page):
    # 1. Fetch and register the clean, web-optimized monospace font
    page.fonts = {
        "TerminalFont": "https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-Regular.ttf"
    }
    
    # 2. Apply it globally so every text element changes automatically
    page.theme = ft.Theme(font_family="TerminalFont")
    
    # Force the page to refresh and render the new typography
    page.update()
    
    page.title = "Tegameno Iyambo // Portfolio Matrix"
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.window_width = 1240
    page.window_height = 850
    page.theme_mode = ft.ThemeMode.DARK

    state = {"menu": False, "card": 0, "warp": 0}
    star_controls, stars = starfield()

    landing_layer = ft.Container(expand=True, alignment=alignment_center())
    portfolio_layer = ft.Container(expand=True)
    menu_layer = ft.Container(visible=False)

    def open_card(index):
        card = CARDS[index]
        state["menu"] = False
        menu_layer.visible = False
        hamburger_label.value = "MENU"

        if card["route"]:
            page.go(card["route"])
            return
        set_card(index)

    def make_card(index):
        card = CARDS[index]
        active = index == state["card"]
        card_surface = glass_box(
            ft.Column(
                [
                    ft.Container(
                        width=32, height=32, opacity=0.9,
                        content=ft.Image(src=card["icon"], width=32, height=32, fit="contain"),
                    ),
                    text(card["title"], size=13, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border_color=CYAN if active else PURPLE,
            pad=10,
            height=105,
        )
        card_surface.width = 180
        return ft.TextButton(
            content=card_surface,
            on_click=lambda e: open_card(index),
            style=ft.ButtonStyle(padding=0),
        )

    # Fixed: Removed ft.ScrollMode.DISABLE entirely to support older layout engines safely
    cards_column = ft.Column(spacing=12, scroll=None)

    def refresh_cards():
        cards_column.controls = [
            ft.Row(
                [make_card(index) for index in range(row_start, min(row_start + 2, len(CARDS)))],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            for row_start in range(0, len(CARDS), 2)
        ]

    def set_card(index):
        state["card"] = index % len(CARDS)
        refresh_cards()
        page.update()

    def toggle_menu(_=None):
        state["menu"] = not state["menu"]
        menu_layer.visible = state["menu"]
        hamburger_label.value = "X" if state["menu"] else "MENU"
        page.update()

    def go_to_section(index):
        state["menu"] = False
        menu_layer.visible = False
        hamburger_label.value = "MENU"
        set_card(index)

    # Core Competencies Skill-Pill Renderer Engine
    def build_skill_chips():
        chips = []
        for i, skill in enumerate(SKILLS):
            theme = TAG_COLORS[i % len(TAG_COLORS)]
            chips.append(
                ft.Container(
                    content=text(skill, color=theme["text"], size=12, weight=ft.FontWeight.W_600),
                    bgcolor=alpha(theme["bg"], 0.75),
                    padding=padding(left=12, right=12, top=6, bottom=6),
                    border_radius=14,
                )
            )
        return ft.Row(controls=chips, wrap=True, spacing=8, run_spacing=8)

    voyage_button = ft.ElevatedButton(
        content=text("INITIATE PORTFOLIO.PY", color=PINK, size=15, weight=ft.FontWeight.W_900),
        on_click=lambda e: page.run_task(initiate_voyage, e),
    )
    landing_layer.content = voyage_button

    async def initiate_voyage(_):
        landing_wrapper.visible = False
        portfolio_wrapper.visible = True
        hamburger_button.visible = True
        portfolio_wrapper.opacity = 0
        portfolio_wrapper.scale = 0.95
        hamburger_button.opacity = 0
        hamburger_button.scale = 0.9
        for section in section_wrappers:
            section.opacity = 0
            section.scale = 0.94
        for prop in floating_props:
            prop["control"].visible = True
            prop["control"].opacity = 0
            prop["control"].scale = 0.82
        state["warp"] = 28
        page.update()
        await asyncio.sleep(0.08)
        portfolio_wrapper.opacity = 1
        portfolio_wrapper.scale = 1
        hamburger_button.opacity = 1
        hamburger_button.scale = 1
        for section in section_wrappers:
            section.opacity = 1
            section.scale = 1
        for prop in floating_props:
            prop["control"].opacity = 1
            prop["control"].scale = 1
        page.update()

    profile_panel = ft.Column(
        [
            nav_label("Profile"),
            glass_box(
                ft.Column(
                    [
                        ft.Stack(
                            [
                                ft.Container(left=0, top=0, width=18, height=2, bgcolor=CYAN),
                                ft.Container(left=0, top=0, width=2, height=18, bgcolor=CYAN),
                            ],
                            width=18,
                            height=18,
                        ),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Container(
                                            height=385,
                                            border=border_all(2, PURPLE),
                                            border_radius=12,
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            bgcolor=alpha("#5D3FD3", 0.07),
                                            content=ft.Image(src="Image-Assets/mtmgt.png", fit="cover"),
                                        ),
                                        ft.Column(
                                            [
                                                tag("SYSTEM PARAMETERS //"),
                                                paragraph("Tegameno Iyambo | Electronics & Computer Engineering Student | University of Namibia | A central archive of my projects, experiments, and multidisciplinary work."),
                                            ],
                                            spacing=5,
                                        ),
                                    ],
                                    spacing=16,
                                    expand=True,
                                ),
                                ft.Container(
                                    width=46,
                                    alignment=alignment_center(),
                                    content=ft.Image(
                                        src="Image-Assets/profile-name-rotated.svg",
                                        width=46,
                                        height=340,
                                        fit="contain",
                                    ),
                                ),
                            ],
                            spacing=18,
                            expand=True,
                            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),
                expand=True,
            ),
        ],
        spacing=14,
        expand=True,
    )

    refresh_cards()
    
    # Combined Layout Engine for Center Panel (Grid Matrix + Skills Component)
    cards_panel = ft.Column(
        [
            nav_label("Cards"),
            ft.Container(content=cards_column, height=360),
            tag("CORE_COMPETENCIES //"),
            ft.Container(
                content=glass_box(
                    content=ft.Column([build_skill_chips()], scroll=ft.ScrollMode.AUTO),
                    border_color=alpha(CYAN, 0.5),
                    pad=16,
                    expand=True,
                ),
                alignment=alignment_center(),
                expand=True,
            )
        ],
        spacing=14,
        expand=True,
    )

    contact_controls = []
    for label, value, url in CONTACTS:
        value_control = ft.TextButton(content=value, url=url, style=ft.ButtonStyle(color=WHITE, padding=0)) if url else text(value, size=13, weight=ft.FontWeight.W_600)
        contact_controls.append(
            ft.Container(
                padding=padding(bottom=8),
                border=border_only(bottom=border_side(1, alpha(WHITE, 0.12))),
                content=ft.Column([tag(label), value_control], spacing=0),
            )
        )

    contact_panel = ft.Column(
        [
            nav_label("Contact"),
            glass_box(
                ft.Column(
                    [
                        ft.Column(
                            [
                                tag("COMMUNICATION ROUTING"),
                                text("Get In Touch", size=20, weight=ft.FontWeight.W_800),
                                paragraph("Direct contact endpoints for engineering operations data tracking requests."),
                            ],
                            spacing=-4,
                        ),
                        ft.Column(contact_controls, spacing=14),
                        ft.Container(
                            padding=padding(top=12),
                            border=border_only(top=border_side(1, alpha(WHITE, 0.14))),
                            content=ft.Column(
                                [
                                    tag("DIRECTORY STATUS:"),
                                    text("Secure Terminal Active", size=13, weight=ft.FontWeight.W_600),
                                ],
                                spacing=3,
                            ),
                        ),
                    ],
                    spacing=24,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                ),
                expand=True,
            ),
        ],
        spacing=14,
        expand=True,
    )

    section_wrappers = [
        enter_container(profile_panel, width=380, height=680),
        enter_container(cards_panel, width=410, height=680),
        enter_container(contact_panel, width=410, height=680),
    ]

    portfolio_layer.content = ft.Container(
        width=1240,
        height=680,
        alignment=alignment_center(),
        content=ft.Row(
            section_wrappers,
            spacing=35,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    hamburger_label = text("MENU", color=CYAN, size=12, weight=ft.FontWeight.W_800)
    hamburger_button = enter_container(
        right=58, top=30, visible=False, width=64, height=34,
        alignment=alignment_center(),
        border=border_all(1, alpha(CYAN, 0.7)), border_radius=6,
        bgcolor=alpha("#0c081c", 0.72),
        content=ft.TextButton(
            content=hamburger_label,
            on_click=toggle_menu,
            style=ft.ButtonStyle(padding=0),
        ),
    )

    menu_layer.content = ft.Container(
        width=230, padding=12,
        bgcolor=alpha("#0c081c", 0.95), border=border_all(1, alpha(PURPLE, 0.6)), border_radius=10,
        content=ft.Column(
            [
                ft.TextButton(content=text("Projects", color=MUTED, size=13), on_click=lambda e: page.go("/projects")),
                ft.TextButton(content=text("Qualifications", color=MUTED, size=13), on_click=lambda e: page.go("/qualifications")),
                ft.TextButton(content=text("Technical Blogs", color=MUTED, size=13), on_click=lambda e: page.go("/blog")),
                ft.TextButton(content=text("Awards(WIP)", color=MUTED, size=13), on_click=lambda e: go_to_section(2)),
                ft.TextButton(content=text("Testimonies(WIP)", color=MUTED, size=13), on_click=lambda e: go_to_section(3)),
                ft.TextButton(content=text("Handles(WIP)", color=MUTED, size=13), on_click=lambda e: go_to_section(5)),
            ],
            spacing=4,
        ),
    )

    prop_one = enter_container(content=decorative_star(PINK, 50), visible=False)
    prop_two = enter_container(content=decorative_star(CYAN, 35), visible=False)
    prop_three = enter_container(content=decorative_star(PINK, 28), visible=False)
    prop_four = enter_container(content=decorative_star(CYAN, 44), visible=False)
    prop_five = enter_container(content=image_prop("Image-Assets/ring-planet.svg", 86, opacity=0.72), visible=False)
    prop_six = enter_container(content=image_prop("Image-Assets/ring-planet.svg", 54, opacity=0.55), visible=False)
    prop_planet = enter_container(content=ring_planet(), visible=False)
    
    floating_props = [
        {"control": prop_one, "x": 0.66, "y": 0.22, "amp_x": 12, "amp_y": 16, "phase": 0.2, "speed": 0.75, "w": 50},
        {"control": prop_two, "x": 0.06, "y": 0.83, "amp_x": 10, "amp_y": 14, "phase": 1.7, "speed": 0.62, "w": 35},
        {"control": prop_three, "x": 0.18, "y": 0.18, "amp_x": 8, "amp_y": 18, "phase": 2.6, "speed": 0.88, "w": 28},
        {"control": prop_four, "x": 0.88, "y": 0.44, "amp_x": 16, "amp_y": 10, "phase": 3.4, "speed": 0.54, "w": 44},
        {"control": prop_five, "x": 0.25, "y": 0.68, "amp_x": 18, "amp_y": 12, "phase": 4.5, "speed": 0.48, "w": 86},
        {"control": prop_six, "x": 0.78, "y": 0.76, "amp_x": 9, "amp_y": 20, "phase": 5.1, "speed": 0.66, "w": 54},
        {"control": prop_planet, "x": 0.965, "y": 0.89, "amp_x": 12, "amp_y": 16, "phase": 2.2, "speed": 0.42, "w": 140},
    ]

    portfolio_wrapper = enter_container(
        content=portfolio_layer, expand=True, alignment=alignment_center(),
        padding=padding(left=36, right=36, top=48, bottom=48), visible=False,
    )
    landing_wrapper = ft.Container(content=landing_layer, expand=True, alignment=alignment_center())

    root = ft.Container(
        expand=True, bgcolor=alpha("#5D3FD3", 0.3), animate_opacity=260, animate_scale=260,
        gradient=ft.RadialGradient(center=ft.Alignment(0, 0), radius=1.15, colors=["#0d092b", BG]),
        content=ft.Stack(
            [
                *star_controls, prop_one, prop_two, prop_three, prop_four, prop_five, prop_six, prop_planet,
                portfolio_wrapper, landing_wrapper, hamburger_button,
                ft.Container(content=menu_layer, right=58, top=76),
            ],
            expand=True,
        ),
    )

    routed_view = {"name": "home", "animate": None}

    async def mount_view(view_root, reveal=None):
        view_root.animate_opacity = 260
        view_root.animate_scale = 260
        view_root.opacity = 0
        view_root.scale = 0.985
        page.controls.clear()
        page.add(view_root)
        page.update()
        await asyncio.sleep(0.04)
        view_root.opacity = 1
        view_root.scale = 1
        page.update()
        if reveal:
            await reveal()

    async def handle_route(_):
        if not page.controls:
            return
        current = page.controls[0]
        current.animate_opacity, current.animate_scale = 220, 220
        current.opacity, current.scale = 0, 0.985
        page.update()
        await asyncio.sleep(0.22)

        if page.route == "/projects":
            root_p, rev_p, anim_p = build_projects_page(
                page,
                home_handler=lambda e=None: page.go("/"),
                qualifications_handler=lambda e=None: page.go("/qualifications"),
                blog_handler=lambda e=None: page.go("/blog"),
            )
            routed_view.update({"name": "projects", "animate": anim_p})
            await mount_view(root_p, rev_p)
        elif page.route == "/qualifications":
            root_q, rev_q, anim_q = build_qualifications_page(
                page,
                home_handler=lambda e=None: page.go("/"),
                projects_handler=lambda e=None: page.go("/projects"),
                blog_handler=lambda e=None: page.go("/blog"),
            )
            routed_view.update({"name": "qualifications", "animate": anim_q})
            await mount_view(root_q, rev_q)
        elif page.route == "/blog":
            root_b, rev_b, anim_b = build_blog_page(
                page,
                home_handler=lambda e=None: page.go("/"),
                projects_handler=lambda e=None: page.go("/projects"),
                qualifications_handler=lambda e=None: page.go("/qualifications"),
            )
            routed_view.update({"name": "blog", "animate": anim_b})
            await mount_view(root_b, rev_b)
        else:
            routed_view.update({"name": "home", "animate": None})
            await mount_view(root)

    page.on_route_change = lambda e: page.run_task(handle_route, e)
    page.add(root)

    tick = 0.0
    frame_count = 0
    while True:
        tick += 0.06
        frame_count += 1
        if routed_view["animate"]:
            routed_view["animate"](tick)
            page.update()
            await asyncio.sleep(0.06)
            continue

        warp_active = state["warp"] > 0
        speed = 42 if warp_active else 2
        if state["warp"] > 0:
            state["warp"] -= 1

        viewport_w, viewport_h = page.width or 1400, page.height or 900
        center_x, center_y = viewport_w / 2, viewport_h / 2

        for star in stars:
            old_scale = 360 / star["z"]
            old_px = star["x"] * old_scale + center_x
            old_py = star["y"] * old_scale + center_y

            star["z"] -= speed
            if star["z"] <= 1:
                star["x"] = (random.random() - 0.5) * viewport_w
                star["y"] = (random.random() - 0.5) * viewport_h
                star["z"] = 1000
                old_px = star["x"] * 0.36 + center_x
                old_py = star["y"] * 0.36 + center_y

            scale = 360 / star["z"]
            px, py = star["x"] * scale + center_x, star["y"] * scale + center_y
            radius = max(1.2, (1 - star["z"] / 1000) * 3.84)
            opacity = max(0.25, min(0.95, 1 - star["z"] / 1000))
            
            star["control"].left, star["control"].top = px, py
            star["control"].width, star["control"].height = radius, radius
            star["control"].opacity = opacity

            trail = star["trail"]
            if warp_active:
                dx, dy = px - old_px, py - old_py
                length = min(150, max(14, math.hypot(dx, dy) * 2.4))
                trail.visible = True
                trail.left, trail.top = px - length, py - max(1, radius * 0.35)
                trail.width, trail.height = length, max(1, radius * 0.7)
                trail.rotate = ft.Rotate(math.atan2(dy, dx))
                trail.opacity = max(0.15, opacity * 0.75)
                star["trail_count"] = 8
            else:
                if star["trail_count"] > 0:
                    trail.opacity = max(0, trail.opacity - 0.1)
                    star["trail_count"] -= 1
                else:
                    trail.visible = False

        for prop in floating_props:
            control = prop["control"]
            if not control.visible:
                continue
            drift_x = math.sin(tick * prop["speed"] + prop["phase"]) * prop["amp_x"]
            drift_y = math.cos(tick * (prop["speed"] * 0.83) + prop["phase"]) * prop["amp_y"]
            control.left = viewport_w * prop["x"] - prop["w"] / 2 + drift_x
            control.top = viewport_h * prop["y"] - prop["w"] / 2 + drift_y
            control.rotate = ft.Rotate(math.sin(tick * prop["speed"] + prop["phase"]) * 0.12)

        page.update()
        await asyncio.sleep(0.06)

ft.app(target=main, assets_dir=".", view=ft.AppView.WEB_BROWSER)
