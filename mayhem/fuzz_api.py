#! /usr/bin/env python3
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=["webcolors"]):
    import webcolors

def simplify_hex(hex):
    hex = hex.strip()
    if hex.startswith("#"):
        hex = hex[1:]
    if len(hex) == 3:
        hex = "".join(x * 2 for x in hex)
    return hex.lower()

value_matchers = ['HTML5', 'valid hexadecimal', 'css3']
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    test = fdp.ConsumeIntInRange(0, 4)
    orig = fdp.ConsumeRemainingString()
    try:
        if test == 0:
            name = webcolors.hex_to_name(orig)
            denamed = webcolors.name_to_hex(name)
            if simplify_hex(orig) != simplify_hex(denamed):
                raise AssertionError("Mismatch")
        elif test == 1:
            webcolors.html5_parse_legacy_color(orig)
        elif test == 2:
            color = webcolors.html5_parse_simple_color(orig)
            webcolors.html5_serialize_simple_color(color)
        elif test == 3:
            rgb = webcolors.hex_to_rgb(orig)
            dergb = webcolors.rgb_to_hex(rgb)
            if simplify_hex(orig) != simplify_hex(dergb):
                raise AssertionError("Mismatch")
        elif test == 4:
            rgb_p = webcolors.hex_to_rgb_percent(orig)
            dergb_p = webcolors.rgb_percent_to_hex(rgb_p)
            if simplify_hex(orig) != simplify_hex(dergb_p):
                raise AssertionError("Mismatch")
    except ValueError as e:
        if any(x in str(e) for x in value_matchers):
            return -1
        raise e




def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
