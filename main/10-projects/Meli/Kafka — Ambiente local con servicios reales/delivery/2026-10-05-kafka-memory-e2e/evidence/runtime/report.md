El SIGKILL está confirmado; su causa permanece desconocida. El hostagent usó `/usr/bin/ssh`, arrancó VZ y registró `signal: killed` con stdout y stderr vacíos. Un SSH de shell por stdin funcionó (exit 0, 76 ms), mientras el forwarding capturado por root recibió señal 9 en aproximadamente 200 ms.

La búsqueda del PID 41272 entre 15:52:29 y 15:52:50, incluidos info y debug, devolvió 0 eventos. Los eventos genéricos EndpointSecurity de esa ventana no identifican el PID ni el objeto; no prueban una denegación del forwarding. Tampoco hay evidencia suficiente para recomendar una actualización o cambio de seguridad.

Root detuvo la VM propia a las 15:55:47 tras el timeout de startup. El probe posterior al puerto antiguo terminó con exit 255 y es inconcluso. No se modificaron runtime compartido, configuración, servicios ni fuentes. No se instalaron dependencias ni se crearon forwards. La ejecución física Kafka permanece BLOCKED; los 845 unit PASS informados por root no certifican el backend.

No hay fix causal certificado. Cualquier siguiente acción requiere identificar primero el emisor del SIGKILL mediante diagnóstico autorizado del host; este turno no propone evadir controles ni alterar políticas. Los detalles y hashes quedan en `receipt.json`.
