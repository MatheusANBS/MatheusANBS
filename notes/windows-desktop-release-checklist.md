# Windows desktop release checklist

A compact checklist I use before publishing a Windows desktop build.

## Application

- Build the production frontend instead of pointing the webview at a development server.
- Launch without an attached console window for GUI releases.
- Verify app name, version, publisher, executable metadata, and window title.
- Regenerate every icon size after changing the source artwork.
- Test startup from a clean directory, not only from the development tree.
- Confirm configuration and data paths use the proper per-user Windows directories.

## Runtime behavior

- Test the first launch, a normal relaunch, and launch after a Windows restart.
- Exercise offline behavior and missing-service states.
- Check high-DPI scaling at 100%, 125%, and 150%.
- Verify keyboard navigation, global hotkeys, tooltips, dialogs, and notifications.
- Confirm background tasks stop cleanly when the main window closes.

## Packaging

- Produce a clean release build from the committed lockfiles.
- Install on a machine or VM without the development toolchain.
- Test uninstall and upgrade over the previous release.
- Scan the final installer and binaries, then record checksums.
- Keep symbols or diagnostic artifacts privately when crash investigation may need them.

## Repository

- Tag the exact source commit used for the binary.
- Let CI reproduce the build and run security checks.
- Write release notes around user-visible changes, known limitations, and compatibility.
- Attach only the intended artifacts and verify each download once after publication.
