# Rectangle Custom Zones

A fork of [Rectangle](https://github.com/rxhanson/Rectangle) that adds editable rectangular snap zones and Shift-drag placement on macOS.

[Download the universal DMG](https://github.com/DrZeshanKhan/Rectangle-Custom-Zones/releases/download/v2.0.2-custom-zones/Rectangle-Custom-Zones-2.0.2-universal.dmg) · [Latest release](https://github.com/DrZeshanKhan/Rectangle-Custom-Zones/releases/latest)

## Install

Requires **macOS 14 or later**. The release contains both **Intel and Apple Silicon** architectures.

1. Open the DMG and drag **Rectangle Custom Zones.app** to **Applications**.
2. Quit other Rectangle instances, open the copied app from Applications, then eject the DMG.
3. When prompted, select **Open System Settings** and enable the app in **Privacy & Security > Accessibility**. The app needs this permission to move and resize windows. Its prompt may still use the upstream name, Rectangle.

The release is **ad hoc signed**, with **no Developer ID signature or Apple notarization**. If macOS blocks opening it, and you trust the download, try opening it once, then use **System Settings > Privacy & Security > Open Anyway**, if your Mac's policy allows that option. Follow [Apple's instructions for opening an unidentified or unnotarized app](https://support.apple.com/en-us/102445). Managed Macs may require administrator approval.

## Create and use a zone

1. Click Rectangle's menu bar icon, then **Settings > Snap Areas > Custom Zones > Add**.
2. Give the zone a name and enter percentages. For a left-half zone:

   | Field | Value |
   | --- | ---: |
   | Left | 0 |
   | Top | 0 |
   | Width | 50 |
   | Height | 100 |

3. Edits save automatically. Click a rectangle in the preview or use the zone picker to select it; **Delete** removes the selected zone.
4. Hold **Shift**, drag a window by its title bar into the zone, then release the mouse **while Shift is still held**.

Percentages scale to each display's usable area. Rectangle's existing gaps and app size restrictions still apply. The most recently added zone wins where zones overlap.

## What changed

- `CustomZone` stores validated, normalized geometry measured from the usable area's top-left corner.
- `Defaults.customZones` saves zones through Rectangle's existing JSON settings and configuration import/export.
- The existing Snap Areas settings page provides Add/Delete, name and percentage fields, and a clickable preview.
- Shift-drag target detection passes a custom rectangle through the existing window movement, gap, restore, and animation paths.
- The updater starts only when a valid feed is present. The distributed app removes the upstream Sparkle feed and disables automatic checks, preserving the fork when users update manually from this repository.

The fork's scope is editable rectangular targets and Shift-drag placement inspired by FancyZones.

## Build from source

Use full Xcode and Swift Package Manager. From this repository's root, resolve packages, then build the universal Release configuration:

```sh
xcodebuild -resolvePackageDependencies \
  -project Rectangle.xcodeproj -scheme Rectangle \
  -clonedSourcePackagesDirPath ../build/SourcePackages

xcodebuild -project Rectangle.xcodeproj -scheme Rectangle \
  -configuration Release -destination 'generic/platform=macOS' \
  -derivedDataPath ../build \
  -clonedSourcePackagesDirPath ../build/SourcePackages \
  -disableAutomaticPackageResolution \
  CODE_SIGN_STYLE=Manual CODE_SIGN_IDENTITY=- DEVELOPMENT_TEAM= \
  PRODUCT_BUNDLE_IDENTIFIER=com.knollsoft.Rectangle.CustomZonesDebug \
  MACOSX_DEPLOYMENT_TARGET=14.0 'ARCHS=arm64 x86_64' ONLY_ACTIVE_ARCH=NO \
  ASSETCATALOG_OTHER_FLAGS= EXCLUDED_SOURCE_FILE_NAMES=AppIcon.icon build
```

The output is `../build/Build/Products/Release/Rectangle.app`. Keep the project's product name unchanged when building.

The packaged app additionally renames the copied bundle, sets its display name, includes dependency licenses, and is signed after those changes. The source plist retains upstream update settings: **remove `SUFeedURL`, `SUPublicEDKey`, and `SUScheduledCheckInterval`, and set `SUEnableAutomaticChecks` to false in any distributed fork before its final signature**. The updater guard alone does not change the source feed.

This release was signed with `codesign --force --sign - --options 0` after packaging. Its ad hoc signature does not enable Hardened Runtime; loading the embedded Sparkle framework under library validation requires compatible developer signing.

## Verification

- **2026-10-01:** 443 XCTest tests passed; the zone editor and live Shift-drag snapping were verified on the development Mac.
- **2026-10-12 packaging:** universal Release build, app launch smoke checks, signature verification, DMG integrity checks, and native background-alias resolution after remounting at a different path passed. The full XCTest suite was not rerun for this packaging pass.

## Credits and licenses

Based on [Rectangle](https://github.com/rxhanson/Rectangle) by Ryan Hanson, itself based on Spectacle by Eric Czarny. The upstream [MIT license](LICENSE) and copyright notices are preserved.

Rectangle uses [Sparkle](https://github.com/sparkle-project/Sparkle) and [MASShortcut](https://github.com/rxhanson/MASShortcut). Their notices are included in the packaged app and the DMG's **Licenses** folder. The Finder-layout helper uses temporary packaging tools `ds-store` and `mac-alias`; these are not application dependencies.
