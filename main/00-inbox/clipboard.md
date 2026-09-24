# 1. Verdict table

|CLAIM|CORRECT|CORRECT_WITH_CONDITIONS|WRONG|comentario corto|
|---|---|---|---|---|
|1||✓||Correcto para Brownian sin drift y barreras fijas; los saltos con overshoot requieren otra fórmula.|
|2|✓||Aritmética y descomposición correctas bajo ejecución continua, sin costes.||
|3||✓||Requiere que la riqueza detenida conserve su esperanza; ser martingala local y tener payoff terminal acotado no basta.|
|4||✓||El 40% exige barreras estáticas, absorción exacta y ausencia de censura o costes.|
|5|✓||Es la regla de multiplicación de probabilidades condicionales.||
|6||✓||Correcto para attempts IID y \(0<q\leq1\). Los valores numéricos son correctos.|
|7||✓||Correcto con payout fijo o media condicional, costes bien definidos y sin doble conteo.|
|8||✓||Clasificación correcta; un MDP exige un estado suficiente y una cadena absorbente supone una política fijada.|
|9||✓||Cambiar outcomes o aumentar win rate no crea por sí solo esperanza positiva de trading.|
|10||✓||La perturbación directa es coherente como modelo de hitting; no identifica por sí sola un proceso de mean reversion.|

# 2. Corrections

**Claim 1 — condiciones y overshoot.**

Para

\[ S_t=x+\sigma B_t,\qquad \sigma>0, \]

con \(L<U\) finitos y

\[ \tau=\inf\{t\geq0:S_t\notin(L,U)\}, \]

la continuidad implica \(S_\tau\in\{L,U\}\), la salida ocurre casi seguramente y el proceso detenido está acotado. Por tanto:

\[ x=E[S_\tau]=pU+(1-p)L, \qquad p=\frac{x-L}{U-L}. \]

Un random walk simétrico de pasos \(\pm h\) reproduce exactamente esa fórmula si \(L,x,U\) pertenecen a la misma retícula y las barreras son alcanzables sin overshoot.

Con saltos que cruzan barreras, suponiendo válida la conservación de esperanza:

\[ p=\frac{x-m_-}{m_+-m_-}, \]

donde

\[ m_+=E[S_\tau\mid\text{salida superior}],\qquad m_-=E[S_\tau\mid\text{salida inferior}]. \]

En general \(m_+\neq U\) y \(m_-\neq L\). Recortar artificialmente los resultados a las barreras cambia el payoff.

**Claim 2 — validado.**

El add conserva la riqueza instantánea:

\[ W_{\text{antes}}=-30,\qquad W_{\text{después}}=2(-30)+30=-30. \]

Después del add:

\[ P(\text{win}\mid S=-30)=\frac{-30-(-65)}{35-(-65)}=0.35. \]

La propiedad fuerte de Markov permite componer:

\[ P(\text{win}) =\frac{30}{130}+\frac{100}{130}\frac{35}{100} =\frac12. \]

Además, **sin agregar**, desde \(-30\), la probabilidad de alcanzar \(+100\) antes de \(-100\) también es \(70/200=35\%\). El add cambia los precios de salida y la duración, pero en este ejemplo conserva tanto la probabilidad condicional como la incondicional.

**Claim 3 — el requisito central es optional stopping válido.**

Sea la riqueza de trading:

\[ X_t=X_0+\int_0^t H_s\,dS_s. \]

La posición \(H\) debe ser **predecible e integrable respecto de \(S\)**. “Adapted” por sí solo no basta: ante saltos no puede observarse el salto y elegir retroactivamente la posición que lo captura.

Con \(X_0=0\), si:

- \(\tau<\infty\) casi seguramente;
- \(X_\tau\in\{G,-L\}\);
- \(E[X_\tau]=0\);

entonces necesariamente:

\[ P(X_\tau=G)=\frac{L}{G+L}. \]

Una condición suficiente general para conservar la esperanza es que \(X_{t\wedge\tau}\) sea una martingala uniformemente integrable.

Una condición suficiente especialmente simple para v0 es: riqueza continua, integral estocástica localmente bien definida, primera salida de \((-L,G)\) y salida casi segura. La riqueza detenida queda acotada en \([-L,G]\), lo que permite aplicar optional stopping.

No basta con que **únicamente la riqueza terminal** esté acotada. El contraejemplo clásico es apostar \(1,2,4,\ldots\) en juegos justos hasta la primera victoria: se obtiene \(+1\) casi seguramente, pero se requieren pérdidas intermedias y capital sin límite; falla la integrabilidad uniforme.

