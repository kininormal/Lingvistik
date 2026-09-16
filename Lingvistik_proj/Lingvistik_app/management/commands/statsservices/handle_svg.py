import re

def make_svg_responsive(svg: str) -> str:
    # grab the original dimensions from the <svg ...> tag
    w = re.search(r'<svg[^>]*\swidth="(\d+)', svg).group(1)
    h = re.search(r'<svg[^>]*\sheight="([\d.]+)', svg).group(1)

    # only touch the opening <svg ...> tag, not inner elements
    svg = re.sub(
        r'(<svg\b[^>]*)\swidth="\d+"\s+height="[\d.]+"([^>]*)',
        rf'\1 viewBox="0 0 {w} {h}" width="100%" height="auto"\2',
        svg, count=1
    )
    svg = svg.replace('style="max-width: none;', 'style="max-width: 80%;')
    return svg