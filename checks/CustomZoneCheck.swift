// Run: swiftc Rectangle/Snapping/CustomZone.swift checks/CustomZoneCheck.swift -o /tmp/rectangle-zone-check && /tmp/rectangle-zone-check
import Foundation
import CoreGraphics

@main
enum CustomZoneCheck {
    static func main() throws {
        let workArea = CGRect(x: -1440, y: -800, width: 1200, height: 900)
        let zone = CustomZone(name: "Top", x: 0.25, y: 0, width: 0.5, height: 0.5)
        assert(zone.frame(in: workArea) == CGRect(x: -1140, y: -350, width: 600, height: 450))
        assert(CustomZone(y: 0.5, height: 0.5).frame(in: workArea)?.minY == workArea.minY)
        assert(zone.frame(in: CGRect(x: 10, y: 20, width: 1, height: 1))?.width == 0.5)
        assert(CustomZone(x: -0.1).frame(in: workArea) == nil)
        assert(CustomZone(x: 0.75, width: 0.5).frame(in: workArea) == nil)
        assert(CustomZone(width: 0).frame(in: workArea) == nil)
        assert(CustomZone(y: .nan).frame(in: workArea) == nil)
        assert(zone.frame(in: .null) == nil && zone.frame(in: .zero) == nil)
        let clamped = CustomZone(id: zone.id, name: zone.name, x: 2, y: -1, width: 2, height: .nan).clamped()
        assert(clamped.isValid && clamped.id == zone.id && clamped.name == zone.name)
        let restored = try JSONDecoder().decode(CustomZone.self, from: JSONEncoder().encode(zone))
        assert(restored == zone)
        print("Custom zone geometry check passed")
    }
}
