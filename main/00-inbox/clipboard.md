Sí. Esa wea es **Universal Clipboard**, y cuando falla intermitentemente normalmente no es el portapapeles en sí: queda pegado algún daemon de Continuity/Handoff. Apple confirma que depende de **misma cuenta Apple + Bluetooth + Wi-Fi + Handoff + proximidad**. ([Soporte Apple](https://support.apple.com/es-la/102430?utm_source=chatgpt.com "Usa Portapapeles universal para copiar y pegar contenido de un dispositivo Apple a otro - Soporte técnico de Apple"))

Yo iría KISS, en este orden:

1. **Cuando vuelva a fallar, no reinicies los Macs todavía.** En el Mac donde no está funcionando:
    
    ```bash
    killall useractivityd
    killall sharingd
    killall pboard
    ```
    
    Los tres los vuelve a levantar `launchd` automáticamente. `useractivityd` maneja Handoff, `sharingd` el transporte entre dispositivos y `pboard` el clipboard local. Es un reset bastante inocuo y hay evidencia reciente de que recupera Universal Clipboard sin reboot. ([GitHub](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/mac_universal_clipboard.md?utm_source=chatgpt.com "context-infrastructure/rules/skills/mac_universal_clipboard.md at main · grapeot/context-infrastructure · GitHub"))
    
2. Si sigue muerto:
    
    ```bash
    sudo killall bluetoothd
    ```
    
    Vas a perder Bluetooth unos segundos y debería reconectarse solo. Hay casos recientes de macOS donde **`bluetoothd` queda zombie aunque Bluetooth aparentemente funcione** y esto recupera Universal Clipboard. ([Ask Different](https://apple.stackexchange.com/questions/486949/universal-clipboard-works-iphone-%E2%86%92-mac-but-not-mac-%E2%86%92-iphone-while-airdrop-works?utm_source=chatgpt.com "macos - Universal Clipboard works iPhone → Mac but not Mac → iPhone, while AirDrop works both ways - Ask Different"))
    
3. Si vuelve a romperse frecuentemente, revisaría en **ambos Macs**:  
    **System Settings → General → AirDrop & Handoff → Allow Handoff between this Mac and your iCloud devices**. Apágalo/enciéndelo una vez. También confirma Wi-Fi y Bluetooth activos y misma Apple Account. Apple recomienda justamente esas comprobaciones. ([Soporte Apple](https://support.apple.com/es-la/102430?utm_source=chatgpt.com "Usa Portapapeles universal para copiar y pegar contenido de un dispositivo Apple a otro - Soporte técnico de Apple"))
    
4. Si todavía se pone weón, hay un estado específico que podemos forzar:
    
    ```bash
    defaults write ~/Library/Preferences/com.apple.coreservices.useractivityd.plist ClipboardSharingEnabled -bool true
    killall useractivityd
    killall sharingd
    ```
    
    Esto ya es el segundo escalón; **no partiría tocando preferences** si matar los daemons lo arregla. Está documentado como workaround por usuarios y sigue apareciendo reportado como efectivo en 2026. ([Apple Community](https://discussions.apple.com/thread/253274114?utm_source=chatgpt.com "FIX for Universal Clipboard copy/paste no… - Apple Community"))
    

### Lo primero que probaría yo

Cuando se te corte de nuevo:

```bash
killall useractivityd sharingd pboard
```

y prueba inmediatamente Mac A → Mac B y Mac B → Mac A.

Si eso **lo arregla al tiro**, ya tenemos localizado el tipo de falla y no necesitas andar reiniciando las máquinas como cavernícola cada vez. 😆

Además, ojo con **VPNs/firewalls**: si tienes alguno de los Macs conectado a VPN corporativa, Tailscale u otra interfaz rara cuando ocurre, vale la pena probar desconectándolo. Continuity usa Bluetooth + networking peer-to-peer y esas weas pueden meter ruido aunque AirDrop parezca funcionar normalmente. ([Apple Community](https://discussions.apple.com/thread/256040651?utm_source=chatgpt.com "How to fix Universal Clipboard and iPhone… - Apple Community"))

Si te pasa seguido, ahí sí conviene dejar un comando tipo `fixclipboard` que haga solamente este reset seguro en ambos Macs.