El leverage ilimitado no invalida automáticamente el resultado, pero elimina una salvaguarda importante. Deben verificarse la existencia de la integral y las condiciones de parada.

Para un horizonte \(T\), defínanse:

\[ r=P(\tau>T),\qquad m=E[X_T\,\mathbf1_{\{\tau>T\}}]. \]

Si optional stopping es válido para \(\tau\wedge T\):

\[ P(\text{hit }G\text{ antes de }-L\text{ y antes de }T) =\frac{L(1-r)-m}{G+L}. \]

Los casos sin absorción son un tercer outcome; no pueden descartarse ni contarse automáticamente como pérdidas de \(-L\).

Con overshoot medio condicional \(o_+,o_-\geq0\):

\[ P(\text{salida superior}) =\frac{L+o_-}{G+L+o_++o_-}, \]

si las salidas son \(G+o_+\) y \(-L-o_-\) en media y se conserva la esperanza.

Así, \(+1500/-2000\) produce exactamente \(4/7=57.142857\%\) bajo las condiciones originales válidas.

**Claim 4 — qué rompe el 40%.**

El resultado es correcto:

\[ P(\text{pass})=\frac{2000}{5000}=0.4. \]

- **Trades discretos:** no lo rompen necesariamente; lo rompen si introducen overshoot, otra distribución terminal o una regla de parada diferente.
- **Commissions debitadas del equity:** la riqueza neta deja de ser la martingala justa postulada. Si se pagan externamente sin afectar equity, cambia la economía, pero no necesariamente el 40%.
- **Trailing drawdown:** la barrera depende de la trayectoria; el máximo acumulado u otra referencia pasa a formar parte del estado.
- **Tiempo finito:** aparece la posibilidad de no alcanzar ninguna barrera.

**Claim 6 — dependencia y no estacionariedad.**

Para \(q=0.10\):

\[ E[N]=10,\qquad E[N-1]=9, \]

y:

\[ P(N\leq10)=65.1322\%,\quad P(N\leq20)=87.8423\%,\quad P(N\leq30)=95.7609\%. \]

Con attempts independientes pero probabilidades \(q_i\) diferentes:

\[ P(N\leq n)=1-\prod_{i=1}^n(1-q_i). \]

La media ya no es \(1/q\).

Con dependencia puede usarse la misma expresión únicamente si cada \(q_i\) representa la probabilidad de éxito **condicional a todos los fracasos anteriores**. Las probabilidades marginales no bastan. Por ejemplo, con resultados perfectamente correlacionados y marginal \(q=0.1\), comprar diez attempts sigue dando solo un 10% de probabilidad de algún éxito.

**Claim 7 — economía y break-even.**

Defínanse indicadores:

\[ I=\mathbf1_{\{\text{evaluation aprobada}\}},\qquad J=\mathbf1_{\{\text{primer payout recibido}\}}, \qquad J\leq I. \]

Si \(W\) es fijo:

\[ R=JW-F-IA-K, \qquad E[K]=C. \]

Por linealidad:

\[ E[R]=qW-F-p_{\text{pass}}A-C. \]

No hace falta independencia entre costes y outcomes.

Si el payout varía, debe usarse:

\[ W=E[\text{cash recibido}\mid J=1], \]

no su media incondicional.

Para \(W>0\), manteniendo los demás parámetros:

\[ \boxed{q_{\mathrm{BE}}=\frac{F+p_{\text{pass}}A+C}{W}}. \]

La viabilidad exige:

\[ q_{\mathrm{BE}}\leq p_{\text{pass}}\leq1, \]

porque \(q\leq p_{\text{pass}}\).

Una comisión descontada del saldo nominal puede afectar la supervivencia sin constituir un desembolso personal adicional. Una deducción ya incluida en \(W\) neto no vuelve a cargarse en \(C\).

**Claim 8 — precisión de clasificación.**

Con acciones por elegir, el problema es de control estocástico. Es un MDP si el estado contiene toda la información relevante para la transición. Con una política fijada y estados adecuados, pasa a ser un proceso de Markov con absorción.

Que una contraparte cambie reglas no basta por sí solo para convertirlo en game theory: debe existir una interacción estratégica entre decisiones de distintos agentes.

**Claim 9 — distinguir tres conceptos.**

Deben separarse:

1. probabilidad de ganar;
2. esperanza de riqueza de trading;
3. esperanza de cash personal extraído.

El caso B no crea esperanza positiva de trading bajo una martingala y condiciones admisibles. Por ejemplo:

\[ P(+1)=99\%,\qquad P(-99)=1\% \]

produce 99% de victorias y esperanza cero.

