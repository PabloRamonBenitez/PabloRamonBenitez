"""TRADUCCIÓN DE LOS PLANOS AL UCRANIANO (usuario 26/11: «todas las leyendas en ucraniano»).
Se aplica a cada texto de la hoja justo antes de guardarla (Figure.savefig y PdfPages.savefig), así sirve para todos los
generadores sin tocar su código. Diccionario por frases (las largas primero) con límites de palabra; los códigos (F01, L1,
S4, MGF, ALAMY, Google Maps) y las cifras se conservan. IDIOMA_PLANOS=es desactiva la traducción.
Plantas: numeración ucraniana (la planta baja es el 1.er piso): «planta 1» → «2-й поверх»."""
import os, re
import matplotlib
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.backends.backend_pdf import PdfPages

ACTIVO = os.environ.get("IDIOMA_PLANOS", "uk") == "uk"
_W = r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]"

FRASES = [
 # ---- cajetín, portada, notas
 ("levantamiento desde fotografías", "обмірне креслення за фотографіями"), ("levantamiento desde fotos", "обмірне креслення за фотографіями"),
 ("HOTEL SALUT", "ГОТЕЛЬ «САЛЮТ»"), ("Kyiv", "Київ"),
 ("Juego de planos para imprimir", "Комплект креслень для друку"), ("imprimir al", "друк у масштабі"), ("sin ajustar", "без підгонки"),
 ("Fuente única: cuadro de cotas (cotas.py). Medidas estimadas con margen (ver cuadro).", "Єдине джерело: таблиця розмірів (cotas.py). Розміри оцінені з допуском (див. таблицю)."),
 ("Fuente única: cuadro de cotas. Medidas estimadas con margen.", "Єдине джерело: таблиця розмірів. Розміри оцінені з допуском."),
 ("Portada, índice y situación de secciones", "Титульний аркуш, зміст і схема розрізів"), ("Índice", "Зміст"),
 ("Cotas en m. Trazo grueso relleno: cortado · fino: visto · discontinuo: por encima.",
  "Розміри в м. Товста лінія із заливкою: у розрізі · тонка: видиме · штрихова: вище січної площини."),
 ("Trazo grueso con trama: cortado · fino: visto ·", "Товста лінія зі штрихуванням: у розрізі · тонка: видиме ·"),
 ("discontinuo: por encima.", "штрихова: вище січної площини."),
 ("Los tres dibujos están a la misma escala y alineados:", "Три креслення в одному масштабі й вирівняні:"),
 ("la misma vertical de puntos cruza sección, planta y alzado.", "одна пунктирна вертикаль проходить через розріз, план і фасад."),
 ("Los tres dibujos tienen el mismo eje horizontal (−x): las verticales discontinuas son las mismas fachadas en los tres.",
  "Три креслення мають спільну горизонтальну вісь (−x): штрихові вертикалі – ті самі фасади на всіх трьох."),
 ("flecha = vista del alzado.", "стрілка = напрям погляду фасаду."), ("Niveles:", "Позначки:"),
 ("cotas en m", "розміри в м"), ("Cotas en m.", "Розміри в м."), ("Medidas de fotos", "Розміри за фото"),
 ("ver CUADRO DE COTAS", "див. ТАБЛИЦЮ РОЗМІРІВ"), ("y de Bing/Google", "і за Bing/Google"), ("Trazo grueso con trama: cortado.", "Товста лінія зі штрихуванням: у розрізі."),
 ("Fino: visto.", "Тонка: видиме."), ("Discontinuo: por encima.", "Штрихова: вище січної площини."), ("(situación)", "(ситуаційний план)"), ("Escala", "Масштаб"),
 ("Mismo norte y orientación que todas las plantas del juego.", "Північ і орієнтація ті самі, що й на всіх планах комплекту."),
 ("y marcas del usuario", "і позначки замовника"), ("Fuentes:", "Джерела:"),
 ("Plantas", "Плани"), ("secciones y alzados", "розрізи й фасади"), ("detalles", "деталі"),
 # ---- plano de lugar
 ("PLANO DE LUGAR", "СИТУАЦІЙНИЙ ПЛАН"), ("situación del hotel y entorno según las fotos de la época", "розташування готелю й оточення за фотографіями того часу"),
 ("El edificio es la planta de cubiertas del modelo (figura clara). El entorno, según las fotos de",
  "Будівля – план покрівлі моделі (світла фігура). Оточення – за фотографіями"),
 ("antes de las vallas posteriores. Caminos y árboles: trazado y posición aproximados (fotos oblicuas).",
  "до пізніших огорож. Доріжки й дерева: трасування й положення приблизні (перспективні фото)."),
 ("EDIFICIO COLINDANTE", "СУСІДНЯ БУДІВЛЯ"), ("PARQUE", "ПАРК"), ("PLAZA", "ПЛОЩА"), ("(pavimento)", "(мощення)"), ("arbolado", "дерева"),
 ("calle Ivana Mazepy", "вул. Івана Мазепи"), ("autobuses", "автобуси"), ("vial de servicio: bordillo y eje", "службовий проїзд: бордюр і вісь"),
 ("plaza abierta a la calle, sin bordillo", "площа відкрита до вулиці, без бордюру"), ("desde la calle Ivana Mazepy", "з вул. Івана Мазепи"), ("hacia la calle", "на вулицю"), ("pasa bajo el vuelo de la torre", "проходить під виносом вежі"), ("(asfalto)", "(асфальт)"), ("sigue al patio", "продовжується до двору"), ("allí gira o sale", "там розвертається або виїжджає"), ("duda", "питання"), ("entra desde la calle", "в'їжджає з вулиці"), ("por la plaza, sube por el vial y rodea el testero", "через площу, піднімається проїздом і огинає торець"), ("plaza de asfalto: sin bordillo hacia la calle", "асфальтована площа: без бордюру з боку вулиці"), ("vial junto al ala larga", "проїзд біля довгого крила"), ("plaza, vial y parque", "площа, проїзд і парк"), ("plaza abierta a la calle", "площа відкрита до вулиці"), ("vial de servicio", "службовий проїзд"), ("rodea el testero por detrás", "огинає торець ззаду"), ("continúa al patio y al garaje", "продовжується до двору і гаража"), ("vehículo de servicio", "службовий транспорт"), ("recorrido en bucle, sin maniobras", "кільцевий маршрут без маневрів"), ("camión", "вантажівка"), ("explanada de maniobra", "розворотний майданчик"), ("pavimento, F35", "мощення, F35"), ("glorieta de giro", "розворотне кільце"), ("isleta", "острівець"),
 ("camión rígido", "вантажівка"), ("recorrido y barrido del camión", "траєкторія й габарит повороту вантажівки"),
 ("recorrido y barrido", "траєкторія й габарит повороту"), ("senda peatonal (losas)", "пішохідна доріжка (плити)"),
 ("senda peatonal", "пішохідна доріжка"), ("senda a la plaza", "доріжка до площі"), ("césped (punteado)", "газон (крапки)"), ("césped", "газон"),
 ("patio de la L", "двір Г-подібного корпусу"), ("(sin foto)", "(без фото)"), ("fuente en media luna", "фонтан-півмісяць"),
 ("medianera (linde)", "брандмауер (межа ділянки)"), ("linde / medianera", "межа ділянки / брандмауер"), ("edificio (cubiertas)", "будівля (покрівлі)"),
 ("árbol (copa y tronco)", "дерево (крона й стовбур)"), ("pavimento de la plaza", "мощення площі"), ("edificio colindante", "сусідня будівля"),
 ("césped y camino junto al ala larga", "газон і доріжка біля довгого крила"), ("plaza, fuente, colindante y parque", "площа, фонтан, сусідня будівля й парк"),
 ("camino y césped ante el testero", "доріжка й газон перед торцем"),
 # ---- títulos de hojas
 ("PLANTA BAJA", "ПЛАН 1-ГО ПОВЕРХУ"), ("PLANTA PRIMERA", "ПЛАН 2-ГО ПОВЕРХУ"), ("PLANTA SEGUNDA", "ПЛАН 3-ГО ПОВЕРХУ"),
 ("PLANTA TIPO DE HABITACIONES", "ПЛАН ТИПОВОГО ПОВЕРХУ НОМЕРІВ"), ("PLANTA DE CUBIERTAS", "ПЛАН ПОКРІВЛІ"),
 ("Planta baja", "План 1-го поверху"), ("Planta de cubiertas", "План покрівлі"), ("Planta tipo de habitaciones", "План типового поверху номерів"),
 ("planta tipo de habitaciones", "план типового поверху номерів"), ("Planta última – tambor", "Верхній рівень – барабан"),
 ("planta tipo de la torre", "типовий поверх вежі"), ("(planta tipo)", "(типовий поверх)"),
 ("por las ventanas", "по вікнах"), ("corte a", "переріз на"), ("suelo", "підлога"),
 ("ALA CORTA", "КОРОТКЕ КРИЛО"), ("ALA LARGA", "ДОВГЕ КРИЛО"), ("CHAFLÁN", "ЗРІЗАНИЙ КУТ"), ("TESTERO", "ТОРЕЦЬ"),
 ("ALZADO", "ФАСАД"), ("SECCIÓN", "РОЗРІЗ"), ("LONGITUDINAL", "ПОЗДОВЖНІЙ"), ("PLANTA", "ПЛАН"), ("Sección", "Розріз"),
 ("Testero y secciones transversales del ala larga", "Торець і поперечні розрізи довгого крила"),
 ("Detalles: planta tipo de la torre y encuentro escalera – rampa – bar", "Деталі: типовий поверх вежі та вузол сходи – пандус – бар"),
 ("escalera en cuña y encuentro con la rampa del techo", "сходи в клині й примикання пандуса покрівлі"),
 ("Detalle", "Деталь"), ("Detalles", "Деталі"),
 ("por el eje de la escalera", "по осі сходів"), ("por el eje de la torre paralela al chaflán", "по осі вежі паралельно до зрізаного кута"),
 ("por la terraza mirando al bar", "по терасі з видом на бар"), ("el bar, su vuelo y la cubierta inclinada en alzado", "бар, його виліт і похила покрівля у фасаді"),
 ("por el bar, la escalera y la torre", "через бар, сходи й вежу"), ("longitudinal por el bar, la escalera y la torre", "поздовжній через бар, сходи й вежу"),
 ("a lo largo del ala corta por el bloque alto y la torre", "вздовж короткого крила через високий блок і вежу"),
 ("transversal del ala larga por el eje del hueco", "поперечний довгого крила по осі отвору"), ("(tramo final sin bar)", "(кінцева ділянка без бару)"),
 ("huecos alto y bajo cortados", "верхній і нижній отвори в розрізі"), ("huecos alto y bajo", "верхній і нижній отвори"),
 ("escalera, barril, cuello, bar y ala larga entera", "сходи, циліндр, шийка, бар і все довге крило"),
 ("restaurante, columna, hotel y esquina a", "ресторан, колона, готель і кут"),
 ("a lo largo de la calle", "вздовж вулиці"), ("(mirando al bar)", "(з видом на бар)"), ("a la calle", "на вулицю"),
 ("fachada exterior del ala larga", "зовнішній фасад довгого крила"), ("fachada exterior", "зовнішній фасад"),
 ("patio interior de la L", "внутрішній двір Г-подібного корпусу"), ("patio interior", "внутрішній двір"),
 ("testero del ala larga", "торець довгого крила"), ("(frontal)", "(головний)"), ("(fachada exterior)", "(зовнішній фасад)"),
 ("(bar, terraza, concha)", "(бар, тераса, «раковина»)"),
 # ---- leyendas de fotos
 ("ALAMY – barril medido por MGF", "ALAMY – циліндр, обміряний за МГФ"), ("ALAMY – torre medida por MGF", "ALAMY – вежа, обміряна за МГФ"),
 ("ALAMY – parte alta", "ALAMY – верхня частина"), ("y pico", "з гаком"), ("paños", "панелей"),
 ("planta baja del chaflán y entrada del hotel", "1-й поверх зрізаного кута і вхід до готелю"), ("rampa de acceso y esquina", "вхідний пандус і кут"),
 ("testero y huecos del ala", "торець і отвори крила"), ("testero, puerta y marquesina", "торець, двері й навіс"),
 ("maqueta: curva de la rampa y techo en rampa", "макет: крива пандуса й покрівля-пандус"), ("vista aérea", "вигляд з висоти"),
 ("cenital: encuentro barril – ala", "вид зверху: примикання циліндра до крила"), ("cenital", "вид зверху"),
 ("escalera en cuña con lamas", "сходи в клині з ламелями"), ("rellanos tras las lamas", "майданчики за ламелями"),
 ("chaflán: restaurante, columna, hotel", "зрізаний кут: ресторан, колона, готель"), ("calle desde el ala corta", "вулиця з боку короткого крила"),
 ("escalera desde el patio", "сходи з двору"), ("escalera y aletas", "сходи й ребра"), ("escalera y barril", "сходи й циліндр"),
 ("huecos del ala y rampa", "отвори крила й пандус"), ("bar y terraza", "бар і тераса"), ("desde el testero", "з боку торця"),
 ("cubierta inclinada del restaurante", "похила покрівля ресторану"), ("cubierta del restaurante", "покрівля ресторану"), ("cubierta inclinada", "похила покрівля"), ("actual", "сучасний стан"),
 # ---- rótulos de plantas y secciones
 ("rampa de acceso · sube a", "вхідний пандус · підйом до"), ("rampa de acceso", "вхідний пандус"), ("(hotel debajo)", "(під ним готель)"),
 ("final del giro", "кінець повороту"), ("(peto en U)", "(U-подібний парапет)"), ("lucernarios piramidales", "пірамідальні ліхтарі"),
 ("vidrio", "скло"), ("caja de escalera", "сходова клітка"), ("por encima", "вище"), ("terraza-restaurante", "тераса-ресторан"),
 ("rellano de planta", "поверховий майданчик"), ("rellano de vuelta", "проміжний майданчик"), ("vestíbulo", "вестибюль"), ("circulaciones", "комунікації"),
 ("visera desplazada", "зміщений козирок"), ("vuelo del barril", "виліт циліндра"), ("vuelo de la cubierta del bar", "виліт покрівлі бару"),
 ("vigas radiales (ménsulas) y barril", "радіальні балки (консолі) й циліндр"), ("paso libre", "вільний прохід"), ("eje torre", "вісь вежі"),
 ("inicio chaflán", "початок зрізу"), ("fin chaflán", "кінець зрізу"), ("fin bar", "кінець бару"), ("fin concha", "кінець «раковини»"),
 ("pie concha", "основа «раковини»"), ("extremo ala corta", "кінець короткого крила"), ("fachada ext.", "зовн. фасад"), ("fachada patio", "фасад у двір"),
 ("esquina chaflán", "кут зрізу"), ("intereje", "крок осей"), ("huecos a", "отвори з кроком"), ("junto al testero", "біля торця"),
 ("situación de secciones", "схема розрізів"), ("techo-rampa", "покрівля-пандус"), ("módulos", "модулів"), ("escalera en cuña", "сходи в клині"),
 ("ª planta hab,", "-й поверх номерів"), ("ª planta hab.", "-й поверх номерів"), ("ª hab,", "-й пов. номерів"), ("ª hab.", "-й пов. номерів"),
 ("cub, bar / bloque alto", "покр. бару / високого блоку"), ("cub. bar / bloque alto", "покр. бару / високого блоку"),
 ("cub, hab,", "покр. номерів"), ("cub. hab.", "покр. номерів"), ("cub, habitaciones", "покр. номерів"), ("cub. habitaciones", "покр. номерів"),
 ("cubierta hab,", "покрівля номерів"), ("cubierta hab.", "покрівля номерів"), ("cubierta habitaciones", "покрівля номерів"),
 ("techo PB", "стеля 1-го пов."), ("terraza / planta 1", "тераса / 2-й поверх"), ("planta 1 / terraza", "2-й поверх / тераса"),
 ("planta 1 / meseta", "2-й поверх / майданчик"), ("bloque alto / bar", "високий блок / бар"), ("bar / bloque alto", "бар / високий блок"),
 ("base del barril", "низ циліндра"), ("1ª planta hab", "1-й поверх номерів"), ("cubierta barril", "покрівля циліндра"),
 ("puerta balconera", "балконні двері"), ("habitación", "номер"), ("pasillo", "коридор"), ("balcón", "балкон"), ("núcleo", "ядро"),
 ("escalera", "сходи"), ("sube", "вгору"), ("baja", "вниз"), ("entrada", "вхід"), ("meseta", "майданчик"),
 ("restaurante", "ресторан"), ("hotel", "готель"), ("columna", "колона"), ("torre", "вежа"), ("terraza", "тераса"), ("bloque alto", "високий блок"),
 ("rampas", "пандуси"), ("rampa", "пандус"), ("cuello", "шийка"), ("tambor", "барабан"), ("banda", "засклений пояс"), ("visera", "козирок"),
 ("remate", "завершення"), ("barril", "циліндр"), ("concha", "«раковина»"), ("lamas", "ламелі"), ("aletas", "ребра"),
 ("testero", "торець"), ("chaflán", "зрізаний кут"), ("alzado", "фасад"), ("sección", "розріз"), ("secciones", "розрізи"), ("planta", "план"),
 ("ala corta", "коротке крило"), ("ala larga", "довге крило"), ("calle", "вулиця"), ("patio", "двір"), ("colindante", "сусідня"), ("edificio", "будівля"),
 ("cuña", "клин"), ("macizo", "простінок"), ("vuelo", "виліт"), ("esquina", "кут"), ("frontal", "головний"), ("bar", "бар"), ("ala", "крило"),
 ("Planta", "План"), ("res", "рест."), ("X rest.", "X рест."), ("Y hotel", "Y готель"), ("col.", "кол."), ("rest.", "рест."), ("hab.", "ном."),
 ("y", "і"), ("con", "з"), ("de la", ""), ("del", ""), ("de", ""), ("la", ""), ("el", ""), ("los", ""), ("las", ""), ("en", "у"), ("por", "через"),
]
FRASES.sort(key=lambda p: -len(p[0]))
_RX = [(re.compile(r"(?<!%s)%s(?!%s)" % (_W, re.escape(a), _W)), b) for a, b in FRASES]
_PLANTA = re.compile(r"(?<!%s)([Pp])lanta (\d)(?!\d)" % _W)
RESTOS = set()


