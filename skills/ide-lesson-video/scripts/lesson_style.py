"""Pillow adaptation of the user's Claude HTML visual reference."""
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT = 1920, 1080
CODE_FONT_PATH = os.environ.get('IDE_VIDEO_CODE_FONT')
UI_FONT_PATH = os.environ.get('IDE_VIDEO_UI_FONT')
if not CODE_FONT_PATH or not UI_FONT_PATH:
    raise EnvironmentError('Set IDE_VIDEO_CODE_FONT and IDE_VIDEO_UI_FONT to valid font paths; the renderer does not auto-fallback.')
for candidate in (CODE_FONT_PATH, UI_FONT_PATH):
    if not Path(candidate).is_file():
        raise FileNotFoundError('Set IDE_VIDEO_CODE_FONT and IDE_VIDEO_UI_FONT to valid font paths; missing: ' + candidate)
DISPLAY_FILE, LESSON_LABEL, VOICE_LABEL, STAGE_COUNT = 'vehicle.py', 'Python 列表', '阿里百炼 Ethan', 3
FONT = ImageFont.truetype(CODE_FONT_PATH, 34)
GUTTER_FONT = ImageFont.truetype(CODE_FONT_PATH, 30)
TERMINAL_FONT = ImageFont.truetype(CODE_FONT_PATH, 29)
FILE_FONT = ImageFont.truetype(CODE_FONT_PATH, 26)
STATUS_FONT = ImageFont.truetype(CODE_FONT_PATH, 23)
UI_FONT = ImageFont.truetype(UI_FONT_PATH, 30)
SMALL_UI_FONT = ImageFont.truetype(UI_FONT_PATH, 24)
FOOTER_FONT = ImageFont.truetype(UI_FONT_PATH, 21)


def oklch(lightness, chroma, hue):
    # Convert the reference's Oklch tokens into displayable sRGB pixels.
    angle = math.radians(hue)
    a, b = chroma * math.cos(angle), chroma * math.sin(angle)
    l = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3
    linear = (4.0767416621*l - 3.3077115913*m + 0.2309699292*s,
              -1.2684380046*l + 2.6097574011*m - 0.3413193965*s,
              -0.0041960863*l - 0.7034186147*m + 1.7076147010*s)
    def channel(value):
        value = min(1, max(0, value))
        encoded = 12.92 * value if value <= 0.0031308 else 1.055 * value ** (1/2.4) - 0.055
        return round(encoded * 255)
    return tuple(channel(value) for value in linear)


COLORS = {
    'page': oklch(.12, .012, 240),
    'editor': oklch(.17, .015, 240),
    'gutter': oklch(.15, .013, 240),
    'terminal': oklch(.10, .008, 240),
    'terminal_top': oklch(.11, .009, 240),
    'border_sub': oklch(.24, .018, 240),
    'border_div': oklch(.20, .014, 240),
    'code': oklch(.85, .008, 240),
    'muted': oklch(.44, .012, 240),
    'output': oklch(.78, .006, 240),
    'accent': oklch(.72, .17, 195),
    'accent_dim': oklch(.56, .13, 195),
    'string': oklch(.73, .16, 145),
    'operator': oklch(.66, .09, 260),
    'function': oklch(.73, .14, 260),
    'dot_red': oklch(.55, .18, 25),
    'dot_yellow': oklch(.70, .17, 80),
    'dot_green': oklch(.60, .18, 145),
    'active': oklch(.195, .017, 240),
    'callout_red': (231, 58, 72),
    'callout_fill_start': oklch(.38, .08, 195),
    'callout_fill': oklch(.18, .035, 195),
}
EDITOR_RECT = (180, 140, 1740, 652)
RUN_BUTTON_RECT = (1586, 156, 1712, 199)
TERMINAL_RECT = (180, 672, 1740, 962)
TERMINAL_BODY_RECT = (182, 738, 1738, 960)
CODE_X, CODE_Y, LINE_HEIGHT = 308, 248, 50
CODE_BASELINE = 2 - FONT.getbbox('Ag', anchor='ls')[1]
CARET_HEIGHT, CARET_WIDTH = 37, 3
CARET_COLOR = COLORS['accent']
TERMINAL_X, TERMINAL_COMMAND_Y = 228, 766
TERMINAL_OUTPUT_Y, TERMINAL_LINE_HEIGHT = 814, 42


