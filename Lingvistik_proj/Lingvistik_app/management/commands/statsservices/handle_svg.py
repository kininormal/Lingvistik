import re


#Version 3
def make_svg_responsive(svg: str) -> str:

    if not svg:
        return svg

    # Find <svg ...>
    svg_match = re.search(r'<svg\b[^>]*>', svg)

    if not svg_match:
        print("No <svg> tag found")
        return svg

    opening_tag = svg_match.group(0)

    # Find width
    width_match = re.search(
        r'\bwidth="([\d.]+)',
        opening_tag
    )

    # Find height
    height_match = re.search(
        r'\bheight="([\d.]+)',
        opening_tag
    )

    if not width_match or not height_match:

        print("Could not find width/height")
        print("Opening SVG tag:")
        print(opening_tag)

        return svg

    w = width_match.group(1)
    h = height_match.group(1)

    # Replace original width/height
    new_tag = re.sub(
        r'\bwidth="[\d.]+"',
        f'width="100%"',
        opening_tag,
        count=1
    )

    new_tag = re.sub(
        r'\bheight="[\d.]+"',
        'height="auto"',
        new_tag,
        count=1
    )

    # Add viewBox
    new_tag = re.sub(
        r'<svg\b',
        f'<svg viewBox="0 0 {w} {h}"',
        new_tag,
        count=1
    )

    # Replace opening tag
    svg = (
        svg[:svg_match.start()]
        + new_tag
        + svg[svg_match.end():]
    )

    return svg
def prepare_svg(svg: str) -> str:

    if not svg:
        return svg

    svg_match = re.search(r'<svg\b[^>]*>', svg)

    if not svg_match:
        return svg

    opening_tag = svg_match.group(0)

    width_match = re.search(
        r'\bwidth="([\d.]+)',
        opening_tag
    )

    height_match = re.search(
        r'\bheight="([\d.]+)',
        opening_tag
    )

    if not width_match or not height_match:
        return svg

    w = width_match.group(1)
    h = height_match.group(1)

    # Add viewBox
    if 'viewBox=' not in opening_tag:

        new_tag = re.sub(
            r'<svg\b',
            f'<svg viewBox="0 0 {w} {h}"',
            opening_tag,
            count=1
        )

    else:
        new_tag = opening_tag

    # Keep natural SVG dimensions
    new_tag = re.sub(
        r'\bwidth="[\d.]+"',
        f'width="{w}"',
        new_tag,
        count=1
    )

    new_tag = re.sub(
        r'\bheight="[\d.]+"',
        f'height="{h}"',
        new_tag,
        count=1
    )

    svg = (
        svg[:svg_match.start()]
        + new_tag
        + svg[svg_match.end():]
    )

    return svg

#Version 2:
# def make_svg_responsive(svg: str) -> str:
#     # Hent original width/height fra <svg>
#     w = re.search(r'<svg[^>]*\swidth="(\d+)', svg).group(1)
#     h = re.search(r'<svg[^>]*\sheight="([\d.]+)', svg).group(1)

#     svg = re.sub(
#         r'(<svg\b[^>]*?)\swidth="\d+"\s+height="[\d.]+"([^>]*)',
#         rf'\1 viewBox="0 0 {w} {h}" width="{w}" height="{h}"\2',
#         svg,
#         count=1
#     )

#     return svg



#Version 1:

# def make_svg_responsive(svg: str) -> str:
#      # grab the original dimensions from the <svg ...> tag
#     w = re.search(r'<svg[^>]*\swidth="(\d+)', svg).group(1)
#     h = re.search(r'<svg[^>]*\sheight="([\d.]+)', svg).group(1)

#     # only touch the opening <svg ...> tag, not inner elements
#     svg = re.sub(
#         r'(<svg\b[^>]*)\swidth="\d+"\s+height="[\d.]+"([^>]*)',
#         rf'\1 viewBox="0 0 {w} {h}" width="100%" height="auto"\2',
#         svg, count=1
#     )
#     svg = svg.replace('style="max-width: none;', 'style="max-width: 100%;')
#     return svg