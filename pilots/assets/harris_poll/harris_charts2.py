import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Style constants matching Ipsos template ──────────────────────────
BG_OUTER = "#E8E8E8"
BG_CARD  = "#FFFFFF"
BAR_COLORS_3 = ["#8B1A1A", "#4DA6C9", "#999999"]  # dark red, teal-blue, gray

SOURCE_TEXT = "Source: The Harris Poll / Fast Company, fielded February 2 \u2013 February 6, 2024 among 1,079 U.S. adults."
COPYRIGHT = "Data: Harris Poll | Visualization style adapted from Ipsos"


def create_ipsos_chart(title, question, row_labels, data_cols, col_labels, bar_colors,
                       filename, source=SOURCE_TEXT, copyright_text=COPYRIGHT,
                       figwidth=13, bar_section_left=0.32):
    """
    Replicates the Ipsos horizontal bar chart style.

    data_cols: list of lists — data_cols[col_index][row_index] = percentage value
    """
    n_rows = len(row_labels)
    n_cols = len(data_cols)

    # Size figure based on content — cap row height so few-row charts aren't too spacious
    row_height_in = min(1.1, 5.0 / max(n_rows, 1))
    fig_height = max(5, n_rows * row_height_in + 3.2)

    fig = plt.figure(figsize=(figwidth, fig_height))
    fig.patch.set_facecolor(BG_OUTER)

    # Draw card background
    card = mpatches.FancyBboxPatch(
        (0.015, 0.015), 0.97, 0.97,
        boxstyle="round,pad=0.015",
        facecolor=BG_CARD, edgecolor="#cccccc", linewidth=0.8,
        transform=fig.transFigure, zorder=0
    )
    fig.patches.append(card)

    # Compute vertical zones (in figure fractions)
    title_top = 0.95
    question_y = 0.91
    header_y = 0.83          # column headers
    chart_top = 0.79         # first row starts here
    chart_bottom = 0.09
    chart_height = chart_top - chart_bottom

    # Title area
    fig.text(0.05, title_top, title,
             fontsize=17, fontweight="bold", color="#1a1a1a",
             fontfamily="sans-serif", va="top")
    fig.text(0.05, question_y, question,
             fontsize=10.5, color="#555555", fontfamily="sans-serif", va="top")

    # Source at bottom
    fig.text(0.05, 0.035, source,
             fontsize=7.5, color="#666666", fontfamily="sans-serif")
    fig.text(0.05, 0.012, copyright_text,
             fontsize=7, color="#aaaaaa", fontfamily="sans-serif")

    # Each row gets equal vertical space (capped)
    row_step = chart_height / n_rows
    bar_h_fig = min(row_step * 0.35, 0.035)  # bar thickness

    # Column layout
    bar_area_left = bar_section_left
    bar_area_right = 0.95
    bar_area_width = bar_area_right - bar_area_left
    col_width = bar_area_width / n_cols

    # Draw column headers
    for c, label in enumerate(col_labels):
        cx = bar_area_left + col_width * c + col_width * 0.35
        fig.text(cx, header_y, label,
                 fontsize=12, fontweight="bold", color="#1a1a1a",
                 fontfamily="sans-serif", ha="center", va="bottom")

    # Draw each row
    for r in range(n_rows):
        row_y_center = chart_top - row_step * r - row_step / 2

        # Row label on left
        fig.text(bar_area_left - 0.015, row_y_center, row_labels[r],
                 fontsize=11, color="#333333", fontfamily="sans-serif",
                 ha="right", va="center", linespacing=1.3)

        # Draw bars for each column
        for c in range(n_cols):
            val = data_cols[c][r]

            col_left = bar_area_left + col_width * c + col_width * 0.05
            max_bar_w = col_width * 0.55

            bar_w = (val / 100.0) * max_bar_w
            bar_y = row_y_center - bar_h_fig / 2

            bar = mpatches.FancyBboxPatch(
                (col_left, bar_y), max(bar_w, 0.003), bar_h_fig,
                boxstyle="square,pad=0",
                facecolor=bar_colors[c], edgecolor="none",
                transform=fig.transFigure, zorder=2
            )
            fig.patches.append(bar)

            label_x = col_left + bar_w + 0.008
            fig.text(label_x, row_y_center, f"{val}%",
                     fontsize=11, fontweight="bold", color="#333333",
                     fontfamily="sans-serif", ha="left", va="center")

        # Light horizontal divider between rows
        if r < n_rows - 1:
            div_y = row_y_center - row_step / 2
            fig.patches.append(mpatches.FancyBboxPatch(
                (0.04, div_y), 0.92, 0.001,
                boxstyle="square,pad=0",
                facecolor="#eeeeee", edgecolor="none",
                transform=fig.transFigure, zorder=1
            ))

    plt.savefig(filename, dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor(), pad_inches=0.1)
    plt.close()
    print(f"Saved: {filename}")


