Para **liberar RAM al tiro** en Daedalus:

```bash
sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
```

Eso libera **page cache + dentries + inodes**. No mata procesos.

Pero si una wea realmente se está comiendo la RAM, encuentra al culpable:

```bash
ps -eo pid,user,%mem,rss,cmd --sort=-rss | head -20
```

Y mira el estado real:

```bash
free -h
```

Si pillas un proceso descontrolado, mejor córtalo limpiamente:

```bash
sudo kill -TERM <PID>
```

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