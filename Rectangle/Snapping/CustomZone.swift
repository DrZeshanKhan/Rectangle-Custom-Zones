import Foundation
import CoreGraphics

struct CustomZone: Codable, Equatable, Identifiable {
    var id = UUID()
    var name = "Zone"
    // Normalized coordinates measured from the work area's top-left corner.
    var x = 0.0
    var y = 0.0
    var width = 0.5
    var height = 1.0

    var isValid: Bool {
        [x, y, width, height].allSatisfy(\.isFinite)
            && x >= 0 && y >= 0 && width > 0 && height > 0
            && x + width <= 1 && y + height <= 1
    }

    func frame(in workArea: CGRect) -> CGRect? {
        guard isValid, workArea.size.width > 0, workArea.size.height > 0,
              [workArea.minX, workArea.minY, workArea.maxX, workArea.maxY,
               workArea.width, workArea.height].allSatisfy(\.isFinite) else { return nil }
        return CGRect(x: workArea.minX + CGFloat(x) * workArea.width,
                      y: workArea.maxY - CGFloat(y + height) * workArea.height,
                      width: CGFloat(width) * workArea.width,
                      height: CGFloat(height) * workArea.height)
    }

    func clamped() -> CustomZone {
        var zone = self
        zone.width = width.isFinite ? min(1, max(0.01, width)) : 0.5
        zone.height = height.isFinite ? min(1, max(0.01, height)) : 1
        zone.x = x.isFinite ? min(1 - zone.width, max(0, x)) : 0
        zone.y = y.isFinite ? min(1 - zone.height, max(0, y)) : 0
        return zone
    }
}
