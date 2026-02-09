import random
import time

from rpi_ws281x import Color

from env import HEIGHT, WIDTH, strip


# --- Helper: 2D → 1D (zigzag mapping) ---
def convert_2d_to_1d(frame_2d):
    leds = []
    for y in range(HEIGHT):
        if y % 2 == 0:  # even row (left→right)
            for x in range(WIDTH):
                leds.append(frame_2d[y][x])
        else:  # odd row (right→left)
            for x in reversed(range(WIDTH)):
                leds.append(frame_2d[y][x])
    return leds

# --- Matrix Rain Effect ---
def matrix_rain(strip=strip, frames=250, delay=0.05):
    rain = [random.randint(0, HEIGHT - 1) for _ in range(WIDTH)]
    rwid = [random.randint(2, 5) for _ in range(WIDTH)]

    for _ in range(frames):
        # Start with black frame
        frame = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]

        for x in range(WIDTH):
            y = rain[x]

            # Head of drop (bright green)
            if 0 <= y < HEIGHT:
                frame[y][x] = (0, 255, 0)

            # Trail
            for i in range(1, rwid[x]):
                if y - i >= 0:
                    g = max(0, 255 // ((i + 2) * (i + 2)))
                    frame[y - i][x] = (0, g, 0)

            # Update position
            rain[x] += 1
            if rain[x] >= HEIGHT:
                rain[x] = 0
                rwid[x] = random.randint(2, 5)

        # Convert 2D → 1D
        led_data = convert_2d_to_1d(frame)

        # Write to LED strip
        for i, (r, g, b) in enumerate(led_data):
            strip.setPixelColor(i, Color(g, r, b))
        strip.show()

        time.sleep(delay)
def xy_to_index(x, y):
    """Map 2D XY -> linear index (zigzag wiring assumed)."""
    if y % 2 == 0:  # even row → left to right
        return y * WIDTH + x
    else:           # odd row → right to left
        return y * WIDTH + (WIDTH - 1 - x)

def fill_square(matrix, pos_x, pos_y, color):
    """Draw a 5x5 block into matrix (clip inside bounds)."""
    for dy in range(5):
        for dx in range(5):
            px = pos_x + dx
            py = pos_y + dy
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                matrix[py][px] = color

def clear_matrix(matrix):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            matrix[y][x] = (0, 0, 0)

def matrix_to_strip(matrix, strip):
    """Push 2D matrix → rpi_ws281x strip."""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = matrix[y][x]
            strip.setPixelColor(xy_to_index(x, y), Color(r, g, b))
    strip.show()

def dvd5px(strip=strip):
    # Start with black frame
    frame = [[[0, 0, 0] for _ in range(WIDTH)] for _ in range(HEIGHT)]

    new_width = WIDTH - 4
    new_height = HEIGHT - 4
    ud, lr = 1, 1
    pos_x = random.randint(0, new_width - 1)
    pos_y = random.randint(0, new_height - 1)
    prev_x, prev_y = pos_x, pos_y

    for t in range(200):  # run for 200 steps
        prev_x, prev_y = pos_x, pos_y

        # Move X
        if lr == 1:
            if pos_x < new_width - 1:
                pos_x += 1
            else:
                pos_x -= 1
                lr = -1
        else:
            if pos_x > 0:
                pos_x -= 1
            else:
                pos_x += 1
                lr = 1

        # Move Y
        if ud == 1:
            if pos_y < new_height - 1:
                pos_y += 1
            else:
                pos_y -= 1
                ud = -1
        else:
            if pos_y > 0:
                pos_y -= 1
            else:
                pos_y += 1
                ud = 1

        # Erase previous square
        fill_square(frame, prev_x, prev_y, [0, 0, 0])
        # Draw new square with changing color
        fill_square(frame, pos_x, pos_y, 
                    [int(t * 5 % 255), 
                     int((255 - (t * 3 % 255))), 
                     int(200)])

        # Convert to 1D + show
        leds = convert_2d_to_1d(frame)
        for i, c in enumerate(leds):
            strip.setPixelColor(i, Color(c[0], c[1], c[2]))
        strip.show()

        time.sleep(0.05)

def spiral(strip=strip, LED_WIDTH=WIDTH, LED_HEIGHT=HEIGHT, delay_ms=5):
    # Create a 2D buffer for the LEDs
    frame = [[(0, 0, 0) for _ in range(LED_WIDTH)] for _ in range(LED_HEIGHT)]

    left, right, top, bottom = 0, LED_WIDTH - 1, 0, LED_HEIGHT - 1
    hue_max = LED_WIDTH + LED_HEIGHT  # used for mapping hue

    while left <= right and top <= bottom:
        # Top row (left → right)
        for x in range(left, right + 1):
            hue = int(((x + top) / hue_max) * 255) % 255
            frame[top][x] = hsv_to_rgb(hue, 255,255)
            leds = convert_2d_to_1d(frame)
            for i, c in enumerate(leds):
                strip.setPixelColor(i, Color(*c))
            strip.show()
            time.sleep(delay_ms / 1000.0)
        top += 1

        # Right column (top → bottom)
        for y in range(top, bottom + 1):
            hue = int(((right + y) / hue_max) * 255) % 255
            frame[y][right] = hsv_to_rgb(hue, 255, 255)
            leds = convert_2d_to_1d(frame)
            for i, c in enumerate(leds):
                strip.setPixelColor(i, Color(*c))
            strip.show()
            time.sleep(delay_ms / 1000.0)
        right -= 1

        # Bottom row (right → left)
        if top <= bottom:
            for x in range(right, left - 1, -1):
                hue = int(((bottom + x) / hue_max) * 255) % 255
                frame[bottom][x] = hsv_to_rgb(hue, 255, 255)
                leds = convert_2d_to_1d(frame)
                for i, c in enumerate(leds):
                    strip.setPixelColor(i, Color(*c))
                strip.show()
                time.sleep(delay_ms / 1000.0)
            bottom -= 1

        # Left column (bottom → top)
        if left <= right:
            for y in range(bottom, top - 1, -1):
                hue = int(((left + y) / hue_max) * 255) % 255
                frame[y][left] = hsv_to_rgb(hue, 255, 255)
                leds = convert_2d_to_1d(frame)
                for i, c in enumerate(leds):
                    strip.setPixelColor(i, Color(*c))
                strip.show()
                time.sleep(delay_ms / 1000.0)
            left += 1

    # Fade out effect (like your FastLED version)
    for b in range(255, -1, -(255 // 20)):
        leds = convert_2d_to_1d(frame)
        for i, c in enumerate(leds):
            r = int(c[0] * b / 255)
            g = int(c[1] * b / 255)
            h = int(c[2] * b / 255)
            strip.setPixelColor(i, Color(r, g, h))
        strip.show()

    # Clear and reset brightness
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def hsv_to_rgb(h, s, v):
    import colorsys

    # Map h,s,v from 0-255 → 0-1
    h = (h % 256) / 255.0
    s = s / 255.0
    v = v / 255.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

if __name__ == "__main__":
    print("Starting Matrix Rain... Press Ctrl+C to stop.")
    try:
        while True:
            matrix_rain()
            dvd5px()
            spiral()
    except KeyboardInterrupt:
        # Clear LEDs on exit
        for i in range(HEIGHT * WIDTH):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
