#!/usr/bin/env python3
"""Set Finder artwork and layout on a mounted, writable installer volume.

Requires Python 3.10+. Packaging tools: pip install --target /private/tmp/rectangle-dmg-tools
    ds-store==1.3.3 mac-alias==2.2.3
Usage: python3 scripts/prepare-dmg.py <mounted-volume-root>
"""

from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, "/private/tmp/rectangle-dmg-tools")
from ds_store import DSStore
from mac_alias import Alias

if len(sys.argv) != 2 or not Path(sys.argv[1]).is_dir():
    raise SystemExit("Usage: prepare-dmg.py <mounted-volume-root>")
volume = Path(sys.argv[1]).resolve()
background = volume / ".background" / "background.png"
background.parent.mkdir(exist_ok=True)

drawing = r'''import AppKit

let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: 680, pixelsHigh: 460,
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
    colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
let bounds = NSRect(x: 0, y: 0, width: 680, height: 460)
NSGradient(starting: NSColor(calibratedWhite: 0.995, alpha: 1),
           ending: NSColor(calibratedRed: 0.94, green: 0.96, blue: 0.99, alpha: 1))!
    .draw(in: bounds, angle: -90)
NSColor.systemBlue.setFill()
NSBezierPath(roundedRect: NSRect(x: 44, y: 402, width: 34, height: 5), xRadius: 2.5, yRadius: 2.5).fill()
func text(_ value: String, x: CGFloat, y: CGFloat, size: CGFloat, weight: NSFont.Weight, color: NSColor) {
    NSAttributedString(string: value, attributes: [.font: NSFont.systemFont(ofSize: size, weight: weight),
        .foregroundColor: color]).draw(at: NSPoint(x: x, y: y))
}
text("Rectangle Custom Zones", x: 44, y: 357, size: 28, weight: .semibold,
     color: NSColor(calibratedWhite: 0.14, alpha: 1))
text("Drag the app to Applications, then open it from there.", x: 44, y: 326, size: 14, weight: .regular,
     color: NSColor(calibratedWhite: 0.42, alpha: 1))
NSColor(calibratedWhite: 0.56, alpha: 1).setStroke()
let arrow = NSBezierPath()
arrow.lineWidth = 3
arrow.lineCapStyle = .round
arrow.lineJoinStyle = .round
arrow.move(to: NSPoint(x: 292, y: 240))
arrow.line(to: NSPoint(x: 388, y: 240))
arrow.move(to: NSPoint(x: 375, y: 252))
arrow.line(to: NSPoint(x: 388, y: 240))
arrow.line(to: NSPoint(x: 375, y: 228))
arrow.stroke()
NSColor(calibratedWhite: 0.87, alpha: 1).setStroke()
let divider = NSBezierPath()
divider.move(to: NSPoint(x: 44, y: 148))
divider.line(to: NSPoint(x: 636, y: 148))
divider.stroke()
NSGraphicsContext.restoreGraphicsState()
try bitmap.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
'''

scratch_root = Path("/private/tmp/rectangle-dmg-layout")
scratch_root.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix="drawing-", dir=scratch_root) as scratch:
    source = Path(scratch) / "background.swift"
    source.write_text(drawing)
    try:
        subprocess.run(["/usr/bin/xcrun", "swift", "-module-cache-path", str(Path(scratch) / "cache"),
                        str(source), str(background)], check=True)
    finally:
        kib = int(subprocess.check_output(["/usr/bin/du", "-sk", scratch], text=True).split()[0])
        print(f"Temporary drawing source/cache: {kib} KiB; removing.")

window = dict(WindowBounds="{{180, 120}, {680, 460}}", ShowToolbar=False, ShowSidebar=False,
              ContainerShowSidebar=False, ShowStatusBar=False, ShowPathbar=False,
              ShowTabView=False, PreviewPaneVisibility=False, SidebarWidth=0)
icons = dict(viewOptionsVersion=1, backgroundType=2, backgroundImageAlias=Alias.for_file(str(background)).to_bytes(),
             iconSize=88.0, textSize=12.0, labelOnBottom=True, arrangeBy="none",
             gridOffsetX=0.0, gridOffsetY=0.0, gridSpacing=100.0, showIconPreview=True,
             showItemInfo=False, scrollPositionX=0.0, scrollPositionY=0.0)
positions = {"Rectangle Custom Zones.app": (170, 220), "Applications": (510, 220),
             "Read Me.rtf": (250, 370), "Licenses": (430, 370)}
with DSStore.open(str(volume / ".DS_Store"), "w+") as store:
    store["."]["vSrn"] = ("long", 1)
    store["."]["icvl"] = ("type", b"icnv")
    store["."]["bwsp"] = window
    store["."]["icvp"] = icons
    for name, position in positions.items():
        store[name]["Iloc"] = position
with DSStore.open(str(volume / ".DS_Store"), "r") as store:
    assert store["."]["bwsp"] == window and all(store[name]["Iloc"] == position for name, position in positions.items())
print(f"Finder layout ready: {volume}; background: {background}")