def rounded_panel(canvas, bounds, background, topbar, gutter=False):
    x0, y0, x1, y1 = bounds
    w, h = x1-x0, y1-y0
    panel = Image.new('RGB', (w,h), background)
    d = ImageDraw.Draw(panel)
    bar_height = 74 if gutter else 64
    d.rectangle((0,0,w,bar_height), fill=topbar)
    d.line((0,bar_height,w,bar_height), fill=COLORS['border_div'], width=2)
    if gutter:
        d.rectangle((0,bar_height+2,90,h), fill=COLORS['gutter'])
        d.line((90,bar_height+2,90,h), fill=COLORS['border_div'], width=2)
    mask = Image.new('L', (w,h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1), radius=24, fill=255)
    canvas.paste(panel, (x0,y0), mask)
    ImageDraw.Draw(canvas).rounded_rectangle((x0,y0,x1-1,y1-1), radius=24,
                                            outline=COLORS['border_div'], width=2)


def base_frame():
    im = Image.new('RGB', (WIDTH,HEIGHT), COLORS['page'])
    rounded_panel(im, EDITOR_RECT, COLORS['editor'], COLORS['gutter'], gutter=True)
    rounded_panel(im, TERMINAL_RECT, COLORS['terminal'], COLORS['terminal_top'])
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((180,80,185,117), radius=2, fill=COLORS['accent'])
    # File badge and run control mirror the HTML; neither changes layout.
    d.rounded_rectangle((208,160,round(242+FILE_FONT.getlength(DISPLAY_FILE)),196), radius=6, fill=COLORS['editor'],
                        outline=COLORS['border_sub'], width=1)
    d.text((225,164), DISPLAY_FILE, font=FILE_FONT, fill=COLORS['muted'], anchor='lt')
    d.rounded_rectangle(RUN_BUTTON_RECT, radius=7, fill=COLORS['accent'])
    d.polygon([(1605,169),(1605,185),(1617,177)], fill=COLORS['page'])
    d.text((1631,161), '运行', font=SMALL_UI_FONT, fill=COLORS['page'], anchor='lt')
    for n, key in enumerate(('dot_red','dot_yellow','dot_green')):
        x = 208 + n * 29
        d.ellipse((x,695,x+15,710), fill=COLORS[key])
    d.text((307,689), '终端输出', font=SMALL_UI_FONT, fill=COLORS['muted'], anchor='lt')
    d.text((180,991), f'{VOICE_LABEL} · {LESSON_LABEL}', font=FOOTER_FONT,
           fill=COLORS['muted'], anchor='lt')
    return im


BASE = base_frame()


def configure(display_file='vehicle.py', lesson_label='Python 列表', voice_label='阿里百炼 Ethan', stage_count=3):
    global DISPLAY_FILE, LESSON_LABEL, VOICE_LABEL, STAGE_COUNT, BASE
    DISPLAY_FILE, LESSON_LABEL, VOICE_LABEL, STAGE_COUNT = display_file, lesson_label, voice_label, stage_count
    assert FILE_FONT.getlength(DISPLAY_FILE) < 900, 'Display file name too long'
    BASE = base_frame()



def syntax_spans(line):
    # A small lexer that also colors unfinished strings while they are typed.
    index = 0
    while index < len(line):
        start = index
        char = line[index]
        color = COLORS['code']
        if char in ('\"', "'"):
            quote = char
            index += 1
            while index < len(line):
                if line[index] == '\\':
                    index = min(len(line), index+2)
                elif line[index] == quote:
                    index += 1
                    break
                else:
                    index += 1
            color = COLORS['string']
        elif char.isalpha() or char == '_':
            index += 1
            while index < len(line) and (line[index].isalnum() or line[index] == '_'):
                index += 1
            if line[start:index] == 'print':
                color = COLORS['function']
        elif char in '=+':
            index += 1
            while index < len(line) and line[index] in '=+':
                index += 1
            color = COLORS['operator']
        else:
            index += 1
        yield start, line[start:index], color


def caret_position(state):
    line = state['lines'][state['row']]
    return (round(CODE_X + FONT.getlength(line[:state['col']])),
            CODE_Y + state['row'] * LINE_HEIGHT)


def _wrap_annotation(text, max_chars=18):
    import textwrap
    return textwrap.wrap(str(text), width=max_chars, break_long_words=True,
                         break_on_hyphens=False) or ['']


def _mix_color(start, end, progress):
    progress = max(0.0, min(1.0, progress))
    return tuple(round(a + (b - a) * progress) for a, b in zip(start, end))


def _ease_in(progress):
    """Approximate Claude's cubic-bezier(.22,.61,.36,1) entrance curve."""
    progress = max(0.0, min(1.0, progress))
    return 1.0 - (1.0 - progress) ** 3