def tr(s):
    if not ACTIVO or not s or not re.search(r"[A-Za-zÁÉÍÓÚáéíóúñ]", s): return s
    for a, b in (("ª planta hab,", "-й поверх номерів"), ("ª planta hab.", "-й поверх номерів"), ("ª hab,", "-й пов. номерів"), ("ª hab.", "-й пов. номерів")):
        s = s.replace(a, b)                                               # tras una cifra (sin límite de palabra)
    s = _PLANTA.sub(lambda m: f"{'П' if m.group(1) == 'P' else 'п'}лан {int(m.group(2)) + 1}-го поверху", s)
    for rx, b in _RX: s = rx.sub(b, s)
    s = re.sub(r"(\d) m(?![A-Za-z])", r"\1 м", s)                               # unidades: metros
    s = re.sub(r"(?<![A-Za-z])m\.(?=\s|$)", "м.", s)
    s = re.sub(r"[ \t]{2,}", " ", s).replace(" ,", ",").replace("( ", "(").strip(" ") if "\n" not in s else s
    for w in re.findall(r"(?<![A-Za-zÁÉÍÓÚáéíóúñ])[A-Za-zÁÉÍÓÚáéíóúñ]{3,}", s):
        if w not in ("Google", "Maps", "ALAMY", "MGF", "Bing", "Booking", "cotas") and not w.isupper(): RESTOS.add(w)
    return s


def traducir(fig):
    if not ACTIVO or getattr(fig, "_uk", False): return
    tit = getattr(fig, "_titulo", "") + " " + (fig.texts[0].get_text() if fig.texts else "")
    if any(k in tit.upper() for k in ("CUADRO DE COTAS", "COHERENCIA")): return     # anexos técnicos (tablas): se dejan en español
    for t in fig.findobj(Text):
        t.set_text(tr(t.get_text()))
    fig._uk = True


_sf = Figure.savefig
def _savefig(self, *a, **k):
    traducir(self); return _sf(self, *a, **k)
Figure.savefig = _savefig
_ps = PdfPages.savefig
def _pdfsave(self, figure=None, **k):
    import matplotlib.pyplot as plt
    f = figure if isinstance(figure, Figure) else (plt.figure(figure) if figure is not None else plt.gcf())
    traducir(f); return _ps(self, figure, **k)
PdfPages.savefig = _pdfsave
import atexit
atexit.register(lambda: open("TRADUCCION_RESTOS.txt", "a").write("".join(w + "\n" for w in sorted(RESTOS))) if RESTOS else None)