A y D permiten esperanza positiva, pero no la garantizan para cualquier sizing. En un modelo:

\[ dS_t=\mu_tdt+\sigma_tdB_t, \]

bajo integrabilidad suficiente:

\[ E[X_\tau]=E\!\left[\int_0^\tau H_t\mu_t\,dt\right]. \]

Importa cómo la exposición coincide con el drift condicional.

C puede generar valor económico sin edge de precio: el cash personal es un payoff distinto de la riqueza nominal, con pérdidas asumidas parcialmente por otra parte. Esto **no contradice** optional stopping aplicado a la riqueza de trading. Tampoco exige reglas path-dependent: un contrato estático con responsabilidad limitada ya puede generar esa diferencia.

**Claim 10 — recomendación: A, kernel de absorción condicional.**

En el estado adverse seleccionado, con próximas salidas terminales \(a<s<b\):

\[ p_0=\frac{s-a}{b-a},\qquad p_\delta=p_0+\delta. \]

Se selecciona la salida superior con probabilidad \(p_\delta\) y la inferior con probabilidad \(1-p_\delta\). Debe exigirse \(0\leq p_\delta\leq1\); configuraciones fuera del intervalo son inválidas.

Para v0, aplicar esta modificación **una sola vez por trade, después del último add previsto y sin eventos intermedios pendientes**. Así se modifica exactamente la probabilidad de la próxima salida terminal.

Esto define un modelo probabilístico coherente y suficiente para economía sin tiempo. Es un **edge condicional de hitting**; no permite afirmar una dinámica específica de mean reversion entre los extremos.

En el claim 2:

\[ P(\text{win})=\frac12+\frac{10}{13}\delta, \qquad E[X_\tau]=\frac{2000}{13}\delta. \]

El edge global queda ponderado por la probabilidad de alcanzar el estado adverse.

# 3. Minimal simulator math spec v0

**State variables**

Por attempt:

- fase \(z\in\{\text{EVALUATION},\text{FUNDED},\text{FAIL},\text{FIRST PAYOUT}\}\);
- equity nominal realizado \(B\) al inicio del trade;
- precio relativo \(s\), reiniciado a cero al abrir cada trade;
- posición long \(h\);
- término contable \(b\), con PnL del trade \(Y=b+hs\);
- equity total de fase \(E=B+Y\);
- índice del próximo add y flag de edge disponible;
- cash personal acumulado \(K\).

El nocional comercial de la cuenta no entra en \(K\).

Parámetros configurados: \(F,A,C,W\); barreras de fase \((-D_z,T_z)\); stop/target de trade \((-\ell,G)\); posición inicial \(h_0\); lista finita de adds; límite \(h_{\max}\); escenario \(\delta\). Todos los tamaños son positivos y \(h_0\leq h\leq h_{\max}<\infty\).

Para evaluation:

\[ D_{\mathrm{eval}}=2000,\qquad T_{\mathrm{eval}}=3000. \]

Los umbrales funded quedan simbólicos: \(D_{\mathrm{fund}},T_{\mathrm{fund}}>0\).

**Stochastic process**

Null model:

\[ ds_t=dB_t. \]

Se normalizan volatilidad y valor monetario por unidad de precio a uno: v0 no calcula tiempos y estas escalas no alteran las probabilidades de hitting.

La simulación usa directamente el kernel exacto entre eventos:

\[ P(\text{próximo evento superior})=\frac{s-a}{b-a}. \]

No necesita discretización temporal.

Cada nueva compra es independiente y usa los mismos parámetros y políticas.

**Actions**

