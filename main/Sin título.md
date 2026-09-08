defaults write ~/Library/Preferences/com.apple.coreservices.useractivityd.plist ClipboardSharingEnabled -bool true
killall useractivityd
killall sharingd