def _ease_out(progress):
    """Approximate Claude's cubic-bezier(.55,.06,.68,.19) exit curve."""
    progress = max(0.0, min(1.0, progress))
    return progress ** 1.7


def _draw_annotations(canvas, stage_index, state, stages, frame=None):
    """Draw close-to-code bubbles and red ellipses declared by the lesson."""
    if stage_index >= len(stages):
        return
    annotations = stages[stage_index].get('annotations', [])
    if not annotations:
        return
    stage_info = stages[stage_index]
    circle_frame = stage_info.get('circle_frame', stage_info.get('typing_end_frame', -1))
    bubble_frame = stage_info.get('bubble_frame', circle_frame + 3)
    bubble_end_frame = stage_info.get('bubble_end_frame', bubble_frame + 6)
    bubble_exit_frame = stage_info.get('bubble_exit_frame', 10**9)
    bubble_exit_end_frame = stage_info.get('bubble_exit_end_frame', bubble_exit_frame + 36)
    if frame is not None and frame < circle_frame:
        return
    d = ImageDraw.Draw(canvas)
    bubble_x, bubble_right = 1110, 1715
    occupied = []
    for annotation in annotations:
        highlight = annotation.get('highlight')
        row = int(annotation.get('row', highlight.get('row', 0) if isinstance(highlight, dict) else 0))
        if row >= len(state['lines']):
            continue
        line = state['lines'][row]
        target_y0 = CODE_Y + row * LINE_HEIGHT - 11
        target_y1 = target_y0 + 47
        # A bubble is independent from emphasis.  Draw the red ellipse only
        # when the lesson explicitly supplies a non-empty highlight range.
        if highlight:
            start_col = max(0, min(int(highlight.get('start_col', 0)), len(line)))
            end_col = max(start_col + 1, min(int(highlight.get('end_col', len(line))), len(line)))
            target_x0 = round(CODE_X + FONT.getlength(line[:start_col]) - 14)
            target_x1 = round(CODE_X + FONT.getlength(line[:end_col]) + 14)
            d.ellipse((target_x0, target_y0, target_x1, target_y1),
                      outline=COLORS['callout_red'], width=4)

        if frame is not None and frame < bubble_frame:
            continue
        bubble_progress = 1.0 if frame is None else min(1.0, max(0.0, (frame - bubble_frame) / max(1, bubble_end_frame - bubble_frame)))
        eased = _ease_in(bubble_progress)
        exiting = frame is not None and frame >= bubble_exit_frame
        exit_progress = 0.0 if not exiting else min(1.0, max(0.0, (frame - bubble_exit_frame) / max(1, bubble_exit_end_frame - bubble_exit_frame)))
        exit_eased = _ease_out(exit_progress)
        bubble_alpha = eased * (1.0 - exit_eased)
        bubble_fill = _mix_color(COLORS['callout_fill_start'], COLORS['callout_fill'], bubble_progress)
        lines = _wrap_annotation(annotation.get('text', ''))
        bubble_h = 22 + len(lines) * 32
        bubble_y = max(205, min(target_y0 - 5, EDITOR_RECT[3] - bubble_h - 20))
        while any(not (bubble_y + bubble_h + 8 < y0 or bubble_y - 8 > y1)
                  for y0, y1 in occupied):
            bubble_y += 12
        bubble_y = min(bubble_y, EDITOR_RECT[3] - bubble_h - 20)
        occupied.append((bubble_y, bubble_y + bubble_h))
        alpha = round(255 * bubble_alpha)
        # Draw the connector independently so it grows like a line being written.
        # The connector anchor belongs to the whole code line, independently of
        # the red ellipse's selected range.
        line_end_x = round(CODE_X + FONT.getlength(line))
        # Anchor the tail at the actual end of the referenced code line.  The
        # highlight ellipse is an independent emphasis layer and must not
        # move this point; the small terminal dot sits directly on the last
        # rendered character's right edge.
        source_x = line_end_x
        source_y = (target_y0 + target_y1) // 2
        connector_progress = eased
        if exiting:
            line_exit_progress = min(1.0, max(0.0, (exit_progress - .5) * 2.0))
            connector_progress *= 1.0 - _ease_out(line_exit_progress)
        connector_x = round(source_x + (bubble_x - 16 - source_x) * connector_progress)
        d.line([(source_x, source_y), (connector_x, source_y)],
               fill=COLORS['accent_dim'] + (round(255 * connector_progress),), width=2)
        if connector_progress > .5:
            d.line([(bubble_x - 16, source_y),
                    (bubble_x - 16, bubble_y + bubble_h // 2)],
                   fill=COLORS['accent_dim'] + (round(255 * connector_progress),), width=2)
        d.ellipse((source_x - 4, source_y - 4, source_x + 4, source_y + 4),
                  fill=COLORS['accent_dim'] + (round(255 * connector_progress),))

        # Claude-style entrance: opacity, translate, scale and blur resolve together.
        pad = 18
        patch = Image.new('RGBA', (bubble_right - bubble_x + pad * 2, bubble_h + pad * 2), (0, 0, 0, 0))
        pd = ImageDraw.Draw(patch)
        pd.rounded_rectangle((pad, pad, patch.width - pad, patch.height - pad),
                             radius=18, fill=bubble_fill + (alpha,),
                             outline=COLORS['accent_dim'] + (alpha,), width=2)
        text_y = pad + 11
        for line_text in lines:
            pd.text((patch.width // 2, text_y), line_text,
                    font=SMALL_UI_FONT, fill=COLORS['accent'] + (alpha,), anchor='ma')
            text_y += 32
        entrance_blur = 2.0 * (1.0 - eased)
        exit_blur = 2.0 * exit_eased
        if entrance_blur or exit_blur:
            patch = patch.filter(ImageFilter.GaussianBlur(radius=max(entrance_blur, exit_blur)))
        scale = (.96 + .04 * eased) * (1.0 - .04 * exit_eased)
        if scale != 1:
            patch = patch.resize((round(patch.width * scale), round(patch.height * scale)), Image.Resampling.LANCZOS)
        paste_x = round(bubble_x - pad * scale - 8 * (1.0 - eased) - 8 * exit_eased)
        paste_y = round(bubble_y - pad * scale + (bubble_h + pad * 2 - patch.height) / 2)
        canvas.paste(patch, (paste_x, paste_y), patch)


def render_frame(stage, state, output_stage, caret_on, stages, frame=None):
    im = BASE.copy()
    d = ImageDraw.Draw(im)
    d.text((205,81), f'第 {stage+1} 步', font=UI_FONT, fill=COLORS['accent'], anchor='lt')
    d.text((1738,90), f'{stage+1:02d} / {STAGE_COUNT:02d}', font=STATUS_FONT,
           fill=COLORS['muted'], anchor='rt')
    active_y = CODE_Y + state['row'] * LINE_HEIGHT
    d.rectangle((272,active_y-6,1736,active_y+41), fill=COLORS['active'])
    for n, line in enumerate(state['lines']):
        baseline = CODE_Y + n * LINE_HEIGHT + CODE_BASELINE
        number_color = COLORS['accent_dim'] if n == state['row'] else COLORS['muted']
        d.text((249,baseline), str(n+1), font=GUTTER_FONT, fill=number_color, anchor='rs')
        for start, text, color in syntax_spans(line):
            # Keep the same font and full-prefix advance for text and caret.
            x = CODE_X + FONT.getlength(line[:start])
            d.text((x,baseline), text, font=FONT, fill=color, anchor='ls')
        assert CODE_X + FONT.getlength(line) < EDITOR_RECT[2]-24
    x,y = caret_position(state)
    assert CODE_X <= x < EDITOR_RECT[2]-24 and y+CARET_HEIGHT < EDITOR_RECT[3]-16
    _draw_annotations(im, stage, state, stages, frame=frame)
    if caret_on:
        d.rectangle((x,y,x+CARET_WIDTH-1,y+CARET_HEIGHT-1), fill=CARET_COLOR)
    if output_stage >= 0:
        d.text((TERMINAL_X,TERMINAL_COMMAND_Y), '> ', font=TERMINAL_FONT,
               fill=COLORS['accent_dim'], anchor='lt')
        d.text((TERMINAL_X+TERMINAL_FONT.getlength('> '),TERMINAL_COMMAND_Y),
               f'python3 {DISPLAY_FILE}', font=TERMINAL_FONT, fill=COLORS['accent'], anchor='lt')
        for n,line in enumerate(stages[output_stage]['output']):
            assert TERMINAL_X+TERMINAL_FONT.getlength(line) < TERMINAL_RECT[2]-30
            d.text((TERMINAL_X,TERMINAL_OUTPUT_Y+n*TERMINAL_LINE_HEIGHT), line,
                   font=TERMINAL_FONT, fill=COLORS['output'], anchor='lt')
    d.text((1738,991), f'Ln {state["row"]+1}, Col {state["col"]+1}',
           font=STATUS_FONT, fill=COLORS['muted'], anchor='rt')
    return im