- Apertura: \(s=0,\ b=0,\ h=h_0\).
- Add \(\Delta h>0\) al precio observado \(s\):\[ h'=h+\Delta h,\qquad b'=b-\Delta h\,s. \]Así \(b'+h's=b+hs\): el add es self-financing.
- Cierre total en barrera; no hay partial exits.
- Después de un cierre ordinario: \(B'=E\), y se abre otro trade con \(h_0\).

La política entre trades es constante en v0. La política intratrade es una lista finita de niveles adverse estrictamente decrecientes y cantidades predeterminadas. El edge inicial es cero; el único edge sintético permitido es el kernel condicional descrito arriba.

**Barriers**

Las salidas del trade son \(Y=-\ell\) y \(Y=G\). Las de la fase son \(E=-D_z\) y \(E=T_z\).

Como \(h>0\), los precios terminales activos son:

\[ a_{\mathrm{term}} =\max\!\left( \frac{-\ell-b}{h}, \frac{-D_z-B-b}{h} \right), \]\[ b_{\mathrm{term}} =\min\!\left( \frac{G-b}{h}, \frac{T_z-B-b}{h} \right). \]

El siguiente add es otro evento inferior si está estrictamente entre \(a_{\mathrm{term}}\) y \(s\). Un add situado más allá de una barrera no se ejecuta.

**Transition/absorption logic**

1. Identificar el evento más cercano por debajo y por encima del precio.
2. Elegir cuál se alcanza primero mediante el kernel exacto.
3. Actualizar el precio al nivel del evento.
4. Si se alcanza una barrera de fase, absorber o cambiar de fase.
5. En caso contrario, ejecutar el cierre del trade o el add correspondiente.

En coincidencias: **barrera de fase → cierre del trade → add**.

Después del último add de un trade elegible, sustituir el kernel de la próxima salida terminal por \(p_0+\delta\). Consumir el flag; no sumar \(\delta\) repetidamente.

No existe timeout en v0. No se eliminan observaciones sin absorción. Un límite técnico de ejecución debe señalar un resultado incompleto, nunca inventar un fracaso.

**Lifecycle composition**

\[ \text{PURCHASE}\to\text{EVALUATION} \to\text{FUNDED}\to\text{FIRST PAYOUT}. \]

- Compra: desembolso \(F+C\).
- Evaluation inferior: FAIL.
- Evaluation superior: pagar \(A\), entrar en FUNDED y reiniciar su equity a cero.
- Funded inferior: FAIL.
- Funded superior: recibir \(W\), terminar en FIRST PAYOUT.

Las fases usan incrementos aleatorios independientes y parámetros fijos. Bajo el null:

\[ p_{\mathrm{pass}}=\frac{D_{\mathrm{eval}}}{T_{\mathrm{eval}}+D_{\mathrm{eval}}}, \qquad p_{\mathrm{funded}}=\frac{D_{\mathrm{fund}}}{T_{\mathrm{fund}}+D_{\mathrm{fund}}}, \]\[ q=p_{\mathrm{pass}}p_{\mathrm{funded}}. \]

La política de cohort es comprar attempts IID hasta el primer payout o hasta un número prefijado \(n\). No hay restricción de presupuesto personal en v0.

**Economics**

Por attempt:

\[ R=JW-F-IA-C. \]

Para v0, \(C\) se representa como un cargo determinista por compra, equivalente a su esperanza para calcular EV sin descuento ni restricción de capital. Esto no reproduce la distribución de costes variables.

La métrica principal es:

\[ E[R]=qW-F-p_{\mathrm{pass}}A-C. \]

Los costes de ejecución debitados del equity se fijan en cero en este null model. El cash cobrado \(W\) es neto de las deducciones incorporadas al payout. No se atribuye valor posterior al primer payout.

# 4. Analytical acceptance tests

Para \(N=10^6\) observaciones independientes, usar como tolerancia estadística:

\[ |\widehat p-p|\leq5\sqrt{\frac{p(1-p)}N}, \qquad |\overline X-E[X]|\leq5\sqrt{\frac{\operatorname{Var}(X)}N}. \]

Son umbrales probabilísticos, no garantías absolutas. En las tablas, las tolerancias de probabilidades son absolutas: \(0.0025=0.25\) puntos porcentuales.

|Test|Setup|Resultado analítico esperado|Tolerancia con \(N\approx10^6\)|Failure interpretation|
|---|---|---|---|---|
|**T1**|Brownian justo; \(h=1\); terminales \(\pm100\); sin adds.|\(p=0.5\); \(E[X]=0\).|Probabilidad: ±0.0025. Media monetaria: ±0.50.|Sesgo del kernel, barreras mal ubicadas o error en payoff.|
|**T2**|Claim 2: add de 1 en \(-30\); terminales monetarios \(\pm100\).|Llegar al add: \(10/13\). Win condicionado al add: 0.35. Win total: 0.5. \(E[X]=0\).|Total: ±0.0025; media: ±0.50. Condicional: \(5\sqrt{0.35(0.65)/N_{\mathrm{add}}}\), aproximadamente ±0.00272.|Error de self-financing, average price o combinación de ramas.|
|**T3**|\(h=1\); agregar 1 en \(-20\) y 1 en \(-40\); mantener riqueza terminal \(\pm100\).|\(p=\frac16+\frac56[\frac14+\frac34\frac15]=0.5\). Tras segundo add: \(Y=3s+60\), salidas \(40/3\) y \(-160/3\).|Probabilidad: ±0.0025. Media: ±0.50.|Cambios de sizing están creando riqueza contable o alterando outcomes terminales.|
|**T4**|Evaluation abstracta continua; \(E_0=0\); barreras \(+3000/-2000\).|Pass: 0.4; burn: 0.6; \(E[E_\tau]=0\).|Pass: ±0.00245. Media de equity terminal: ±12.25.|Overshoot artificial, costes implícitos, censura o fórmula de hitting incorrecta.|
|**T5**|Un millón de cohortes IID hasta primer éxito, \(q=0.1\).|Media attempts: 10; failures: 9. Éxito en 10/20/30: 0.651322 / 0.878423 / 0.957609.|Medias: ±0.04744. Probabilidades: ±0.002383 / ±0.001635 / ±0.001008.|Off-by-one, truncamiento de colas o dependencia entre attempts.|
|**T6**|\(p_{\mathrm{pass}}=0.4\), \(p_{\mathrm{funded}}=0.25\), \(q=0.1\); \(F=100,A=50,W=1500,C=10\).|\(R=-110,-160,1340\) con probabilidades \(0.6,0.3,0.1\). \(E[R]=20\); \(\operatorname{Var}(R)=194100\). Break-even \(q=0.0866667\).|Media de cash: ±2.203. \(q\): ±0.0015.|Activation cobrada al grupo equivocado, payout fuera de funded, coste duplicado o multiplicación incorrecta.|
|**T7**|Repetir T2 con kernel sintético y \(\delta=0\).|Kernel idéntico al null; \(p=0.5\), \(E[X]=0\).|Identidad algebraica del kernel dentro de precisión numérica; Monte Carlo: mismas tolerancias que T2.|El mecanismo de edge altera el baseline incluso con edge cero.|
|**T8 — crítico**|T2 con \(\delta=0.10\), aplicado solo al alcanzar el add.|Win condicional: 0.45. Win total: \(15/26=0.5769231\). \(E[X]=200/13=15.384615\).|Win total: ±0.002471. Media: ±0.495.|Se agregó \(\delta\) globalmente, se aplicó más de una vez o no se ponderó la llegada al estado adverse.|

Además, verificar como **invariantes deterministas**, sin tolerancia Monte Carlo:

- cada add conserva \(Y\), salvo redondeo numérico;
- \(J\leq I\) en todos los attempts;
- \(h\leq h_{\max}\);
- no hay salidas fuera de las barreras en el modelo continuo;
- una probabilidad fuera de \([0,1]\) provoca rechazo de configuración, no clipping silencioso.

# 5. Hidden assumptions / traps

1. **Riqueza nominal y cash personal son variables distintas.** Una martingala nominal puede coexistir con EV personal positivo por la estructura contractual.
2. **Optional stopping puede fallar.** Payoff terminal acotado no sustituye el control de pérdidas y exposición durante la trayectoria.
3. **La absorción debe ocurrir.** Detenerse sin cerrar, pausar indefinidamente o censurar runs rompe las fórmulas binarias.
4. **El monitoreo es continuo y la ejecución exacta.** Saltos, gaps, slippage y pasos temporales pueden introducir overshoot.
5. **El add es self-financing.** Cambiar el average price no recupera pérdidas ni agrega riqueza instantánea.
6. **El edge se introduce como supuesto.** Un \(\delta>0\) es un escenario de sensibilidad, no evidencia de rentabilidad ni de mean reversion real.
7. **Mayor win rate no implica mayor expectancy.** Deben conservarse y contabilizarse todos los tamaños de pérdidas y ganancias.
8. **Las fórmulas geométricas requieren attempts IID.** Compartir mercado, señal o régimen puede producir fuerte correlación.
9. **Los costes deben tener un único tratamiento económico.** Distinguir cargos al equity nominal, desembolsos personales y deducciones ya incluidas en \(W\).
10. **El kernel de hitting omite el tiempo y el interior de las trayectorias.** No permite calcular deadlines, cargos por duración, trailing drawdown ni necesidades reales de liquidez.

# 6. Explicitly defer

- Market data histórico, backtesting y estimación empírica de \(\delta\).
- Drift continuo, procesos de mean reversion y microestructura.
- Saltos, ejecución discreta, slippage y comisiones debitadas del equity.
- Trailing drawdown, daily loss limits, consistency rules y restricciones de calendario.
- Partial exits, scratch, break-even y optimización de sizing.
- Resets internos y distribuciones de costes variables.
- Attempts correlacionados, probabilidades cambiantes y presupuesto personal limitado.
- Payouts posteriores al primero y lifetime value.
- Respuesta estratégica de la prop y game theory.
- Optimización de portfolio, implementación e infraestructura.

# 7. Final verdict

**MATH_GO**

Para el contrato v0 corregido y delimitado en la sección 3.