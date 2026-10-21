# PC simulator of the fx-CG100 "casioplot" module - for testing on a laptop.
# Needs: sudo apt install python3-tk python3-pil
# Keys: arrows = arrows, Enter = EXE, Space or O = OK, number keys = numbers, Esc = AC (quit)
import tkinter as tk, time, sys, os
from PIL import Image, ImageDraw, ImageFont

W, H, SCALE = 384, 192, 3
KEY_DELAY = float(os.environ.get("SIM_KEY_DELAY", "0.03"))  # raise to slow the game down

KEYMAP = {"Up": 14, "Down": 34, "Left": 23, "Right": 25, "Return": 95, "KP_Enter": 95,
          "space": 24, "o": 24, "1": 81, "2": 82, "3": 83, "4": 71, "5": 72, "6": 73,
          "7": 61, "8": 62, "9": 63, "0": 91}

_img = Image.new("RGB", (W, H), (255, 255, 255))
_draw = ImageDraw.Draw(_img)
_draw.fontmode = "1"  # sharp pixel text like the calculator (no smoothing leftovers)
_held = []

def _font(px):
    for name in ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except Exception:
            pass
    return ImageFont.load_default()

_FONTS = {"small": _font(10), "medium": _font(13), "large": _font(19)}

_root = tk.Tk()
_root.title("fx-CG100 simulator - Python (casioplot)")
_label = tk.Label(_root, bg="black")
_label.pack()
_photo = None

def _down(e):
    if e.keysym == "Escape":
        _root.destroy()
        sys.exit("AC pressed - script stopped")
    k = KEYMAP.get(e.keysym)
    if k and k not in _held:
        _held.append(k)

def _up(e):
    k = KEYMAP.get(e.keysym)
    if k in _held:
        _held.remove(k)

_root.bind("<KeyPress>", _down)
_root.bind("<KeyRelease>", _up)
_root.protocol("WM_DELETE_WINDOW", lambda: (_root.destroy(), sys.exit(0)))

def _pump():
    try:
        _root.update()
    except tk.TclError:
        sys.exit(0)

def _ok(x, y):
    return isinstance(x, int) and isinstance(y, int) and 0 <= x <= 383 and 0 <= y <= 191

def _col(c):
    return tuple(int(v) for v in c)

def show_screen():
    global _photo
    big = _img.resize((W * SCALE, H * SCALE), Image.NEAREST)
    data = b"P6 %d %d 255\n" % big.size + big.tobytes()
    _photo = tk.PhotoImage(data=data, format="PPM")
    _label.configure(image=_photo)
    _pump()

def clear_screen():
    _draw.rectangle((0, 0, W - 1, H - 1), fill=(255, 255, 255))

def set_pixel(x, y, color=(0, 0, 0)):
    if _ok(x, y):
        _img.putpixel((x, y), _col(color))

def get_pixel(x, y):
    if _ok(x, y):
        return _img.getpixel((x, y))
    return None

def draw_string(x, y, s, color=(0, 0, 0), size="medium"):
    if _ok(x, y):
        _draw.text((x, y), str(s), fill=_col(color), font=_FONTS.get(size, _FONTS["medium"]))

def getkey():
    _pump()
    time.sleep(KEY_DELAY)  # the real getkey() is slow; this keeps game speed realistic
    _pump()
    return _held[-1] if _held else 0

clear_screen()
show_screen()
