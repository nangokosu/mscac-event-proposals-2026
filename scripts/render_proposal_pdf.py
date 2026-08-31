"""Render an MScAC proposal Markdown file to its matching PDF for submission.

Converts one proposal Markdown file — written to the fixed template defined
in this project's CLAUDE.md (an H2 title, H3 section headers, bold labels,
a single GitHub-style pipe table for the budget, and bullet lists) — into a
PDF using ReportLab's Platypus layer (Paragraph/Table/ListFlowable), so
`proposed/` and `approved/` can hold the `.md` + `.pdf` pair the README's
workflow expects.

This is a template-specific renderer, not a general Markdown-to-PDF
converter: it only understands the subset of Markdown the proposal
template actually uses.

Usage:
    python3 scripts/render_proposal_pdf.py proposed/<file>.md proposed/<file>.pdf

Requires: reportlab (`pip install reportlab`).
"""

import re
import sys

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch as INCH
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    ListFlowable,
    ListItem,
)

# Regex for a GitHub-style pipe-table row, e.g. "| a | b | c |".
# Group 1 captures everything between the outer pipes as one raw string;
# callers still need to split that string on "|" themselves to get cells.
PIPE_TABLE_ROW_PATTERN = re.compile(r"^\s*\|(.+)\|\s*$")

# A table's second row is the header/body separator, e.g. "| :--- | :--- |".
# Every cell in it is dashes/colons only, so this pattern distinguishes it
# from a genuine data row.
PIPE_TABLE_SEPARATOR_PATTERN = re.compile(r"^[\s|:-]+$")


def markdown_inline_to_reportlab_markup(source_text):
    """Convert the small set of inline Markdown the template uses to ReportLab's XML markup.

    Args:
        source_text: Raw Markdown text for a single line or cell (e.g.
            "**Event:** [Event Name]").

    Returns:
        The same text with "**bold**" spans replaced by ReportLab's
        "<b>bold</b>" tags, ready to pass into a Paragraph.
    """
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", source_text)


def parse_pipe_table_block(markdown_lines, start_line_index):
    """Parse a contiguous block of pipe-table lines into a 2-D list of cell strings.

    Args:
        markdown_lines: The full list of source lines.
        start_line_index: Index of the table's header row within
            markdown_lines.

    Returns:
        A tuple of (table_rows, next_line_index) where table_rows is a
        list of rows (each a list of cell strings, inline Markdown
        already converted to ReportLab markup) and next_line_index is the
        index of the first line after the table.
    """
    table_rows = []
    current_line_index = start_line_index
    while current_line_index < len(markdown_lines):
        line = markdown_lines[current_line_index]
        match = PIPE_TABLE_ROW_PATTERN.match(line)
        if not match:
            # First non-pipe-row line ends the table block.
            break
        # Skip the "| :--- | :--- |" alignment separator row entirely.
        if PIPE_TABLE_SEPARATOR_PATTERN.match(match.group(1)):
            current_line_index += 1
            continue
        cell_texts = [cell.strip() for cell in match.group(1).split("|")]
        table_rows.append(
            [markdown_inline_to_reportlab_markup(cell) for cell in cell_texts]
        )
        current_line_index += 1
    return table_rows, current_line_index


