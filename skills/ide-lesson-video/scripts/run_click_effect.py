"""An animated mouse click on Run, synchronized with terminal output."""
from PIL import Image, ImageDraw
from lesson_style import COLORS, RUN_BUTTON_RECT

APPROACH_SECONDS = .6
HOLD_SECONDS = .2
FADE_SECONDS = 1.2
END_SECONDS = HOLD_SECONDS + FADE_SECONDS
CLICK_TIP = (1677, 179)
SPRITE_TIP = (8, 8)


def smoothstep(value):
    value = min(1., max(0., value))
    return value * value * (3 - 2 * value)


def make_pointer():
    scale = 4
    im = Image.new('RGBA', (64 * scale, 78 * scale))
    d = ImageDraw.Draw(im)
    points = [(8, 8), (8, 55), (21, 43), (32, 65), (42, 60), (31, 38), (50, 38)]
    shadow = [((x + 2) * scale, (y + 3) * scale) for x, y in points]
    polygon = [(x * scale, y * scale) for x, y in points]
    d.polygon(shadow, fill=(0, 0, 0, 125))
    d.polygon(polygon, fill=(247, 251, 255, 255))
    d.line(polygon + [polygon[0]], fill=(6, 12, 18, 255), width=2 * scale, joint='curve')
    return im.resize((64, 78), Image.Resampling.LANCZOS)


POINTER = make_pointer()


def phase_frame(frame_number, result_frame, fps=30):
    relative = frame_number - result_frame
    if -round(APPROACH_SECONDS * fps) <= relative < round(END_SECONDS * fps):
        return relative
    return None


def cursor_state(frame_number, result_frame, fps=30):
    phase = phase_frame(frame_number, result_frame, fps)
    if phase is None:
        return None
    t = phase / fps
    travel = smoothstep((t + APPROACH_SECONDS) / .5)
    tip_x = CLICK_TIP[0] + 88 * (1 - travel)
    tip_y = CLICK_TIP[1] + 102 * (1 - travel)
    if t < 0:
        opacity = smoothstep((t + APPROACH_SECONDS) / .16)
    else:
        opacity = 1 - smoothstep((t - HOLD_SECONDS) / FADE_SECONDS)
    pressed = 0 <= t < .16
    if pressed:
        tip_y += 1.5 * (1 - t / .16)
    return dict(t=t, tip_x=tip_x, tip_y=tip_y, opacity=opacity, pressed=pressed)


def apply_run_click(frame, frame_number, result_frame, fps=30):
    state = cursor_state(frame_number, result_frame, fps)
    if state is None or state['opacity'] <= 0:
        return frame
    t = state['t']
    layer = Image.new('RGBA', frame.size)
    d = ImageDraw.Draw(layer)
    if state['pressed']:
        d.rounded_rectangle(RUN_BUTTON_RECT, radius=7,
                            fill=(0, 0, 0, round(90 * (1 - t / .16))))
    if 0 <= t < .65:
        progress = t / .65
        radius = 10 + 38 * smoothstep(progress)
        x, y = CLICK_TIP
        d.ellipse((x-radius, y-radius, x+radius, y+radius),
                  outline=(*COLORS['accent'], round(220 * (1-progress))), width=3)
        if t < .18:
            d.ellipse((x-5, y-5, x+5, y+5),
                      fill=(224, 255, 255, round(165 * (1-t/.18))))
    pointer = POINTER.copy()
    pointer.putalpha(pointer.getchannel('A').point(lambda alpha: round(alpha * state['opacity'])))
    origin = (round(state['tip_x'] - SPRITE_TIP[0]), round(state['tip_y'] - SPRITE_TIP[1]))
    layer.alpha_composite(pointer, dest=origin)
    return Image.alpha_composite(frame.convert('RGBA'), layer).convert('RGB')

