import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── Style constants matching Ipsos template ──────────────────────────
BG_OUTER = "#E8E8E8"
BG_CARD  = "#FFFFFF"
BAR_COLORS_3 = ["#8B1A1A", "#4DA6C9", "#999999"]  # dark red, teal-blue, gray

SOURCE_TEXT = "Source: The Harris Poll / Fast Company, Feb 2\u20136, 2024 (n=1,079 U.S. adults)"
COPYRIGHT = "Data: Harris Poll | Visualization style adapted from Ipsos"

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_ipsos_chart(title, question, row_labels, data_cols, col_labels, bar_colors,
                       filename, source=SOURCE_TEXT, copyright_text=COPYRIGHT,
                       figwidth=7, bar_section_left=0.38):
    """
    Ipsos-style horizontal bar chart optimized for small widget display.
    Size C preset: ~50% larger text than original, 280 DPI.

    data_cols: list of lists — data_cols[col_index][row_index] = percentage value
    """
    n_rows = len(row_labels)
    n_cols = len(data_cols)

    # Compact rows with bigger bars
    row_height_in = 0.60
    fig_height = max(4.0, n_rows * row_height_in + 2.8)

    fig = plt.figure(figsize=(figwidth, fig_height))
    fig.patch.set_facecolor(BG_OUTER)

    # Draw card background
    card = mpatches.FancyBboxPatch(
        (0.01, 0.01), 0.98, 0.98,
        boxstyle="round,pad=0.012",
        facecolor=BG_CARD, edgecolor="#cccccc", linewidth=0.8,
        transform=fig.transFigure, zorder=0
    )
    fig.patches.append(card)

    # Vertical zones — headers pushed down near data rows
    title_top = 0.96
    question_y = 0.85
    header_y = 0.76
    chart_top = 0.72
    chart_bottom = 0.10
    chart_height = chart_top - chart_bottom

    # Title
    fig.text(0.05, title_top, title,
             fontsize=20, fontweight="bold", color="#1a1a1a",
             fontfamily="sans-serif", va="top",
             transform=fig.transFigure)
    fig.text(0.05, question_y, question,
             fontsize=12, color="#777777", fontfamily="sans-serif", va="top",
             fontstyle="italic", transform=fig.transFigure)

    # Source at bottom
    fig.text(0.05, 0.04, source,
             fontsize=9, color="#888888", fontfamily="sans-serif")
    fig.text(0.05, 0.015, copyright_text,
             fontsize=8, color="#aaaaaa", fontfamily="sans-serif")

    # Row layout
    row_step = chart_height / n_rows
    bar_h_fig = min(row_step * 0.48, 0.055)

    # Column layout
    bar_area_left = bar_section_left
    bar_area_right = 0.96
    bar_area_width = bar_area_right - bar_area_left
    col_width = bar_area_width / n_cols

    # Column headers
    for c, label in enumerate(col_labels):
        cx = bar_area_left + col_width * c + col_width * 0.35
        fig.text(cx, header_y, label,
                 fontsize=14, fontweight="bold", color="#1a1a1a",
                 fontfamily="sans-serif", ha="center", va="bottom",
                 linespacing=1.15)

    # Draw each row
    for r in range(n_rows):
        row_y_center = chart_top - row_step * r - row_step / 2

        # Row label
        fig.text(bar_area_left - 0.02, row_y_center, row_labels[r],
                 fontsize=13, color="#333333", fontfamily="sans-serif",
                 ha="right", va="center", linespacing=1.25)

        # Bars for each column
        for c in range(n_cols):
            val = data_cols[c][r]

            col_left = bar_area_left + col_width * c + col_width * 0.05
            max_bar_w = col_width * 0.48

            bar_w = (val / 100.0) * max_bar_w
            bar_y = row_y_center - bar_h_fig / 2

            bar = mpatches.FancyBboxPatch(
                (col_left, bar_y), max(bar_w, 0.003), bar_h_fig,
                boxstyle="square,pad=0",
                facecolor=bar_colors[c], edgecolor="none",
                transform=fig.transFigure, zorder=2
            )
            fig.patches.append(bar)

            # Percentage label
            label_x = col_left + bar_w + 0.008
            fig.text(label_x, row_y_center, f"{val}%",
                     fontsize=13, fontweight="bold", color="#333333",
                     fontfamily="sans-serif", ha="left", va="center")

        # Light divider between rows
        if r < n_rows - 1:
            div_y = row_y_center - row_step / 2
            fig.patches.append(mpatches.FancyBboxPatch(
                (0.04, div_y), 0.92, 0.001,
                boxstyle="square,pad=0",
                facecolor="#eeeeee", edgecolor="none",
                transform=fig.transFigure, zorder=1
            ))

    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=280, bbox_inches="tight",
                facecolor=fig.get_facecolor(), pad_inches=0.08)
    plt.close()
    print(f"Saved: {filepath}")


