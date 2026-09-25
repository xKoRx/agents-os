my fundedfutres
tradefy
sin consistencia en real





topstep
ludic

takeprofittrader
apex



y si el wn no muere:

```bash
sudo kill -KILL <PID>
```

Para cachar **servicios/containers/cgroups** que están chupando memoria, este es particularmente bueno:

```bash
systemd-cgtop
```

⚠️ No hagas `swapoff -a` a ciegas si estás corto de RAM; ahí sí puedes hacer pico Daedalus.

Si me pegas la salida de:

```bash
free -h; ps -eo pid,user,%mem,rss,cmd --sort=-rss | head -20
```

te digo inmediatamente qué wea está comiéndose la máquina.