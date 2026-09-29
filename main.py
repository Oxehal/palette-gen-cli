import argparse
import colorsys
import sys


def hex_to_rgb(hex_code: str) -> tuple[float, float, float]:
    clean_hex = hex_code.lstrip("#")
    if len(clean_hex) != 6:
        raise ValueError("Invalid HEX format. Use 6 characters, e.g., #6366F1")
    r, g, b = (int(clean_hex[i : i + 2], 16) for i in (0, 2, 4))
    return r / 255.0, g / 255.0, b / 255.0


def rgb_to_hex(r: float, g: float, b: float) -> str:
    ir, ig, ib = (int(round(max(0.0, min(1.0, val)) * 255)) for val in (r, g, b))
    return f"#{ir:02X}{ig:02X}{ib:02X}"


def get_harmonies(hex_code: str) -> dict[str, list[str]]:
    r, g, b = hex_to_rgb(hex_code)
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    # Комплементарная (противоположный цвет)
    comp_h = (h + 0.5) % 1.0
    complementary = [
        rgb_to_hex(r, g, b),
        rgb_to_hex(*colorsys.hls_to_rgb(comp_h, l, s)),
    ]

    # Аналоговая (соседние оттенки +/- 30 градусов)
    analogous = [
        rgb_to_hex(*colorsys.hls_to_rgb((h - 30 / 360) % 1.0, l, s)),
        rgb_to_hex(r, g, b),
        rgb_to_hex(*colorsys.hls_to_rgb((h + 30 / 360) % 1.0, l, s)),
    ]

    # Триада (равноудаленные 120 градусов)
    triadic = [
        rgb_to_hex(r, g, b),
        rgb_to_hex(*colorsys.hls_to_rgb((h + 1 / 3) % 1.0, l, s)),
        rgb_to_hex(*colorsys.hls_to_rgb((h + 2 / 3) % 1.0, l, s)),
    ]

    # Монохромная (5 шагов яркости)
    lightness_steps = [0.92, 0.75, l, max(0.1, l * 0.6), max(0.05, l * 0.3)]
    monochromatic = [
        rgb_to_hex(*colorsys.hls_to_rgb(h, step_l, s)) for step_l in lightness_steps
    ]

    return {
        "complementary": complementary,
        "analogous": analogous,
        "triadic": triadic,
        "monochromatic": monochromatic,
    }


def export_css(base_hex: str, harmonies: dict[str, list[str]]) -> str:
    lines = [":root {", f"  --color-primary: {base_hex.upper()};"]
    for i, color in enumerate(harmonies["monochromatic"], start=1):
        lines.append(f"  --color-mono-{i * 100}: {color};")
    for i, color in enumerate(harmonies["analogous"], start=1):
        lines.append(f"  --color-analogous-{i}: {color};")
    for i, color in enumerate(harmonies["triadic"], start=1):
        lines.append(f"  --color-triadic-{i}: {color};")

    grad_c1 = harmonies["monochromatic"][1]
    grad_c2 = harmonies["complementary"][1]
    lines.append(
        f"  --gradient-accent: linear-gradient(135deg, {base_hex.upper()} 0%, {grad_c2} 100%);"
    )
    lines.append(
        f"  --gradient-soft: linear-gradient(180deg, {grad_c1} 0%, {base_hex.upper()} 100%);"
    )
    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Harmonious UI Palette & CSS Gradient Generator"
    )
    parser.add_argument(
        "hex",
        nargs="?",
        default="#6366F1",
        help="Base color in HEX format (default: #6366F1)",
    )
    parser.add_argument(
        "--css",
        action="store_true",
        help="Export palette as ready-to-use CSS custom properties",
    )

    args = parser.parse_args()

    try:
        harmonies = get_harmonies(args.hex)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    if args.css:
        print(export_css(args.hex, harmonies))
        return

    print(f"\n🎨 Base Color: {args.hex.upper()}\n" + "─" * 36)
    print("Complementary :", " → ".join(harmonies["complementary"]))
    print("Analogous     :", " → ".join(harmonies["analogous"]))
    print("Triadic       :", " → ".join(harmonies["triadic"]))
    print("Monochrome    :", " → ".join(harmonies["monochromatic"]))
    print(
        f"CSS Gradient  : linear-gradient(135deg, {args.hex.upper()}, {harmonies['complementary'][1]})"
    )
    print("─" * 36)
    print("Tip: Run with --css to get full CSS variables block.\n")


if __name__ == "__main__":
    main()