# ══════════════════════════════════════════════════════════════════════
# CHART 1: Attitudes about flying safety (% Agree) by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Younger Americans are less confident in air travel safety",
    question="Q: How much do you agree or disagree with each of the following statements? (% Agree)",
    row_labels=[
        "Flying is safer than other\nlong-distance transport",
        "I trust flight teams to\nkeep passengers safe",
        "I trust planes are\nthoroughly inspected",
        "Flying makes me\nfeel nervous",
        "News stories about incidents\nmake me feel unsafe flying",
    ],
    data_cols=[
        [69, 79, 72, 67, 72],   # Gen Z
        [73, 80, 75, 63, 64],   # Millennials
        [74, 90, 70, 55, 61],   # Boomers
    ],
    col_labels=["Gen Z\n(18-27)", "Millennials\n(28-42)", "Boomers\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="/tmp/harris_chart1_attitudes.png",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 2: Awareness of incidents by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Boomers are most aware of recent plane safety incidents",
    question="Q: Which of the following recent plane safety incidents were you aware of? (Select all that apply)",
    row_labels=[
        "Boeing door panel\nblew out midflight",
        "Airbus jet collided with\nmilitary plane in Tokyo",
        "Boeing nose wheel\nfell off before takeoff",
        "Cargo plane crashed in\nresidential area",
        "None of the above",
    ],
    data_cols=[
        [40, 19, 24, 13, 35],   # Gen Z
        [47, 25, 22, 14, 31],   # Millennials
        [87, 39, 19, 19, 12],   # Boomers
    ],
    col_labels=["Gen Z\n(18-27)", "Millennials\n(28-42)", "Boomers\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="/tmp/harris_chart2_awareness.png",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 3: Impact on comfort by Gender
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Women are more likely to feel less comfortable flying after incidents",
    question="Q: What impact have recent plane safety incidents had on your comfort traveling by air?",
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
    filename="/tmp/harris_chart3_comfort_gender.png",
    source=SOURCE_TEXT + " Base: Aware of a recent incident (n=817).",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 4: Impact on comfort by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Gen Z is most likely to feel more comfortable after safety incidents",
    question="Q: What impact have recent plane safety incidents had on your comfort traveling by air?",
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
    col_labels=["Gen Z\n(18-27)", "Millennials\n(28-42)", "Boomers\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="/tmp/harris_chart4_comfort_gen.png",
    source=SOURCE_TEXT + " Base: Aware of a recent incident.",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 5: Behavioral changes (% More Likely) by Generation
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Younger flyers are most likely to change behavior after safety incidents",
    question="Q: Have recent incidents made you more or less likely to do each of the following? (% More Likely)",
    row_labels=[
        "Wear seatbelt\nwhen not required",
        "Pay attention to\nsafety materials",
        "Pay attention to\npre-takeoff activities",
        "Monitor plane\nfunctions",
        "Consider the type\nof plane",
        "Consider the\nairline booked",
        "Select seat in\nspecific zone",
        "Select seat in\nspecific row area",
    ],
    data_cols=[
        [56, 56, 45, 42, 40, 48, 41, 42],   # Gen Z
        [49, 52, 53, 50, 35, 41, 28, 36],   # Millennials
        [50, 48, 41, 39, 35, 30, 26, 26],   # Boomers
    ],
    col_labels=["Gen Z\n(18-27)", "Millennials\n(28-42)", "Boomers\n(59-77)"],
    bar_colors=BAR_COLORS_3,
    filename="/tmp/harris_chart5_behavior.png",
    source=SOURCE_TEXT + " Base: Plans to fly & aware of incident (n=557).",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 6: Flying safety attitudes by Gender
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Women are more nervous about flying than men",
    question="Q: How much do you agree or disagree with each of the following statements? (% Agree)",
    row_labels=[
        "Flying is safer than other\nlong-distance transport",
        "I trust flight teams to\nkeep passengers safe",
        "I trust planes are\nthoroughly inspected",
        "Flying makes me\nfeel nervous",
        "News stories about incidents\nmake me feel unsafe flying",
    ],
    data_cols=[
        [64, 87, 74, 50, 53],   # Male
        [74, 88, 72, 68, 74],   # Female
        [69, 86, 73, 59, 64],   # Total
    ],
    col_labels=["Male", "Female", "Total"],
    bar_colors=BAR_COLORS_3,
    filename="/tmp/harris_chart6_attitudes_gender.png",
)

# ══════════════════════════════════════════════════════════════════════
# CHART 7: Attitudes by Race/Ethnicity
# ══════════════════════════════════════════════════════════════════════
create_ipsos_chart(
    title="Air travel safety perceptions by race and ethnicity",
    question="Q: How much do you agree or disagree with each of the following statements? (% Agree)",
    row_labels=[
        "Flying is safer than other\nlong-distance transport",
        "I trust flight teams to\nkeep passengers safe",
        "I trust planes are\nthoroughly inspected",
        "Flying makes me\nfeel nervous",
        "News stories about incidents\nmake me feel unsafe flying",
    ],
    data_cols=[
        [64, 82, 75, 58, 62],   # White
        [64, 82, 72, 62, 67],   # People of Color
        [69, 86, 73, 59, 64],   # Total
    ],
    col_labels=["White Only\n(NH/L)", "All People\nof Color", "Total"],
    bar_colors=BAR_COLORS_3,
    filename="/tmp/harris_chart7_attitudes_race.png",
)

print("\nAll 7 charts generated!")