def build_pdf_story(markdown_lines, paragraph_styles):
    """Walk the proposal's Markdown lines and build the list of ReportLab flowables.

    Args:
        markdown_lines: The full list of source lines from the proposal file.
        paragraph_styles: The ReportLab stylesheet (plus the project's
            custom styles) to draw named styles from.

    Returns:
        A list of ReportLab flowables (Paragraph, Table, Spacer,
        HRFlowable, ListFlowable) representing the whole document, in
        top-to-bottom order.
    """
    pdf_story = []
    line_index = 0
    while line_index < len(markdown_lines):
        line = markdown_lines[line_index].rstrip("\n")
        stripped_line = line.strip()

        if stripped_line == "":
            line_index += 1
            continue

        if stripped_line == "---":
            # "---" is a Markdown thematic break; render it as a ruled
            # divider with spacing above and below.
            pdf_story.append(Spacer(1, 6))
            pdf_story.append(HRFlowable(width="100%", color=colors.grey, thickness=0.5))
            pdf_story.append(Spacer(1, 6))
            line_index += 1
            continue

        if stripped_line.startswith("### "):
            heading_text = markdown_inline_to_reportlab_markup(stripped_line[len("### "):])
            pdf_story.append(Paragraph(heading_text, paragraph_styles["ProposalH3"]))
            line_index += 1
            continue

        if stripped_line.startswith("## "):
            heading_text = markdown_inline_to_reportlab_markup(stripped_line[len("## "):])
            pdf_story.append(Paragraph(heading_text, paragraph_styles["ProposalH2"]))
            line_index += 1
            continue

        if PIPE_TABLE_ROW_PATTERN.match(stripped_line):
            table_rows, line_index = parse_pipe_table_block(markdown_lines, line_index)
            # Render every cell as a Paragraph (not a bare string) so long
            # cell text wraps instead of overflowing the page width. The
            # TableStyle below paints the header row's background dark, so
            # the header row's own cells must use the white-text style —
            # TableStyle's TEXTCOLOR command has no effect on text inside
            # a Paragraph flowable, only on plain-string cells.
            wrapped_rows = [
                [
                    Paragraph(
                        cell,
                        paragraph_styles["ProposalTableHeader"]
                        if row_index == 0
                        else paragraph_styles["ProposalTableCell"],
                    )
                    for cell in row
                ]
                for row_index, row in enumerate(table_rows)
            ]
            # 1.6 * INCH = the 0.8" left + 0.8" right margins configured on
            # the SimpleDocTemplate in render_proposal_markdown_to_pdf;
            # kept in sync manually since the table is built before the
            # document object exists.
            page_content_width = LETTER[0] - 1.6 * INCH
            # The description column holds free-form text (the longest
            # content in the table) and always gets a fixed 45% share;
            # every other column holds a short numeric/quantity value, so
            # the remaining width is split evenly across however many of
            # those columns the table actually has (derived from the
            # parsed header row, not assumed to be a fixed count).
            DESCRIPTION_COLUMN_WIDTH_FRACTION = 0.45
            column_count = len(table_rows[0])
            description_column_width = page_content_width * DESCRIPTION_COLUMN_WIDTH_FRACTION
            other_column_width = (page_content_width - description_column_width) / (column_count - 1)
            column_widths = [description_column_width] + [other_column_width] * (column_count - 1)
            budget_table = Table(wrapped_rows, colWidths=column_widths, repeatRows=1)
            budget_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f2f2f")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
                    ]
                )
            )
            pdf_story.append(Spacer(1, 6))
            pdf_story.append(budget_table)
            pdf_story.append(Spacer(1, 6))
            continue

        if stripped_line.startswith("* "):
            # Collect every consecutive "* " line into one bullet_items
            # list so they render as a single ListFlowable, not one
            # separate list per item.
            bullet_items = []
            while line_index < len(markdown_lines) and markdown_lines[line_index].strip().startswith("* "):
                bullet_text = markdown_inline_to_reportlab_markup(
                    markdown_lines[line_index].strip()[len("* "):]
                )
                bullet_items.append(ListItem(Paragraph(bullet_text, paragraph_styles["ProposalBody"])))
                line_index += 1
            pdf_story.append(ListFlowable(bullet_items, bulletType="bullet", leftIndent=18))
            continue

        # Plain paragraph line (covers **Total Budget Requested: $X** too).
        paragraph_text = markdown_inline_to_reportlab_markup(stripped_line)
        pdf_story.append(Paragraph(paragraph_text, paragraph_styles["ProposalBody"]))
        line_index += 1

    return pdf_story


def render_proposal_markdown_to_pdf(source_markdown_path, output_pdf_path):
    """Render one MScAC proposal Markdown file to a PDF at the given path.

    Args:
        source_markdown_path: Path to the input .md proposal file.
        output_pdf_path: Path to write the generated .pdf to.
    """
    with open(source_markdown_path, "r", encoding="utf-8") as markdown_file:
        markdown_lines = markdown_file.readlines()

    base_styles = getSampleStyleSheet()
    paragraph_styles = {
        "ProposalH2": ParagraphStyle(
            "ProposalH2", parent=base_styles["Heading1"], fontSize=16, spaceAfter=10
        ),
        "ProposalH3": ParagraphStyle(
            "ProposalH3", parent=base_styles["Heading2"], fontSize=12.5, spaceBefore=10, spaceAfter=6
        ),
        "ProposalBody": ParagraphStyle(
            "ProposalBody", parent=base_styles["Normal"], fontSize=10, leading=14, spaceAfter=6
        ),
        "ProposalTableCell": ParagraphStyle(
            "ProposalTableCell", parent=base_styles["Normal"], fontSize=9, leading=12
        ),
    }
    # Style for header-row cells: white text against the dark header
    # background set in build_pdf_story's TableStyle. TableStyle's
    # TEXTCOLOR command doesn't reach text inside a Paragraph flowable, so
    # build_pdf_story selects this style for row 0 instead.
    paragraph_styles["ProposalTableHeader"] = ParagraphStyle(
        "ProposalTableHeader", parent=paragraph_styles["ProposalTableCell"], textColor=colors.white
    )

    pdf_story = build_pdf_story(markdown_lines, paragraph_styles)

    document = SimpleDocTemplate(
        output_pdf_path,
        pagesize=LETTER,
        topMargin=0.8 * INCH,
        bottomMargin=0.8 * INCH,
        leftMargin=0.8 * INCH,
        rightMargin=0.8 * INCH,
    )
    document.build(pdf_story)


if __name__ == "__main__":
    source_markdown_path, output_pdf_path = sys.argv[1], sys.argv[2]
    render_proposal_markdown_to_pdf(source_markdown_path, output_pdf_path)
    print(f"Wrote {output_pdf_path}")