# ══════════════════════════════════════════════════════════════════════
# CHART 1: Attitudes about flying safety (% Agree) by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Younger Americans are less confident\nin air travel safety",
    question="% Agree with each statement",
    row_labels=[
        "Flying is safer than\nother transport",
        "I trust flight teams\nto keep us safe",
        "I trust planes are\nthoroughly inspected",
        "Flying makes me\nfeel nervous",
        "News stories make\nme feel unsafe",
    ],
    data_cols=[
        [69, 79, 72, 67, 72],   # Gen Z
        [73, 80, 75, 63, 64],   # Millennials
        [74, 90, 70, 55, 61],   # Boomers
    ],
    col_labels=["Gen Z\n(18-27)", "Millennial\n(28-42)", "Boomer\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="harris_chart1_attitudes.png",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 2: Awareness of incidents by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Boomers are most aware of recent\nplane safety incidents",
    question="% aware of each incident (select all that apply)",
    row_labels=[
        "Boeing door panel\nblew out midflight",
        "Airbus/military\ncollision in Tokyo",
        "Boeing nose wheel\nfell off at takeoff",
        "Cargo plane crash\nin residential area",
        "None of the above",
    ],
    data_cols=[
        [40, 19, 24, 13, 35],   # Gen Z
        [47, 25, 22, 14, 31],   # Millennials
        [87, 39, 19, 19, 12],   # Boomers
    ],
    col_labels=["Gen Z\n(18-27)", "Millennial\n(28-42)", "Boomer\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="harris_chart2_awareness.png",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 3: Impact on comfort by Gender
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Women feel less comfortable flying\nafter safety incidents",
    question="Impact of incidents on comfort traveling by air",
    row_labels=[
        "More comfortable",
        "No change",
        "Less comfortable",
        "Not at all sure",
    ],
    data_cols=[
        [11, 54, 33, 3],   # Male
        [8, 34, 53, 4],    # Female
        [10, 44, 43, 3],   # Total
    ],
    col_labels=["Male", "Female", "Total"],
    bar_colors=BAR_COLORS_3,
    filename="harris_chart3_comfort_gender.png",
    source=SOURCE_TEXT + " Base: Aware of incident (n=817).",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 4: Impact on comfort by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Gen Z most likely to feel more comfortable\nafter safety incidents",
    question="Impact of incidents on comfort traveling by air",
    row_labels=[
        "More comfortable",
        "No change",
        "Less comfortable",
        "Not at all sure",
    ],
    data_cols=[
        [25, 30, 37, 8],   # Gen Z
        [19, 40, 39, 2],   # Millennials
        [0, 48, 49, 3],    # Boomers
    ],
    col_labels=["Gen Z\n(18-27)", "Millennial\n(28-42)", "Boomer\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="harris_chart4_comfort_gen.png",
    source=SOURCE_TEXT + " Base: Aware of incident.",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 5: Behavioral changes (% More Likely) by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Younger flyers most likely to change\nbehavior after incidents",
    question="% More Likely to do each of the following",
    row_labels=[
        "Wear seatbelt\nwhen not required",
        "Attend to\nsafety materials",
        "Attend to pre-\ntakeoff activities",
        "Monitor plane\nfunctions",
        "Consider type\nof plane",
        "Consider the\nairline booked",
        "Pick seat by\nplane zone",
        "Pick seat by\nrow area",
    ],
    data_cols=[
        [56, 56, 45, 42, 40, 48, 41, 42],   # Gen Z
        [49, 52, 53, 50, 35, 41, 28, 36],   # Millennials
        [50, 48, 41, 39, 35, 30, 26, 26],   # Boomers
    ],
    col_labels=["Gen Z\n(18-27)", "Millennial\n(28-42)", "Boomer\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="harris_chart5_behavior.png",
    source=SOURCE_TEXT + " Base: Plans to fly & aware (n=557).",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 6: Flying safety attitudes by Gender
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Women are more nervous about\nflying than men",
    question="% Agree with each statement",
    row_labels=[
        "Flying is safer than\nother transport",
        "I trust flight teams\nto keep us safe",
        "I trust planes are\nthoroughly inspected",
        "Flying makes me\nfeel nervous",
        "News stories make\nme feel unsafe",
    ],
    data_cols=[
        [64, 87, 74, 50, 53],   # Male
        [74, 88, 72, 68, 74],   # Female
        [69, 86, 73, 59, 64],   # Total
    ],
    col_labels=["Male", "Female", "Total"],
    bar_colors=BAR_COLORS_3,
    filename="harris_chart6_attitudes_gender.png",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 7: Attitudes by Race/Ethnicity
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Air travel safety perceptions\nby race and ethnicity",
    question="% Agree with each statement",
    row_labels=[
        "Flying is safer than\nother transport",
        "I trust flight teams\nto keep us safe",
        "I trust planes are\nthoroughly inspected",
        "Flying makes me\nfeel nervous",
        "News stories make\nme feel unsafe",
    ],
    data_cols=[
        [64, 82, 75, 58, 62],   # White
        [64, 82, 72, 62, 67],   # People of Color
        [69, 86, 73, 59, 64],   # Total
    ],
    col_labels=["White\n(NH/L)", "People of\nColor", "Total"],
    bar_colors=BAR_COLORS_3,
    filename="harris_chart7_attitudes_race.png",
)

print("\nAll 7 charts generated!")
