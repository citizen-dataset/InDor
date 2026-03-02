
spans_detection_zero_shot_en = """You are a framing and language bias expert. Your job is to analyze news excerpts and identify text spans that may be misleading, biased, speculative, emotionally charged or problematic.

TASK
- Identify only unique, non-overlapping spans that could affect reader perception.
- If no spans are found, write "No"

PROBLEMATIC SPANS INCLUDE:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual
OUTPUT FORMAT (strict):
If ONE span:
<SPANS>: ["..."]

If MULTIPLE spans:
<SPANS>: ["...", "..."]

If no spans:
<SPANS>: ["No"]

**Now process the following input:**
{instance}

Return answer with ONLY ONE <SPANS> block. Do NOT return multiple blocks. Do NOT repeat spans already listed. Ensure formatting is strictly followed. Do not add explanations.
"""


spans_detection_few_shots_en = """You are a framing and language bias expert. Your job is to analyze news excerpts and identify text spans that may be misleading, biased, speculative, emotionally charged or problematic.

TASK
- Identify only unique, non-overlapping spans that could affect reader perception.
- If no spans are found, write "No"

PROBLEMATIC SPANS INCLUDE:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual
OUTPUT FORMAT (strict):
If ONE span:
<SPANS>: ["..."]

If MULTIPLE spans:
<SPANS>: ["...", "..."]

If no spans:
<SPANS>: ["No"]

Return ONLY ONE <SPANS> block. Do NOT return multiple blocks. Do NOT repeat spans already listed. Ensure formatting is strictly followed.

Example 1 (for reference only — do NOT copy this):

TITLE: Ben Shapiro: What the latest stupid government shutdown means  
SENTENCE_0: The population is addicted to the notion that the government operates without the bumps and breaks uniquely built into the American system; the media are addicted to the daily show of government; the members of government are happy to keep spending cash and scare the life out of constituents when the spending stops.  
SENTENCE_1: We also have been trained for years that the power of the purse is in the hands of the Congress, not the executive.  
SENTENCE_2: That means we see the Congress as the party most responsible for passing legislation the president will sign, not the president as the party most responsible for agreeing with Congress.  
<SPANS>: ["stupid"]

Example 2 (for reference only — do NOT copy this):

TITLE: New York Times : "The Pentagon's Mysterious UFO Program" (plus DeLonge's new website/videos)
SENTENCE 1: it isn't that USA is backward about it - it's pretending to be, while sitting on information that will change the world when released.the only question is - apart from "when will it be released", but judging by the article, not that far away - is Mr Bigelow just a scapegoat to be used to prepare the public for the real deal, or is he aware of the truth and it's all just smoke and mirrors he went through knowingly.
SENTENCE 2: they were given some money and allowed to do some research, because that way they were kept under control.
SENTENCE 3: after they've found some tidbits of sensitive information, their request to classify it further was denied.
<SPANS>: [ "it isn't that USA is backward about it - it's pretending to be, while sitting on information that will change the world", "scapegoat", "they were given some money and allowed to do some research, because that way they were kept under control" ]

Now analyze the following input and return ONLY the final <SPANS> output:
{instance}

Return answer with ONLY ONE <SPANS> block. Do NOT return multiple blocks. Do NOT repeat spans already listed. Ensure formatting is strictly followed. Do not add explanations.
"""


rationales_generation_zero_shot_en = """You are an expert in discourse framing and media bias. Your task is to explain why certain spans of text in a news excerpt may be misleading, biased, or problematic.

You are given:
1. A news excerpt with:
   - One TITLE line
   - Three SENTENCE lines (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. A list of exact spans extracted from that text.

Your goal is to generate **one rationale for each span**. Use this strict format:
→ "if [reference to the span in the text], then [implication or consequence]"

A span is problematic if it:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual

These Output Instructions must strictly followed:
- If spans are present, return one rationale per span, matching their order exactly
- If <SPANS>: ["No"], then return <RATIONALES>: ["No"]
- Do not generate a rationale if <SPANS>: ["No"]
- Each rationale must be wrapped in double quotes ("rationale1", "rationale2", ...)
- All rationales must be returned in a single <RATIONALES> list, matching the order of the spans and separating with a comma(,)
- Do not add ellipses or extra quotes inside the rationale (no "...if" or "...")
- Do not repeat spans or return any explanation outside the output block
- Do not skip or combine spans
- Do not explain your output — only return the formatted result below:

<RATIONALES>: ["if ..., then ...", "if ..., then ...", "..."]

News Excerpt: {instance}

Spans: {spans}

Now return final answer with <RATIONALES> tag, and No explanation"""



rationales_generation_few_shots_en = """You are an expert in discourse framing and media bias. Your task is to explain why certain spans of text in a news excerpt may be misleading, biased, or problematic.

You are given:
1. A news excerpt with:
   - One TITLE line
   - Three SENTENCE lines (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. A list of exact spans extracted from that text.

Your goal is to generate **one rationale for each span**. Use this strict format:
→ "if [reference to the span in the text], then [implication or consequence]"

A span is problematic if it:
- Describes or refers to events in a way that downplays or distorts responsibility (eventive bias)
- Describes or refers to people using emotionally charged, stereotypical, or exaggerated language (attributive bias)
- Sensationalizes or exaggerates facts
- Uses vague or speculative statements as if they are factual

These Output Instructions must strictly followed:
- If spans are present, return one rationale per span, matching their order exactly
- If <SPANS>: ["No"], then return <RATIONALES>: ["No"]
- Do not generate a rationale if <SPANS>: ["No"]
- Each rationale must be wrapped in double quotes ("rationale1", "rationale2", ...)
- All rationales must be returned in a single <RATIONALES> list, matching the order of the spans and separating with a comma(,)
- Do not add ellipses or extra quotes inside the rationale (no "...if" or "...")
- Do not repeat spans or return any explanation outside the output block
- Do not skip or combine spans
- Do not explain your output — only return the formatted result below:

<RATIONALES>: ["if ..., then ...", "if ..., then ...", "..."]

Example 1 (for reference only — do NOT copy this):

Input:

News Excerpt:
TITLE: Water Scarcity: Cooperation or Conflict in the Middle East and North Africa?
SENTENCE 1: Water-sharing agreements governing shared resources such as the Nile are the way forward for the MENA region in order to avoid hydrological poverty and the harsh economic and human consequences this entails, especially as the gap between supply and demand widens in the future.
SENTENCE 2: This is the case for example for the Mountain Aquifer, the 1995 Oslo II interim agreement—which also defined the water-sharing arrangements between Palestine and Israel—came to consolidate the Israeli control that had been in place since 1967: Israel was granted access to over 71 percent of the aquifer water, while Palestinians were only granted 17 percent.
SENTENCE 3: Resources in the West Bank, for example, include the Jordan River, which runs all along the eastern border of the West Bank, and the Mountain Aquifer underlying the West Bank and Israel.

Spans: [ "Nile are the way forward for the MENA region", "Israel was granted access to over 71 percent of the aquifer water, while Palestinians were only granted 17 percent." ]

Output:
<RATIONALES>: [ "If you describe Nile as a way forward for the MENA region, then you said that Nile is only used for that" , "If the water-sharing agreement is described as consolidating Israeli control, then it implies an imbalance in resource distribution that favors Israel" ]

Example 2 (for reference only — do NOT copy this):

Input:

News Excerpt:
TITLE: Why Have There Been So Many Trans Murders This Year?
SENTENCE 1: Mere days into 2017, Sioux Falls, South Dakota, police only found the body of 28-year-old transgender woman Jamie Lee Wounded Arrow because, as KSFY reported, “a neighbor reported a strong odor coming from the apartment.” Just days prior, police in Madison County, Mississippi, had found 41-year-old Mesha Caldwell, a transgender hair and makeup artist, dead on the side of a rural road outside of Jackson, as Mississippi News Now reported.
SENTENCE 2: And that pisses me off as an elder.” The stories of these seven deaths are indeed all the more tragic for the youth of the victims—and for the sheer brutality with which their lives were discarded.
SENTENCE 3: “It results in not only the delayed recognition and response in the trans community of us honoring our last trans sisters, it is disrespectful to their memory and can delay justice in these cases,” the statement read.

Spans: [ "transgender" ]

Output:
<RATIONALES>: [ "If the term transgender woman is used to describe, then it serves to affirm her identity and highlight that the violence against her may be linked to anti-transgender discrimination" ]


Now process the following input:

News Excerpt: {instance}

Spans: {spans}

Now return final answer with <RATIONALES> tag, and No explanation"""


spans_detection_zero_shot_it = """Sei un esperto di framing e bias linguistici. Il tuo compito è analizzare estratti di notizie e identificare span di testo che possono essere fuorvianti, di parte, speculativi, emotivamente carichi o problematici.
TASK
Identifica solo span unici e non sovrapposti che potrebbero influenzare la percezione del lettore.
Se non vengono trovati span, scrivi "No"

GLI SPAN PROBLEMATICI INCLUDONO:
Descrivere o riferirsi a eventi in modo da minimizzare o distorcere le responsabilità (bias eventivo)
Descrivere o riferirsi a persone usando un linguaggio emotivamente carico, stereotipato o esagerato (bias attributivo)
Sensazionalizzare o esagerare i fatti
Usare affermazioni vaghe o speculative come se fossero fattuali

FORMATO DI OUTPUT (rigido):
Se C'È UNO span:
<SPANS>: ["..."]
Se CI SONO PIÙ span:
<SPANS>: ["...", "..."]
Se NON ci sono span:
<SPANS>: ["No"]

**Ora elabora il seguente input**:
{instance}
La risposta deve contenere un solo blocco <SPANS>. NON restituire più blocchi. NON ripetere gli span già elencati. Assicurati che il formato sia seguito rigorosamente. NON aggiungere spiegazioni.
"""

spans_detection_few_shots_it = """Sei un esperto di framing e bias linguistici. Il tuo compito è analizzare estratti di notizie e identificare gli span di testo che possono essere fuorvianti, di parte, speculativi, emotivamente carichi o problematici.
TASK
Identifica solo span unici e non sovrapposti che potrebbero influenzare la percezione del lettore.
Se non vengono trovati span, scrivi "No"

GLI SPAN PROBLEMATICI INCLUDONO:
Descrivere o riferirsi a eventi in modo da minimizzare o distorcere le responsabilità (bias eventivo)
Descrivere o riferirsi a persone usando un linguaggio emotivamente carico, stereotipato o esagerato (bias attributivo)
Sensazionalizzare o esagerare i fatti
Usare affermazioni vaghe o speculative come se fossero fattuali

FORMATO DI OUTPUT (rigido):
Se C'È UNO span:
<SPANS>: ["..."]
Se CI SONO PIÙ span:
<SPANS>: ["...", "..."]
Se NON ci sono span:
<SPANS>: ["No"]
La risposta deve contenere un solo blocco <SPANS>. NON restituire più blocchi. NON ripetere gli span già elencati. Assicurati che il formato sia seguito rigorosamente. NON aggiungere spiegazioni.

Example 1 (for reference only — do NOT copy this):

TITLE: ESTERI - Notizie 24 ore
SENTENCE_0: La recente politica estera degli Stati Uniti sotto la guida del presidente Donald Trump sta suscitando preoccupazioni...
SENTENCE_1: Negli ultimi giorni, l’Unione Europea ha segnato una svolta significativa nella sua politica di difesa, con l’intento...
SENTENCE_2: Durante un incontro ufficiale con il Primo Ministro irlandese Micheál Martin, il Presidente degli Stati Uniti Donald...
<SPANS>: ["recente politica estera degli Stati Uniti sotto la guida del presidente Donald Trump sta suscitando preoccupazioni"]

Example 2 (for reference only — do NOT copy this):

TITLE: Il papa del battesimo di Satana – RENOVATIO 21
SENTENCE_0: Crediamo sia impossibile che al papa nessuno abbia spiegato che viviamo in un mondo in cui sono proprio i ricchi – Bill Gates e i suoi enti come la Fondazione, il GAVI, il CEPI – a voler vaccinare subito i poveri, e vien da pensare – pensando alla storia del cammello e della cruna nell’ago – che non lo facciano per guadagnarsi il Regno dei Cieli (a cui non credono), ma per altri motivi indicibili; il primo che viene da pensare: perché i poveri non oppongono resistenza, è ideale quindi partire da loro…
SENTENCE_1: Dopo anni di indagini al rallentatore, e insabbiamenti, e censure, possiamo dire che colpe della Cina della pandemia possono apparire «mitigate» dal fatto che l’operazione di Gain of Function all’Istituto di Virologia di Wuhano sia stata finanziata in larga parte, se non interamente, dalla Sanità americana e in particolare da Anthony Fauci, chissà perché graziato nelle ultime ore dell’amministrazione Biden.
SENTENCE_2: Non sorprende che il capo della chiesa che ha abbandonato i sacramenti (chiudendo le chiese, privando il popolo dell’Eucarestia, piazzando l’amuchina idrogel nelle acquasantiere) voglia ora sostituire il battesimo cristiano con il «battesimo laico» – quando, a dirla fuori dai denti, «laico» è spessissimo una parola foglia di fico per non dire «massonico».
<SPANS>: ["possiamo dire che colpe della Cina della pandemia possono apparire «mitigate» dal fatto che l’operazione di Gain of Function all’Istituto di Virologia di Wuhano sia stata finanziata in larga parte, se non interamente, dalla Sanità americana e in particolare da Anthony Fauci, chissà perché graziato nelle ultime ore dell’amministrazione Biden", "Non sorprende che il capo della chiesa che ha abbandonato i sacramenti (chiudendo le chiese, privando il popolo dell’Eucarestia, piazzando l’amuchina idrogel nelle acquasantiere) voglia ora sostituire il battesimo cristiano con il «battesimo laico» – quando, a dirla fuori dai denti, «laico» è spessissimo una parola foglia di fico per non dire «massonico"]

Ora elabora il seguente input e restituisci solo il blocco finale <SPANS>:
{instance}
La risposta deve contenere un solo blocco <SPANS>. Non restituire più blocchi. Non ripetere gli stessi span già elencati. Rispetta rigorosamente il formato richiesto. Non aggiungere spiegazioni.
"""

rationales_generation_zero_shot_it = """Sei un esperto in framing discorsivo e bias nei media. Il tuo compito è spiegare perché certi span di testo in un estratto di notizia possono essere fuorvianti, di parte o problematici.

TI VIENE FORNITO:
Un estratto di notizia con:
Una riga contenente il TITOLO
Tre righe contenenti frasi (SENTENCE_0, SENTENCE_1, SENTENCE_2)
Una lista di span esatti estratti da quel testo.

Il tuo obiettivo è generare **una sola razionale per ogni span**. Usa questo formato rigido:
→ "se [riferimento allo span nel testo], allora [implicazione o conseguenza]"
Uno span è problematico se:
Descrive o riferisce eventi minimizzando o distorcendo le responsabilità (bias eventivo)
Descrive o riferisce persone usando un linguaggio carico, stereotipato o esagerato (bias attributivo)
Sensazionalizza o esagera i fatti
Usa affermazioni vaghe o speculative come se fossero fattuali

ISTRUZIONI DI OUTPUT (seguile rigorosamente):
Se sono presenti span, restituisci una razionale per ciascuno, nell’ordine esatto
Se <SPANS>: ["No"], allora restituisci <RATIONALES>: ["No"]
NON generare razionali se <SPANS>: ["No"]
Ogni razionale deve essere racchiusa tra virgolette doppie ("rationale1", "rationale2", ...)
Tutte le razionali devono essere restituite in un’unica lista <RATIONALES>, seguendo l’ordine degli span e separandoli con una virgola (,)
Non aggiungere puntini di sospensione o virgolette annidate nella razionale (no “…se” o “…”)
Non ripetere span 
NON combinare span o razionali
NON spiegare il tuo output – restituisci solo il risultato formattato qui sotto:
<RATIONALES>: ["se ..., allora ...", "se ..., allora ...", "..."]

Estratto di notizia: 
{instance}

Spans: {spans}

Ora restituisci la risposta finale con il tag <RATIONALES>, senza spiegazioni.
"""

rationales_generation_few_shots_it = """Sei un esperto in framing discorsivo e bias nei media. Il tuo compito è spiegare perché certi span di testo in un estratto di notizia possono essere fuorvianti, di parte/con bias o problematici.

TI VIENE FORNITO:
Un estratto di notizia con:
Una riga contenente il TITOLO
Tre righe contenenti frasi (SENTENCE_0, SENTENCE_1, SENTENCE_2)
Una lista di span esatti estratti da quel testo.

Il tuo obiettivo è generare **una sola razionale per ogni span**. Usa questo formato rigido:
→ "se [riferimento allo span nel testo], allora [implicazione o conseguenza]"
Uno span è problematico se:
Descrive o riferisce eventi minimizzando o distorcendo le responsabilità (bias eventivo)
Descrive o riferisce persone usando un linguaggio carico, stereotipato o esagerato (bias attributivo)
Sensazionalizza o esagera i fatti
Usa affermazioni vaghe o speculative come se fossero fattuali

ISTRUZIONI DI OUTPUT (seguile rigorosamente):
Se sono presenti span, restituisci UNA razionale per ciascuno, nell’ordine esatto
Se <SPANS>: ["No"], allora restituisci <RATIONALES>: ["No"]
NON generare razionali se <SPANS>: ["No"]
Ogni razionale deve essere racchiusa tra virgolette doppie ("rationale1", "rationale2", ...)
Tutte le razionali devono essere restituite in un’unica lista <RATIONALES>, seguendo l’ordine degli span e separandoli con una virgola (,)
Non usare puntini di sospensione o virgolette annidate nella razionale (no “…se” o “…”
Non ripetere gli span già e non restituire spiegazioni fuori dal blocco di output
Non saltare e non combinare gli span
Non spiegare il tuo output – restituisci solo il risultato formattato qui sotto:
<RATIONALES>: ["se ..., allora ...", "se ..., allora ...", "..."]

Example 1 (for reference only — do NOT copy this):

Input: 

Estratto di notizia:
TITLE: ESTERI - Notizie 24 ore
SENTENCE_0: La recente politica estera degli Stati Uniti sotto la guida del presidente Donald Trump sta suscitando preoccupazioni...
SENTENCE_1: Negli ultimi giorni, l’Unione Europea ha segnato una svolta significativa nella sua politica di difesa, con l’intento...
SENTENCE_2: Durante un incontro ufficiale con il Primo Ministro irlandese Micheál Martin, il Presidente degli Stati Uniti Donald...

Spans: ["recente politica estera degli Stati Uniti sotto la guida del presidente Donald Trump sta suscitando preoccupazioni"]

Output:
<RATIONALES>: ["Se dici che la cosa provoca preoccupazioni, dovresti specificare in chi le sta provocando."]

Example 2 (for reference only — do NOT copy this):

Input: 

Estratto di notizia:
TITLE: Il papa del battesimo di Satana – RENOVATIO 21
SENTENCE_0: Crediamo sia impossibile che al papa nessuno abbia spiegato che viviamo in un mondo in cui sono proprio i ricchi – Bill Gates e i suoi enti come la Fondazione, il GAVI, il CEPI – a voler vaccinare subito i poveri, e vien da pensare – pensando alla storia del cammello e della cruna nell’ago – che non lo facciano per guadagnarsi il Regno dei Cieli (a cui non credono), ma per altri motivi indicibili; il primo che viene da pensare: perché i poveri non oppongono resistenza, è ideale quindi partire da loro…
SENTENCE_1: Dopo anni di indagini al rallentatore, e insabbiamenti, e censure, possiamo dire che colpe della Cina della pandemia possono apparire «mitigate» dal fatto che l’operazione di Gain of Function all’Istituto di Virologia di Wuhano sia stata finanziata in larga parte, se non interamente, dalla Sanità americana e in particolare da Anthony Fauci, chissà perché graziato nelle ultime ore dell’amministrazione Biden.
SENTENCE_2: Non sorprende che il capo della chiesa che ha abbandonato i sacramenti (chiudendo le chiese, privando il popolo dell’Eucarestia, piazzando l’amuchina idrogel nelle acquasantiere) voglia ora sostituire il battesimo cristiano con il «battesimo laico» – quando, a dirla fuori dai denti, «laico» è spessissimo una parola foglia di fico per non dire «massonico».

Spans: ["possiamo dire che colpe della Cina della pandemia possono apparire «mitigate» dal fatto che l’operazione di Gain of Function all’Istituto di Virologia di Wuhano sia stata finanziata in larga parte, se non interamente, dalla Sanità americana e in particolare da Anthony Fauci, chissà perché graziato nelle ultime ore dell’amministrazione Biden", "Non sorprende che il capo della chiesa che ha abbandonato i sacramenti (chiudendo le chiese, privando il popolo dell’Eucarestia, piazzando l’amuchina idrogel nelle acquasantiere) voglia ora sostituire il battesimo cristiano con il «battesimo laico» – quando, a dirla fuori dai denti, «laico» è spessissimo una parola foglia di fico per non dire «massonico"]

Output:
<RATIONALES>: ["Se l'autore parla con tanta certezza, allora si capisce che alcune pandemie acadute nel mondo risultano in larga parte del finanziamento dell'America. ", "Se si riferisce al papa come capo della chiesa avendo abbandonato la giustizia, allora si capisce che tutte le chiese hanno perso la direzione. Non c\'è più una degna di fiducia visto che il capo invece di difendere i diritti di ciò che è scritto, i sacramenti, li ha sostituiti con un modello "massonico". "]

Ora elabora il seguente input:
Estratto di notizia: {instance}
Spans: {spans}
Ora restituisci la risposta finale con il tag <RATIONALES>, senza spiegazioni.
"""


spans_detection_zero_shot_es = """Eres experto en encuadrar eventos y identificar sesgo lingüístico. Tu trabajo consiste en analizar fragmentos de noticias e identificar fragmentos de texto que puedan ser engañosos, sesgados, especulativos, con carga emocional o problemáticos.

TAREA
- Identifique únicamente los intervalos únicos y no superpuestos que podrían afectar la percepción del lector.
- Si no se encuentran intervalos, escriba "No".

UNA PORCIÓN DE TEXTO PROBLEMÁTICA PUEDE:
- Describir o referirse a eventos de una manera que minimiza o distorsiona la responsabilidad (sesgo eventivo).
- Describir o referirse a personas utilizando un lenguaje emocionalmente cargado, estereotipado o exagerado (sesgo atributivo).
- Sensacionalizar o exagerar los hechos.
- Utilizar afirmaciones vagas o especulativas como si fueran hechos.
FORMATO DE SALIDA (estricta):
Si UNA porción de texto identificada:
<SPANS>: ["..."]

Si MUCHAS porciones de texto identificadas:
<SPANS>: ["...", "..."]

Si NINGUNA porción de texto identificada:
<SPANS>: ["No"]

**Ahora procese la siguiente entrada:**
{instance}

Devuelva la respuesta con un solo bloque <SPANS>. No devuelva varios bloques. No repita los intervalos ya listados. Asegúrese de seguir estrictamente el formato. No añada explicaciones.
"""

spans_detection_few_shots_es = """Eres experto en encuadrar eventos y identificar sesgo lingüístico. Tu trabajo consiste en analizar fragmentos de noticias e identificar fragmentos de texto que puedan ser engañosos, sesgados, especulativos, con carga emocional o problemáticos.

TAREA
- Identifique únicamente los intervalos únicos y no superpuestos que podrían afectar la percepción del lector.
- Si no se encuentran intervalos, escriba "No".

UNA PORCIÓN DE TEXTO PROBLEMÁTICA PUEDE:
- Describir o referirse a eventos de una manera que minimiza o distorsiona la responsabilidad (sesgo eventivo).
- Describir o referirse a personas utilizando un lenguaje emocionalmente cargado, estereotipado o exagerado (sesgo atributivo).
- Sensacionalizar o exagerar los hechos.
- Utilizar afirmaciones vagas o especulativas como si fueran hechos.
FORMATO DE SALIDA (estricta):
Si UNA porción de texto identificada:
<SPANS>: ["..."]

Si MUCHAS porciones de texto identificadas:
<SPANS>: ["...", "..."]

Si NINGUNA porción de texto identificada:
<SPANS>: ["No"]

Devuelva la respuesta con un solo bloque <SPANS>. No devuelva varios bloques. No repita los intervalos ya listados. Asegúrese de seguir estrictamente el formato. No añada explicaciones.

Ejemplo 1 (sólo como referencia — NO copiar esto):
TITLE: EXCLUSIVA: Redadas, humillaciones y riesgo de cárcel: así actúa la Policía contra el colectivo LGTBIQ+ con la excusa de las drogas y el 'chemsex' | Público
SENTENCE_0: No es nuevo que la Policía vigile, registre y persiga a quienes se salen del estrecho imperativo de la heteronorma: pasó en Stonewall en 1969, cuando un grupo de personas trans, "maricas" y lesbianas de Nueva York dijeron "basta" a las redadas en sus bares; ocurrió en la España franquista, cuando ser homosexual podía llevarte a la cárcel bajo la Ley de Peligrosidad y Rehabilitación Social; y, según denuncian cada vez más voces, parece que sigue sucediendo en discotecas, saunas o en plena calle –también de grandes y presuntamente transgresoras metrópolis como Madrid–.
SENTENCE_1: Un fin de semana, mientras participaba en una sesión de chemsex (práctica consiste en mantener relaciones sexuales en un ambiente de consumo de sustancias psicoactivas), recibió la dirección de otra reunión: "Nos habían enviado la dirección de esta otra sesión a través de una aplicación de citas y nos habían dicho que pilláramos dos gramos de tina (metanfetamina)", explica.
SENTENCE_2: Además del enjuiciamiento, denuncia un "patrón de actuación policial" dirigido específicamente contra los "maricas" –uno de los términos que utilizan para autorreferenciarse dentro del colectivo– en Madrid, en particular contra quienes practican chemsex: "Nos están manipulando, están jugando con nuestras vidas y con nuestra intimidad para conseguir hacer detenciones a mansalva".
<SPANS>: ["No es nuevo que la Policía vigile, registre y persiga a quienes se salen del estrecho imperativo de la heteronorma: pasó en Stonewall en 1969, cuando un grupo de personas trans, 'maricas' y lesbianas de Nueva York dijeron 'basta' a las redadas en sus bares; ocurrió en la España franquista, cuando ser homosexual podía llevarte a la cárcel bajo la Ley de Peligrosidad y Rehabilitación Social; y, según denuncian cada vez más voces, parece que sigue sucediendo en discotecas, saunas o en plena calle –también de grandes y presuntamente transgresoras metrópolis como Madrid"]

Ejemplo 2 (sólo como referencia — NO copiar esto):
TITLE: Cárteles en México reclutan estudiantes de química para fabricar fentanilo
SENTENCE_0: Según investigaciones del prestigioso medio, los cárteles cuentan con reclutadores en universidades de México, donde ofrecen a estudiantes con excelencia académica grandes sumas de dinero para que desarrollen fórmulas de fentanilo.
SENTENCE_1: Con el objetivo de fabricar fentanilo con dosis más potentes, los cárteles mexicanos han comenzado a reclutar a jóvenes estudiantes de química con excelencia académica de las universidades, según The New York Times (NYT).
SENTENCE_2: Cocineros de fentanilo que trabajan para el Cártel de Sinaloa han declarado al periódico estadounidense que necesitan trabajadores con conocimientos avanzados de química para ayudar en la producción de la droga.
<SPANS>: ["Según investigaciones del prestigioso medio"]

Ahora analice la siguiente entrada y devuelva SÓLO la salida final <SPANS>:
{instance}

Devuelva la respuesta con un solo bloque <SPANS>. No devuelva varios bloques. No repita los intervalos ya listados. Asegúrese de seguir estrictamente el formato. No añada explicaciones.
"""

rationales_generation_zero_shot_es = """Eres experto en encuadrar eventos y identificar sesgo lingüístico. Tu trabajo consiste en explicar por qué ciertos fragmentos de texto en un extracto de noticias pueden ser engañosos, sesgados o problemáticos.

Se le proporciona:
1. Un extracto de noticia con:
- Una línea de TITLE 
Tres líneas de SENTENCE (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. Una lista de los períodos exactos extraídos de ese texto.

El objetivo es generar **una justificación para cada período**. Utilice este formato estricto:
→ "si [referencia al período en el texto], entonces [implicación o consecuencia]"

Un período es problemático si:
- Describe o se refiere a eventos de una manera que minimiza o distorsiona la responsabilidad (sesgo eventivo).
- Describe o se refiere a personas utilizando un lenguaje emocionalmente cargado, estereotipado o exagerado (sesgo atributivo).
- Sensacionaliza o exagera los hechos.
- Utiliza afirmaciones vagas o especulativas como si fueran factuales.

Estas instrucciones de salida deben seguirse estrictamente:
- Si hay intervalos, devolver una justificación por intervalo, siguiendo exactamente su orden.
- Si <SPANS>: ["No"], devolver <RATIONALES>: ["No"].
- No generar una justificación si <SPANS>: ["No"].
- Cada justificación debe ir entre comillas dobles ("razonamiento1", "razonamiento2", ...).
- Todas las justificaciones deben devolverse en una sola lista <RAZONES>, siguiendo el orden de los intervalos y separándolas con una coma (,).
- No añadir puntos suspensivos ni comillas adicionales dentro de la justificación (no usar "...si" ni "...").
- No repetir intervalos ni devolver ninguna explicación fuera del bloque de salida.
- No omitir ni combinar intervalos.
- No explicar la salida; solo devolver el resultado formateado a continuación.

<RATIONALES>: ["si ..., entonces...", "si ..., entonces ...", "..."]

Extracto de noticias: 
{instance}

Porciones de texto: {spans}

Ahora devuelve la respuesta final con la etiqueta <RATIONALES> y sin explicación.
"""

rationales_generation_few_shots_es = """Eres experto en encuadrar eventos y identificar sesgo lingüístico. Tu trabajo consiste en explicar por qué ciertos fragmentos de texto en un extracto de noticias pueden ser engañosos, sesgados o problemáticos.

Se le proporciona:
1. Un extracto de noticia con:
- Una línea de TITLE 
- Tres líneas de SENTENCE (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. Una lista de los períodos exactos extraídos de ese texto.

El objetivo es generar **una justificación para cada período**. Utilice este formato estricto:
→ "si [referencia al período en el texto], entonces [implicación o consecuencia]"

Un período es problemático si:
- Describe o se refiere a eventos de una manera que minimiza o distorsiona la responsabilidad (sesgo eventivo).
- Describe o se refiere a personas utilizando un lenguaje emocionalmente cargado, estereotipado o exagerado (sesgo atributivo).
- Sensacionaliza o exagera los hechos.
- Utiliza afirmaciones vagas o especulativas como si fueran factuales.

Estas instrucciones de salida deben seguirse estrictamente:
- Si hay intervalos, devolver una justificación por intervalo, siguiendo exactamente su orden.
- Si <SPANS>: ["No"], devolver <RATIONALES>: ["No"].
- No generar una justificación si <SPANS>: ["No"].
- Cada justificación debe ir entre comillas dobles ("razonamiento1", "razonamiento2", ...).
- Todas las justificaciones deben devolverse en una sola lista <RAZONES>, siguiendo el orden de los intervalos y separándolas con una coma (,).
- No añadir puntos suspensivos ni comillas adicionales dentro de la justificación (no usar "...si" ni "...").
- No repetir intervalos ni devolver ninguna explicación fuera del bloque de salida.
- No omitir ni combinar intervalos.
- No explicar la salida; solo devolver el resultado formateado a continuación.

<RATIONALES>: ["si ..., entonces...", "si ..., entonces ...", "..."]

Ejemplo 1 (sólo como referencia — NO copiar esto):

Input:

Extracto de noticias:
TITLE: EXCLUSIVA: Redadas, humillaciones y riesgo de cárcel: así actúa la Policía contra el colectivo LGTBIQ+ con la excusa de las drogas y el 'chemsex' | Público
SENTENCE_0: No es nuevo que la Policía vigile, registre y persiga a quienes se salen del estrecho imperativo de la heteronorma: pasó en Stonewall en 1969, cuando un grupo de personas trans, "maricas" y lesbianas de Nueva York dijeron "basta" a las redadas en sus bares; ocurrió en la España franquista, cuando ser homosexual podía llevarte a la cárcel bajo la Ley de Peligrosidad y Rehabilitación Social; y, según denuncian cada vez más voces, parece que sigue sucediendo en discotecas, saunas o en plena calle –también de grandes y presuntamente transgresoras metrópolis como Madrid–.
SENTENCE_1: Un fin de semana, mientras participaba en una sesión de chemsex (práctica consiste en mantener relaciones sexuales en un ambiente de consumo de sustancias psicoactivas), recibió la dirección de otra reunión: "Nos habían enviado la dirección de esta otra sesión a través de una aplicación de citas y nos habían dicho que pilláramos dos gramos de tina (metanfetamina)", explica.
SENTENCE_2: Además del enjuiciamiento, denuncia un "patrón de actuación policial" dirigido específicamente contra los "maricas" –uno de los términos que utilizan para autorreferenciarse dentro del colectivo– en Madrid, en particular contra quienes practican chemsex: "Nos están manipulando, están jugando con nuestras vidas y con nuestra intimidad para conseguir hacer detenciones a mansalva".
Spans: ["No es nuevo que la Policía vigile, registre y persiga a quienes se salen del estrecho imperativo de la heteronorma: pasó en Stonewall en 1969, cuando un grupo de personas trans, 'maricas' y lesbianas de Nueva York dijeron 'basta' a las redadas en sus bares; ocurrió en la España franquista, cuando ser homosexual podía llevarte a la cárcel bajo la Ley de Peligrosidad y Rehabilitación Social; y, según denuncian cada vez más voces, parece que sigue sucediendo en discotecas, saunas o en plena calle –también de grandes y presuntamente transgresoras metrópolis como Madrid"]

Output:
<RATIONALES>: ["SI se menciona únicamente casos históricos de represión policial (Stonewall 1969, España franquista) ENTONCES está construyendo una narrativa de continuidad represiva absoluta, ignorando deliberadamente posibles cambios normativos, protocolos actuales de actuación policial o contextos específicos que puedan mostrar una evolución institucional, con el objetivo de reforzar su mensaje de que la policía sigue actuando con la misma violencia sistemática sin matices ni progresos."]

Ejemplo 2 (sólo como referencia — NO copiar esto):

Input:

Extracto de noticias:
TITLE: Cárteles en México reclutan estudiantes de química para fabricar fentanilo
SENTENCE_0: Según investigaciones del prestigioso medio, los cárteles cuentan con reclutadores en universidades de México, donde ofrecen a estudiantes con excelencia académica grandes sumas de dinero para que desarrollen fórmulas de fentanilo.
SENTENCE_1: Con el objetivo de fabricar fentanilo con dosis más potentes, los cárteles mexicanos han comenzado a reclutar a jóvenes estudiantes de química con excelencia académica de las universidades, según The New York Times (NYT).
SENTENCE_2: Cocineros de fentanilo que trabajan para el Cártel de Sinaloa han declarado al periódico estadounidense que necesitan trabajadores con conocimientos avanzados de química para ayudar en la producción de la droga.
Spans: ["Según investigaciones del prestigioso medio"]

Output:
<RATIONALES>: ["SI el artículo menciona 'investigaciones del prestigioso medio' sin nombrar inicialmente al New York Times (NYT) ENTONCES está utilizando un recurso de autoridad aparente que genera credibilidad anticipada sin permitir verificación inmediata, lo que podría exagerar la percepción de rigor periodístico antes de revelar la fuente real."]


Ahora analice la siguiente entrada y devuelva SÓLO la salida final <SPANS>:

Extracto de noticias: 
{instance}
Spans: {spans}

Ahora devuelve la respuesta final con la etiqueta <RATIONALES> y sin explicación.
"""


spans_detection_zero_shot_fa = """
شما یک متخصص چارچوب‌بندی و سوگیری زبانی هستید. وظیفه شما تجزیه و تحلیل گزیده‌های خبری و شناسایی بازه‌های متنی است که ممکن است گمراه‌کننده، مغرضانه، سوداگرانه، دارای بار احساسی یا مشکل‌ساز باشند.
 وظیفه
فقط بازه‌های منحصربه‌فرد و بدون همپوشانی را شناسایی کنید که می‌توانند بر درک خواننده تأثیر بگذارند.
اگر هیچ بازه‌ای یافت نشد، "No" بنویسید.
بازه‌های مشکل‌ساز شامل موارد زیر است:
رویدادها را به گونه‌ای توصیف یا به آنها اشاره می‌کند که مسئولیت را کم‌اهمیت جلوه داده یا تحریف می‌کند (سوگیری رویدادی).
افراد را با استفاده از زبان دارای بار احساسی، کلیشه‌ای یا اغراق‌آمیز توصیف یا به آنها اشاره می‌کند (سوگیری اسنادی).
واقعیت‌ها را هیجان‌انگیز یا اغراق‌آمیز جلوه می‌دهد.
از اظهارات مبهم یا سوداگرانه به گونه‌ای استفاده می‌کند که گویی واقعی هستند.
 فرمت خروجی (دقیق):
 اگر یک بازه:
 <SPANS>: ["..."]
اگر چند بازه: 

<SPANS>: ["...", "..."]
اگر هیچ بازه‌ای وجود ندارد:
<SPANS>: ["No"]

**اکنون ورودی زیر را پردازش کن**
 {instance}
پاسخ را فقط با یک بلوک <SPANS> برگردانید. بلوک‌های متعدد را برنگردانید. بازه‌هایی را که قبلاً فهرست شده‌اند تکرار نکنید. اطمینان حاصل کنید که قالب‌بندی به دقت رعایت شده است. توضیحات اضافه نکنید. 
"""

spans_detection_few_shots_fa = """شما یک متخصص چارچوب‌بندی و سوگیری زبانی هستید. وظیفه شما تجزیه و تحلیل گزیده‌های خبری و شناسایی بازه‌های متنی است که ممکن است گمراه‌کننده، مغرضانه، سوداگرانه، دارای بار احساسی یا مشکل‌ساز باشند.
 وظیفه
فقط بازه‌های منحصربه‌فرد و بدون همپوشانی را شناسایی کنید که می‌توانند بر درک خواننده تأثیر بگذارند.
اگر هیچ بازه‌ای یافت نشد، "No" بنویسید.
بازه‌های مشکل‌ساز شامل موارد زیر است:
رویدادها را به گونه‌ای توصیف یا به آنها اشاره می‌کند که مسئولیت را کم‌اهمیت جلوه داده یا تحریف می‌کند (سوگیری رویدادی).
افراد را با استفاده از زبان دارای بار احساسی، کلیشه‌ای یا اغراق‌آمیز توصیف یا به آنها اشاره می‌کند (سوگیری اسنادی).
واقعیت‌ها را هیجان‌انگیز یا اغراق‌آمیز جلوه می‌دهد.
از اظهارات مبهم یا سوداگرانه به گونه‌ای استفاده می‌کند که گویی واقعی هستند.
 فرمت خروجی (دقیق):
 اگر یک بازه: 
<SPANS>: ["..."]
اگر چند بازه:
<SPANS>: ["...", "..."]
اگر هیچ بازه‌ای وجود ندارد: 
<SPANS>: ["No"]
فقط یک بلوک <SPANS> را برگردانید. بلوک‌های متعدد را برنگردانید. بازه‌هایی را که قبلاً فهرست شده‌اند تکرار نکنید. اطمینان حاصل کنید که قالب‌بندی به دقت رعایت شده است.

مثال ۱ (فقط جهت اطلاع — کپی نکنید):

TITLE: همشهری آنلاین - روز هفتم
SENTENCE_0: شهر تهران مساجد قدیمی بسیاری دارد که این روزها نه تنها قدمت آنها نه تنها مقصدی مناسب برای گردش در دل تاریخ به حساب می‌آیند،بلکه مکانی مناسب برای برگزاری مراسم مذهبی بوده و در ماه‌های مختلف سال ازجمله ماه رمضان میزبان پایتخت نشنینان هستند.مسجد جامع جماران درمحدوده شمالی تهران نیز یکی ازاین مساجداست.
SENTENCE_1: از تدارک افطاری ساده با همراهی اهالی محله گرفته تا گسترده شدن بساط دعا و نیایش که لحظه‌هایی پر شوری را در ذهن و جان روزه‌داران رقم می‌زند و ده‌ها برنامه دیگر در این خانه‌های خدا جریان دارد.
SENTENCE_2: نام سلیمانیه منسوب به امیر سلیمانی پسرعضدالملک رئیس ایل قاجار است.اراضی این بوستان در گذشته متعلق به روستای اصفهانک از روستاهای جنوب شرقی تهران بوده است و تا دهه های اخیر در آن کشاورزی می کردند.
<SPANS>: ["شهر تهران مساجد قدیمی بسیاری دارد که این روزها نه تنها قدمت آنها نه تنها مقصدی مناسب برای گردش در دل تاریخ به حساب می\u200cآیند،بلکه مکانی مناسب برای برگزاری مراسم مذهبی بوده و در ماه\u200cهای مختلف سال ازجمله ماه رمضان میزبان پایتخت نشنینان هستند.مسجد جامع جماران درمحدوده شمالی تهران نیز یکی ازاین مساجداست.\n"]

مثال ۲ (فقط جهت اطلاع — کپی نکنید):

TITLE: زمان اندک ایران برای ماندن در نقشه اقتصاد جهانی
SENTENCE_0: قیمت تمام‌شده آیفون‌هایی که در چین تولید می‌شوند، مثلاً 200 دلار است که این مبلغ سهم کارگر، کارخانه‌دار و دولت چین (بابت مالیات) است اما این موبایل با قیمتی هزار تا هزار و 500 دلار به فروش می‌رسد که مازاد این مبلغ به‌عنوان رانت فکری و انحصار به اپل و آمریکا برمی‌گردد؛ زیرا توسعه نرم‌افزار، طراحی محصول و انحصارهای زیرساختی در دست این کشور است.
SENTENCE_1: قنبری با انتقاد از سیاست‌های دیپلماتیک که منجر به نتایج اقتصادی نشده، می‌گوید: «بخش بزرگی از هزینه‌های دیپلماسی ایران طی سال‌های گذشته در کشور عراق خرج شد اما اگر بررسی کنید می‌بینید ایران بین شرکای تجاری کشوری مثل عراق حتی بین 10 کشور اول نیست و ترکیه بااینکه هزینه کمتری از ایران کرد، میان سه شریک اول تجاری عراق قرار دارد.»
SENTENCE_2: قنبری برای حل این مشکل نیز راه‌حلی ارائه می‌کند: «مهم‌ترین مسئله این است که بتوانید کارگزار، توزیع‌کننده یا مسئول حقوقی داشته باشید که صفرتاصد این کار را بر عهده بگیرد و بقیه هم در قبال آن پاسخگو باشند؛ یعنی اگر از سازمانی داده بخواهد، آن سازمان باید به‌راحتی این داده‌ها را ارائه کند.
<SPANS>: ["قیمت تمام\u200cشده آیفون\u200cهایی که در چین تولید می\u200cشوند، مثلاً 200 دلار است که این مبلغ سهم کارگر، کارخانه\u200cدار و دولت چین (بابت مالیات) است اما این موبایل با قیمتی هزار تا هزار و 500 دلار به فروش می\u200cرسد که مازاد این مبلغ به\u200cعنوان رانت فکری و انحصار به اپل و آمریکا برمی\u200cگردد؛ زیرا توسعه نرم\u200cافزار، طراحی محصول و انحصارهای زیرساختی در دست این کشور است.\nS", "قنبری با انتقاد از سیاست\u200cهای دیپلماتیک که منجر به نتایج اقتصادی نشده، می\u200cگوید: «بخش بزرگی از هزینه\u200cهای دیپلماسی ایران طی سال\u200cهای گذشته در کشور عراق خرج شد اما اگر بررسی کنید می\u200cبینید ایران بین شرکای تجاری کشوری مثل عراق حتی بین 10 کشور اول نیست و ترکیه بااینکه هزینه کمتری از ایران کرد، میان سه شریک اول تجاری عراق قرار دارد.»\nS", "قنبری برای حل این مشکل نیز راه\u200cحلی ارائه می\u200cکند: «مهم\u200cترین مسئله این است که بتوانید کارگزار، توزیع\u200cکننده یا مسئول حقوقی داشته باشید که صفرتاصد این کار را بر عهده بگیرد و بقیه هم در قبال آن پاسخگو باشند؛ یعنی اگر از سازمانی داده بخواهد، آن سازمان باید به\u200cراحتی این داده\u200cها را ارائه کند."]

اکنون ورودی زیر را تجزیه و تحلیل کرده و فقط خروجی نهایی <SPANS> را برگردانید:
 {instance}
پاسخ را فقط با یک بلوک <SPANS> برگردانید. بلوک‌های متعدد را برنگردانید. بازه‌هایی را که قبلاً فهرست شده‌اند تکرار نکنید. اطمینان حاصل کنید که قالب‌بندی به دقت رعایت شده است. توضیحات اضافه نکنید. 
"""

rationales_generation_zero_shot_fa = """شما یک متخصص در چارچوب‌بندی گفتمان و سوگیری رسانه‌ای هستید. وظیفه شما توضیح این است که چرا بازه‌های خاصی از متن در یک گزیده خبری ممکن است گمراه‌کننده، مغرضانه یا مشکل‌ساز باشند. به شما داده شده است: ۱. یک گزیده خبری با: - یک خط عنوان (TITLE) - سه خط جمله (SENTENCE_0، SENTENCE_1، SENTENCE_2)
۲. فهرستی از بازه‌های دقیق استخراج شده از آن متن. هدف شما تولید یک استدلال برای هر بازه است. از این فرمت دقیق استفاده کنید: → "اگر [ارجاع به بازه در متن]، آنگاه [پیامد یا نتیجه]"
یک بازه در صورتی مشکل‌ساز است که:
رویدادها را به گونه‌ای توصیف یا به آنها اشاره می‌کند که مسئولیت را کم‌اهمیت جلوه داده یا تحریف می‌کند (سوگیری رویدادی).
افراد را با استفاده از زبان دارای بار احساسی، کلیشه‌ای یا اغراق‌آمیز توصیف یا به آنها اشاره می‌کند (سوگیری اسنادی).
واقعیت‌ها را هیجان‌انگیز یا اغراق‌آمیز جلوه می‌دهد.
از اظهارات مبهم یا سوداگرانه به گونه‌ای استفاده می‌کند که گویی واقعی هستند.
این دستورالعمل‌های خروجی باید به دقت رعایت شوند:
اگر بازه‌ها موجود هستند، برای هر بازه یک استدلال برگردانید، دقیقاً با ترتیب آنها مطابقت داشته باشد.
اگر
<SPANS>: ["No"]
 آنگاه
<RATIONALES>: ["No"]
 را برگردانید.
اگر
<SPANS>: ["No"]
 استدلالی تولید نکنید.
هر استدلال باید در گیومه ("استدلال۱"، "استدلال۲"، ...) قرار گیرد.
همه استدلال‌ها باید در یک لیست <RATIONALES> منفرد برگردانده شوند، با ترتیب بازه‌ها مطابقت داشته باشند و با کاما (,) از هم جدا شوند.
سه نقطه یا گیومه‌های اضافی داخل استدلال اضافه نکنید (نه "...اگر" یا "...")
بازه‌ها را تکرار نکنید یا هیچ توضیحی خارج از بلوک خروجی برنگردانید.
بازه‌ها را رد نکنید یا ترکیب نکنید.
خروجی خود را توضیح ندهید — فقط نتیجه قالب‌بندی شده زیر را برگردانید:
<RATIONALES>: ["اگر ...، آنگاه ..."، "اگر ...، آنگاه ..."، "..."]
گزیده خبری: {instance}
بازه‌ها: {spans}
اکنون پاسخ نهایی را با تگ <RATIONALES> و بدون توضیح برگردانید.
"""

rationales_generation_few_shots_fa = """شما یک متخصص در چارچوب‌بندی گفتمان و سوگیری رسانه‌ای هستید. وظیفه شما توضیح این است که چرا بازه‌های خاصی از متن در یک گزیده خبری ممکن است گمراه‌کننده، مغرضانه یا مشکل‌ساز باشند. به شما داده شده است: ۱. یک گزیده خبری با: - یک خط عنوان (TITLE) - سه خط جمله (SENTENCE_0، SENTENCE_1، SENTENCE_2)
۲. فهرستی از بازه‌های دقیق استخراج شده از آن متن. هدف شما تولید یک استدلال برای هر بازه است. از این فرمت دقیق استفاده کنید: → "اگر [ارجاع به بازه در متن]، آنگاه [پیامد یا نتیجه]"
یک بازه در صورتی مشکل‌ساز است که:
رویدادها را به گونه‌ای توصیف یا به آنها اشاره می‌کند که مسئولیت را کم‌اهمیت جلوه داده یا تحریف می‌کند (سوگیری رویدادی).
افراد را با استفاده از زبان دارای بار احساسی، کلیشه‌ای یا اغراق‌آمیز توصیف یا به آنها اشاره می‌کند (سوگیری اسنادی).
واقعیت‌ها را هیجان‌انگیز یا اغراق‌آمیز جلوه می‌دهد.
از اظهارات مبهم یا سوداگرانه به گونه‌ای استفاده می‌کند که گویی واقعی هستند.
این دستورالعمل‌های خروجی باید به دقت رعایت شوند:
اگر بازه‌ها موجود هستند، برای هر بازه یک استدلال برگردانید، دقیقاً با ترتیب آنها مطابقت داشته باشد.
اگر
<SPANS>: ["No"]
آنگاه
<RATIONALES>: ["No"]
 را برگردانید.
<SPANS>: ["No"]
 استدلالی تولید نکنید.
هر استدلال باید در گیومه ("استدلال۱"، "استدلال۲"، ...) قرار گیرد.
همه استدلال‌ها باید در یک لیست <RATIONALES> منفرد برگردانده شوند، با ترتیب بازه‌ها مطابقت داشته باشند و با کاما (,) از هم جدا شوند.
سه نقطه یا گیومه‌های اضافی داخل استدلال اضافه نکنید (نه "...اگر" یا "...")
بازه‌ها را تکرار نکنید یا هیچ توضیحی خارج از بلوک خروجی برنگردانید.
بازه‌ها را رد نکنید یا ترکیب نکنید.
خروجی خود را توضیح ندهید — فقط نتیجه قالب‌بندی شده زیر را برگردانید:
<RATIONALES>: ["اگر ...، آنگاه ..."، "اگر ...، آنگاه ..."، "..."]

مثال ۱ (فقط جهت اطلاع — کپی نکنید):

Input:

News Excerpt:
TITLE: همشهری آنلاین - روز هفتم
SENTENCE_0: شهر تهران مساجد قدیمی بسیاری دارد که این روزها نه تنها قدمت آنها نه تنها مقصدی مناسب برای گردش در دل تاریخ به حساب می‌آیند،بلکه مکانی مناسب برای برگزاری مراسم مذهبی بوده و در ماه‌های مختلف سال ازجمله ماه رمضان میزبان پایتخت نشنینان هستند.مسجد جامع جماران درمحدوده شمالی تهران نیز یکی ازاین مساجداست.
SENTENCE_1: از تدارک افطاری ساده با همراهی اهالی محله گرفته تا گسترده شدن بساط دعا و نیایش که لحظه‌هایی پر شوری را در ذهن و جان روزه‌داران رقم می‌زند و ده‌ها برنامه دیگر در این خانه‌های خدا جریان دارد.
SENTENCE_2: نام سلیمانیه منسوب به امیر سلیمانی پسرعضدالملک رئیس ایل قاجار است.اراضی این بوستان در گذشته متعلق به روستای اصفهانک از روستاهای جنوب شرقی تهران بوده است و تا دهه های اخیر در آن کشاورزی می کردند.
Spans: ["شهر تهران مساجد قدیمی بسیاری دارد که این روزها نه تنها قدمت آنها نه تنها مقصدی مناسب برای گردش در دل تاریخ به حساب می\u200cآیند،بلکه مکانی مناسب برای برگزاری مراسم مذهبی بوده و در ماه\u200cهای مختلف سال ازجمله ماه رمضان میزبان پایتخت نشنینان هستند.مسجد جامع جماران درمحدوده شمالی تهران نیز یکی ازاین مساجداست.\n"]

Output:
<RATIONALES>: ["اگر متن صرفاً به قابلیت گردشگری مساجد قدیمی تهران اشاره کند اما:\nآمار واقعی گردشگران خارجی بازدیدکننده از این مکان\u200cها را ذکر نکند\nمشکلات زیرساختی مانند نبود تابلوهای راهنمای چندزبانه یا سرویس\u200cهای بهداشتی مناسب را نادیده بگیرد\nمحدودیت\u200cهای امنیتی برای بازدید غیرمسلمانان از بخش\u200cهای اصلی مساجد را بررسی ننماید\nپس این ادعا که «ایران مقصد گردشگری است» بیشتر شعار تبلیغاتی است تا واقعیت.\n\n"]

مثال ۱ (فقط جهت اطلاع — کپی نکنید):

Input:

News Excerpt:
TITLE: زمان اندک ایران برای ماندن در نقشه اقتصاد جهانی
SENTENCE_0: قیمت تمام‌شده آیفون‌هایی که در چین تولید می‌شوند، مثلاً 200 دلار است که این مبلغ سهم کارگر، کارخانه‌دار و دولت چین (بابت مالیات) است اما این موبایل با قیمتی هزار تا هزار و 500 دلار به فروش می‌رسد که مازاد این مبلغ به‌عنوان رانت فکری و انحصار به اپل و آمریکا برمی‌گردد؛ زیرا توسعه نرم‌افزار، طراحی محصول و انحصارهای زیرساختی در دست این کشور است.
SENTENCE_1: قنبری با انتقاد از سیاست‌های دیپلماتیک که منجر به نتایج اقتصادی نشده، می‌گوید: «بخش بزرگی از هزینه‌های دیپلماسی ایران طی سال‌های گذشته در کشور عراق خرج شد اما اگر بررسی کنید می‌بینید ایران بین شرکای تجاری کشوری مثل عراق حتی بین 10 کشور اول نیست و ترکیه بااینکه هزینه کمتری از ایران کرد، میان سه شریک اول تجاری عراق قرار دارد.»
SENTENCE_2: قنبری برای حل این مشکل نیز راه‌حلی ارائه می‌کند: «مهم‌ترین مسئله این است که بتوانید کارگزار، توزیع‌کننده یا مسئول حقوقی داشته باشید که صفرتاصد این کار را بر عهده بگیرد و بقیه هم در قبال آن پاسخگو باشند؛ یعنی اگر از سازمانی داده بخواهد، آن سازمان باید به‌راحتی این داده‌ها را ارائه کند.
Spans: ["قیمت تمام\u200cشده آیفون\u200cهایی که در چین تولید می\u200cشوند، مثلاً 200 دلار است که این مبلغ سهم کارگر، کارخانه\u200cدار و دولت چین (بابت مالیات) است اما این موبایل با قیمتی هزار تا هزار و 500 دلار به فروش می\u200cرسد که مازاد این مبلغ به\u200cعنوان رانت فکری و انحصار به اپل و آمریکا برمی\u200cگردد؛ زیرا توسعه نرم\u200cافزار، طراحی محصول و انحصارهای زیرساختی در دست این کشور است.\nS", "قنبری با انتقاد از سیاست\u200cهای دیپلماتیک که منجر به نتایج اقتصادی نشده، می\u200cگوید: «بخش بزرگی از هزینه\u200cهای دیپلماسی ایران طی سال\u200cهای گذشته در کشور عراق خرج شد اما اگر بررسی کنید می\u200cبینید ایران بین شرکای تجاری کشوری مثل عراق حتی بین 10 کشور اول نیست و ترکیه بااینکه هزینه کمتری از ایران کرد، میان سه شریک اول تجاری عراق قرار دارد.»\nS", "قنبری برای حل این مشکل نیز راه\u200cحلی ارائه می\u200cکند: «مهم\u200cترین مسئله این است که بتوانید کارگزار، توزیع\u200cکننده یا مسئول حقوقی داشته باشید که صفرتاصد این کار را بر عهده بگیرد و بقیه هم در قبال آن پاسخگو باشند؛ یعنی اگر از سازمانی داده بخواهد، آن سازمان باید به\u200cراحتی این داده\u200cها را ارائه کند."]

Output:
<RATIONALES>: ["اگر قیمت تمام\u200cشده آیفون\u200cهای تولید شده در چین و تفاوت آن با قیمت فروش تنها به رانت فکری و انحصار اپل نسبت داده شود بدون تحلیل دقیق\u200cتر از سهم عوامل دیگر مانند هزینه\u200cهای بازاریابی، توزیع و فناوری،\nپس ممکن است مخاطب تصویر ناقصی از ساختار قیمت\u200cگذاری جهانی داشته باشد و عوامل واقعی تأثیرگذار بر این تفاوت قیمت را نادیده بگیرد.", "اگر انتقاد از سیاست\u200cهای دیپلماتیک ایران در عراق صرفاً بر اساس مقایسه با ترکیه بیان شود بدون ارائه تحلیل جامع\u200cتر از روابط اقتصادی ایران و عراق یا بررسی عوامل تأثیرگذار بر کاهش نقش ایران در بازار عراق،\n\nپس ممکن است مخاطب نتواند به\u200cطور دقیق دلایل کاهش سهم ایران در تجارت عراق را درک کند.\n\n", "اگر راه\u200cحل پیشنهادی برای بهبود شرایط اقتصادی ایران تنها بر داشتن یک کارگزار یا مسئول حقوقی متمرکز شود بدون تحلیل جامع\u200cتر از چالش\u200cهای نهادی، اداری و زیرساختی،\nپس ممکن است مخاطب این راه\u200cحل را بیش از حد ساده\u200cسازی شده تلقی کند و درک درستی از پیچیدگی\u200cهای اجرایی آن نداشته باشد."]

اکنون ورودی زیر را پردازش کنید:
گزیده خبری: 
{instance}
بازه‌ها: {spans}

اکنون پاسخ نهایی را با تگ <RATIONALES>: و بدون توضیح برگردانید.
"""



spans_detection_zero_shot_nl = """Je bent een expert op het gebied van framing en taal bias. Je taak is om nieuwsfragmenten te analyseren en tekstfragmenten te identificeren die misleidend, bevooroordeeld, speculatief, emotioneel geladen of problematisch kunnen zijn.

TAAK
- Identificeer alleen unieke, niet-overlappende tekstfragmenten die de perceptie van de lezer kunnen beïnvloeden.
- Als er geen tekstfragmenten zijn gevonden, schrijf dan "Nee".


PROBLEMATISCHE TEKSTFRAGMENTEN ZIJN ONDER ANDERE:
- Beschrijft of verwijst naar gebeurtenissen op een manier die de verantwoordelijkheid bagatelliseert of vervormt (eventive bias).
- Beschrijft of verwijst naar mensen met behulp van emotioneel geladen, stereotype of overdreven taal (attributieve bias)
- Sensationaliseert of overdrijft feiten
- Gebruikt vage of speculatieve uitspraken alsof ze feitelijk zijn
OUTPUT FORMAT (strict):
Bij ÉÉN span:
<SPANS>: ["..."]

Bij MEERDERE spans:
<SPANS>: ["...", "..."]

Bij GEEN spans:
<SPANS>: ["No"]

**Verwerk nu de volgende input:**
{instance}
Geef antwoord met ALLEEN ÉÉN <SPANS> blok. Geef NIET meerdere blokken terug. Herhaal NIET eerder genoemde spans. Zorg ervoor dat de format strict wordt gevolgd. Voeg geen uitleg toe.
"""

spans_detection_few_shots_nl = """Je bent een expert op het gebied van framing en taal bias. Je taak is om nieuwsfragmenten te analyseren en spans te identificeren die misleidend, bevooroordeeld, speculatief, emotioneel geladen of problematisch kunnen zijn.

TAAK
- Identificeer alleen unieke, niet-overlappende spans die de perceptie van de lezer kunnen beïnvloeden.
- Als er geen spans zijn gevonden, schrijf dan "Nee".


PROBLEMATISCHE SPANS ZIJN ONDER ANDERE:
- Beschrijft of verwijst naar gebeurtenissen op een manier die de verantwoordelijkheid bagatelliseert of vervormt (eventive bias).
- Beschrijft of verwijst naar mensen met behulp van emotioneel geladen, stereotype of overdreven taal (attributieve bias)
- Sensationaliseert of overdrijft feiten
- Gebruikt vage of speculatieve uitspraken alsof ze feitelijk zijn
OUTPUT FORMAT (strict):
Bij ÉÉN span:
<SPANS>: ["..."]

Bij MEERDERE spans:
<SPANS>: ["...", "..."]

Bij GEEN spans:
<SPANS>: ["No"]

Example 1 (for reference only — do NOT copy this):

TITLE: -Frits Bosch- Het Westen gaat aan altruisme ten onder
SENTENCE_0: Heb je de twee filmpjes gezien van die moslima’s in Den Bosch die los gaan: “de lijken van Alewieten moeten aan de vissen gevoerd worden.” Het geeft een inkijkje in de denkwereld, een kruidvat.
SENTENCE_1: Overigens als de Samaritaan een moslim was geweest en het slachtoffer een jood, dan was er gerede kans dat de moslim de jood niet geholpen had, maar vermoord had, conform de opdracht in soera’s.
SENTENCE_2: Eenieder die op een christelijke school heeft gezeten zal meegekregen hebben dat je jezelf dient weg te cijferen en dat je de ander moet helpen in nood.
<SPANS>: ["moslima’s in Den Bosch die los gaan", "Het Westen gaat aan altruisme ten onder", "de moslim de jood niet geholpen had, maar vermoord had"]

Example 2 (for reference only — do NOT copy this):

TITLE: Zelenski wijst vrede af: Europa en VS in de kou"
SENTENCE_0: Londen en Parijs kwamen al met een halfbakken idee voor een “beperkt staakt-het-vuren”: geen luchtaanvallen, geen zeegevechten, geen kapotgeschoten stroomnet.
SENTENCE_1: De Dagelijkse Standaard is een nieuws- en opinieweblog dat bovenop het nieuws zit, zelf nieuws brengt en commentaar en achtergronden levert bij het nieuws.
SENTENCE_2: Samen met de Europeanen wil hij een “gezamenlijk standpunt” bepalen – lees: een nieuw eisenpakket waar geen Rus ooit mee akkoord gaat.
<SPANS>: ["waar geen Rus ooit mee akkoord gaat", "halfbakken"]

Analyseer nu de volgende input en geef ALLEEN laatste <SPANS> output:
{instance}

Geef antwoord met ALLEEN ÉÉN <SPANS> blok. Geef NIET meerdere blokken terug. Herhaal NIET eerder genoemde spans. Zorg ervoor dat de format strict wordt gevolgd. Voeg geen uitleg toe.
"""

rationales_generation_zero_shot_nl = """Je bent een expert in discourse framing en media bias. Je taak is om uit te leggen waarom bepaalde stukken tekst in een nieuwsfragment misleidend, bevooroordeeld of problematisch kunnen zijn.

Je krijgt:
1. Een nieuwsfragment met:
   - Één TITLE regel
   - Drie SENTENCE regels (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. Een lijst met exacte spans uit die tekst.

Je doel is om **één redenatie te genereren voor elke span**. Gebruik deze strikte format:
→ “als [verwijzing naar de span in de tekst], dan [implicatie of gevolg]”.

Een span is problematisch als het:
- Beschrijft of verwijst naar gebeurtenissen op een manier die de verantwoordelijkheid bagatelliseert of vervormt (eventive bias).
- Beschrijft of verwijst naar mensen met behulp van emotioneel geladen, stereotype of overdreven taal (attributieve bias)
- Sensationaliseert of overdrijft feiten
- Gebruikt vage of speculatieve uitspraken alsof ze feitelijk zijn

Deze Output instructies moeten strikt worden opgevolgd:
- Als er spans aanwezig zijn, output dan één redenatie per span, in dezelfde volgorde
- Als <SPANS>: [“No”], output dan <RATIONALES>: [“No”].
- Genereer geen redenatie als <SPANS>: [“No”]
- Elke redenatie moet tussen dubbele aanhalingstekens staan (“rationale1”, “rationale2”, ...)
- Alle redenaties moeten worden gegeven in één <RATIONALES> lijst, in dezelfde volgorde als de spans en gescheiden door een komma(,)
- Voeg geen ellipsen of extra aanhalingstekens toe binnen de redenatie (geen “...als” of “...”)
- Herhaal geen spans en geef geen uitleg buiten het uitvoerblok
- Sla geen spans over en combineer ze niet
- Leg de uitvoer niet uit - retourneer alleen het onderstaande geformatteerde resultaat:

<RATIONALES>: ["als ..., dan ...", "als ..., dan ...", "..."].

Nieuwsfragment: {instance}

Spans: {spans}

Geef nu het uiteindelijke antwoord terug met <RATIONALES> tag, en Geen uitleg
"""

rationales_generation_few_shots_nl = """Je bent een expert in discourse framing en media bias. Je taak is om uit te leggen waarom bepaalde stukken tekst in een nieuwsfragment misleidend, bevooroordeeld of problematisch kunnen zijn.

Je krijgt:
1. Een nieuwsfragment met:
   - Één TITLE regel
   - Drie SENTENCE regels (SENTENCE_0, SENTENCE_1, SENTENCE_2)

2. Een lijst met exacte spans uit die tekst.

Je doel is om **één redenatie te genereren voor elke span**. Gebruik deze strikte format:
→ “als [verwijzing naar de span in de tekst], dan [implicatie of gevolg]”.

Een span is problematisch als het:
- Beschrijft of verwijst naar gebeurtenissen op een manier die de verantwoordelijkheid bagatelliseert of vervormt (eventive bias).
- Beschrijft of verwijst naar mensen met behulp van emotioneel geladen, stereotype of overdreven taal (attributieve bias)
- Sensationaliseert of overdrijft feiten
- Gebruikt vage of speculatieve uitspraken alsof ze feitelijk zijn

Deze Output instructies moeten strikt worden opgevolgd:
- Als er spans aanwezig zijn, output dan één redenatie per span, in dezelfde volgorde
- Als <SPANS>: [“No”], output dan <RATIONALES>: [“No”].
- Genereer geen redenatie als <SPANS>: [“No”]
- Elke redenatie moet tussen dubbele aanhalingstekens staan (“rationale1”, “rationale2”, ...)
- Alle redenaties moeten worden gegeven in één <RATIONALES> lijst, in dezelfde volgorde als de spans en gescheiden door een komma(,)
- Voeg geen ellipsen of extra aanhalingstekens toe binnen de redenatie (geen “...als” of “...”)
- Herhaal geen spans en geef geen uitleg buiten het uitvoerblok
- Sla geen spans over en combineer ze niet
- Leg de uitvoer niet uit - retourneer alleen het onderstaande geformatteerde resultaat:

<RATIONALES>: ["als ..., dan ...", "als ..., dan ...", "..."].

Example 1 (for reference only — do NOT copy this):

Input:

News Excerpt:
TITLE: -Frits Bosch- Het Westen gaat aan altruisme ten onder
SENTENCE_0: Heb je de twee filmpjes gezien van die moslima’s in Den Bosch die los gaan: “de lijken van Alewieten moeten aan de vissen gevoerd worden.” Het geeft een inkijkje in de denkwereld, een kruidvat.
SENTENCE_1: Overigens als de Samaritaan een moslim was geweest en het slachtoffer een jood, dan was er gerede kans dat de moslim de jood niet geholpen had, maar vermoord had, conform de opdracht in soera’s.
SENTENCE_2: Eenieder die op een christelijke school heeft gezeten zal meegekregen hebben dat je jezelf dient weg te cijferen en dat je de ander moet helpen in nood.

Spans: ["moslima’s in Den Bosch die los gaan", "Het Westen gaat aan altruisme ten onder", "de moslim de jood niet geholpen had, maar vermoord had"]

Output:
<RATIONALES>: ["ALS je op deze manier praat over deze dames DAN impliceer je dat hun gedrag komt doordat het moslims zijn", "ALS je het hebt over het hele Westen dat ten onder gaat DAN probeer je in te spelen op mensen hun angst", "ALS je zegt dat moslims iemand zouden vermoorden DAN verspreid je haat en angst richting die bevolkingsgroep"]

Example 2 (for reference only — do NOT copy this):

Input:

News Excerpt:

TITLE: Zelenski wijst vrede af: Europa en VS in de kou"
SENTENCE_0: Londen en Parijs kwamen al met een halfbakken idee voor een “beperkt staakt-het-vuren”: geen luchtaanvallen, geen zeegevechten, geen kapotgeschoten stroomnet.
SENTENCE_1: De Dagelijkse Standaard is een nieuws- en opinieweblog dat bovenop het nieuws zit, zelf nieuws brengt en commentaar en achtergronden levert bij het nieuws.
SENTENCE_2: Samen met de Europeanen wil hij een “gezamenlijk standpunt” bepalen – lees: een nieuw eisenpakket waar geen Rus ooit mee akkoord gaat.

Spans: ["waar geen Rus ooit mee akkoord gaat", "halfbakken"]

Output:
<RATIONALES>: ["ALS je een plan omschrijft als iets waar geen Rus ooit mee akkoord zal gaan DAN doe je het bij voorbaat af als een slecht plan en noem je de maker ervan incompetent, iets wat niet past bij neutrale verslaggeving", "ALS je het woord halfbakken gebruikt DAN doe je geen politiek neutraal verslag"]

Verwerk nu de volgende input:

Nieuwsfragment: {instance}

Spans: {spans}

Geef nu het uiteindelijke antwoord terug met <RATIONALES> tag, en Geen uitleg
"""


spans_detection_zero_shot_ru = """Ты — эксперт по фреймингу и языковой предвзятости. Твоя задача — анализировать фрагменты новостей и выявлять отрывки текста, которые могут вводить в заблуждение, быть предвзятыми, спекулятивными, эмоционально окрашенными или проблемными.
ЗАДАЧА
Определяй только уникальные, неперекрывающиеся фрагменты, которые могут повлиять на восприятие читателя.
Если таких фрагментов не обнаружено, напиши "No".
ПРОБЛЕМНЫЕ ФРАГМЕНТЫ ВКЛЮЧАЮТ:
Описывает или упоминает события таким образом, что ответственность преуменьшается или искажается (событийная предвзятость).
Описывает или упоминает людей в эмоционально окрашенных, стереотипных или преувеличенных выражениях (атрибутивная предвзятость).
Сенсационализирует или преувеличивает факты.
Использует расплывчатые или предположительные утверждения как достоверные факты.
ФОРМАТ ВЫВОДА (строго):
 Если ОДИН фрагмент:
 <SPANS>: ["..."]
Если НЕСКОЛЬКО фрагментов:
 <SPANS>: ["...", "..."]
Если фрагментов нет:
 <SPANS>: ["No"]
Возвращай ТОЛЬКО ОДИН блок <SPANS>. НЕ возвращай несколько блоков. НЕ повторяй уже указанные фрагменты. Строго соблюдай формат. Не добавляй пояснений.
**Теперь обработай следующие исходные данные:**
{instance}
"""

spans_detection_few_shots_ru = """Ты — эксперт по фреймингу и языковой предвзятости. Твоя задача — анализировать фрагменты новостей и выявлять отрывки текста, которые могут вводить в заблуждение, быть предвзятыми, спекулятивными, эмоционально окрашенными или проблемными.
ЗАДАЧА
Определяй только уникальные, неперекрывающиеся фрагменты, которые могут повлиять на восприятие читателя.
Если таких фрагментов не обнаружено, напиши "No".
ПРОБЛЕМНЫЕ ФРАГМЕНТЫ ВКЛЮЧАЮТ:
Описывает или упоминает события таким образом, что ответственность преуменьшается или искажается (событийная предвзятость).
Описывает или упоминает людей в эмоционально окрашенных, стереотипных или преувеличенных выражениях (атрибутивная предвзятость).
Сенсационализирует или преувеличивает факты.
Использует расплывчатые или предположительные утверждения как достоверные факты.
ФОРМАТ ВЫВОДА (строго):
 Если ОДИН фрагмент:
<SPANS>: ["..."]

Если НЕСКОЛЬКО фрагментов:
 <SPANS>: ["...", "..."]

Если фрагментов нет:
 <SPANS>: ["No"]
Возвращай ТОЛЬКО ОДИН блок <SPANS>. НЕ возвращай несколько блоков. НЕ повторяй уже указанные фрагменты. Строго соблюдай формат.

Образец 1 (только для справки — НЕ копируй это):

TITLE: Новости науки сегодня LIVE24
SENTENCE_0: Частое злоупотребление просмотром порно напрямую связано с низкой самооценкой у женщин.
SENTENCE_1: Запись о регистрации СМИ: Эл No ФС77-88404 выдано Роскомнадзором 29.10.2024.
SENTENCE_2: *Meta Platforms (Instagram, Facebook) признана экстремистской организацией и запрещена.
<SPANS>: ["Частое злоупотребление просмотром порно напрямую связано с низкой самооценкой у женщин"]

Образец 2 (только для справки — НЕ копируй это):

TITLE: Трамп заявил об обязательствах Киева перед США на $400–500 млрд — РБК
SENTENCE_0: Axios писал, что США несколько дней назад передали Украине «улучшенный» проект сделки и призвали Зеленского подписать обновленное соглашение, чтобы «избежать дальнейшего столкновения с Трампом и позволить президенту США обосновать дальнейшую поддержку Украины».
SENTENCE_1: WSJ узнала дату возможного подписания США и Украиной сделки об ископаемых Политика
SENTENCE_2: В Белом доме на фоне ужесточившейся риторики Трампа и угроз Украине «проблемами» также выразили уверенность, что сделка будет одобрена Киевом в ближайшее время.
<SPANS>: ["Трамп заявил об обязательствах Киева перед США на $400–500 млрд", "США несколько дней назад передали Украине «улучшенный» проект сделки", "выразили уверенность, что сделка будет одобрена Киевом в ближайшее время."]

Теперь проанализируй следующий ввод и верни ТОЛЬКО финальный блок <SPANS>:
{instance}
Ответ должен содержать ТОЛЬКО ОДИН блок <SPANS>. НЕ возвращай несколько блоков. НЕ повторяй уже указанные интервалы <SPANS>. Строго соблюдай формат. НЕ добавляй пояснений.
"""

rationales_generation_zero_shot_ru = """Ты — эксперт по фреймингу и языковой предвзятости. Твоя задача — объяснить, почему определённые фрагменты текста в новостном отрывке могут быть вводящими в заблуждение, предвзятыми или проблематичными.
Вам предоставляется:
Новостной отрывок, содержащий:


Одну строку с ЗАГОЛОВКОМ


Три строки с ПРЕДЛОЖЕНИЯМИ (SENTENCE_0, SENTENCE_1, SENTENCE_2)


Список точных фрагментов, извлечённых из текста.


Ваша цель — сгенерировать **одно обоснование для каждого фрагмента**. Используйте строгий формат:
 → "если [отсылка к фрагменту в тексте], то [следствие или вывод]"
Фрагмент считается проблематичным, если он:
Описывает события или ссылается на них таким образом, что умаляет или искажает ответственность (байас событий)


Описывает людей или ссылается на них, используя эмоционально окрашенный, стереотипный или преувеличенный язык (атрибутивный байас)


Сенсационализирует или преувеличивает факты


Использует расплывчатые или предположительные утверждения как факты


Эти инструкции по выводу необходимо строго соблюдать:
Если фрагменты присутствуют, верните одно обоснование на каждый фрагмент, в точном порядке


Если <SPANS>: ["No"], то верните <RATIONALES>: ["No"]


Не генерируйте обоснование, если <SPANS>: ["No"]


Каждое обоснование должно быть заключено в двойные кавычки ("обоснование1", "обоснование2", ...)


Все обоснования должны быть возвращены в одном списке <RATIONALES>, строго в порядке фрагментов и разделены запятыми (,)


Не добавляйте многоточий или лишних кавычек внутри обоснования (никаких "...если" или "...")


Не повторяйте фрагменты и не добавляйте объяснений вне блока вывода


Не пропускайте и не объединяйте фрагменты


Не объясняйте ваш вывод — просто верните отформатированный результат ниже:


<RATIONALES>: ["если ..., то ...", "если ..., то ...", "..."]
Новостной отрывок: {instance}

Фрагменты: {spans}

Теперь верните окончательный ответ с тегом <RATIONALES> и без объяснений.
"""

rationales_generation_few_shots_ru = """Ты — эксперт по фреймингу и языковой предвзятости. Ваша задача — объяснить, почему определённые фрагменты текста в новостном отрывке могут быть вводящими в заблуждение, предвзятыми или проблематичными.
Вам предоставляется:
Новостной отрывок, содержащий:

Одну строку с ЗАГОЛОВКОМ

Три строки с ПРЕДЛОЖЕНИЯМИ (SENTENCE_0, SENTENCE_1, SENTENCE_2)

Список точных фрагментов, извлечённых из текста.

Ваша цель — сгенерировать одно обоснование для каждого фрагмента. Используйте строгий формат:
 → "если [отсылка к фрагменту в тексте], то [следствие или вывод]"
Фрагмент считается проблематичным, если он:
Описывает события или ссылается на них таким образом, что умаляет или искажает ответственность (байас событий)

Описывает людей или ссылается на них, используя эмоционально окрашенный, стереотипный или преувеличенный язык (атрибутивный байас)

Сенсационализирует или преувеличивает факты

Использует расплывчатые или предположительные утверждения как факты

Эти инструкции по выводу необходимо строго соблюдать:
Если фрагменты присутствуют, верните одно обоснование на каждый фрагмент, в точном порядке

Если <SPANS>: ["No"], то верните <RATIONALES>: ["No"]


Не генерируйте обоснование, если <SPANS>: ["No"]


Каждое обоснование должно быть заключено в двойные кавычки ("обоснование1", "обоснование2", ...)


Все обоснования должны быть возвращены в одном списке <RATIONALES>, строго в порядке фрагментов и разделены запятыми (,)


Не добавляйте многоточий или лишних кавычек внутри обоснования (никаких "...если" или "...")


Не повторяйте фрагменты и не добавляйте объяснений вне блока вывода


Не пропускайте и не объединяйте фрагменты


Не объясняйте ваш вывод — просто верните отформатированный результат ниже:

<RATIONALES>: ["если ..., то ...", "если ..., то ...", "..."]

Пример 1 (только для справки — НЕ копировать его):
Ввод:

Новостной отрывок:
TITLE: Новости науки сегодня LIVE24
SENTENCE_0: Частое злоупотребление просмотром порно напрямую связано с низкой самооценкой у женщин.
SENTENCE_1: Запись о регистрации СМИ: Эл No ФС77-88404 выдано Роскомнадзором 29.10.2024.
SENTENCE_2: *Meta Platforms (Instagram, Facebook) признана экстремистской организацией и запрещена.
Spans: ["Частое злоупотребление просмотром порно напрямую связано с низкой самооценкой у женщин"]

Вывод:
<RATIONALES>: ["Если вы утверждаете, что просмотр порно напрямую связан с низкой самооценкой у женщин, не предоставляя при этом источников или уточнений, тогда вы рискуете воспроизвести гендерные стереотипы и стигматизировать поведение, делая выводы о психологическом состоянии на основе предположений."]

Пример 2 (только для справки — НЕ копировать его):
Ввод:
TITLE: Трамп заявил об обязательствах Киева перед США на $400–500 млрд — РБК
SENTENCE_0: Axios писал, что США несколько дней назад передали Украине «улучшенный» проект сделки и призвали Зеленского подписать обновленное соглашение, чтобы «избежать дальнейшего столкновения с Трампом и позволить президенту США обосновать дальнейшую поддержку Украины».
SENTENCE_1: WSJ узнала дату возможного подписания США и Украиной сделки об ископаемых Политика
SENTENCE_2: В Белом доме на фоне ужесточившейся риторики Трампа и угроз Украине «проблемами» также выразили уверенность, что сделка будет одобрена Киевом в ближайшее время.
Spans: ["Трамп заявил об обязательствах Киева перед США на $400–500 млрд", "США несколько дней назад передали Украине «улучшенный» проект сделки", "выразили уверенность, что сделка будет одобрена Киевом в ближайшее время."]

Output:
<RATIONALES>: ["Если заголовок утверждает о конкретных финансовых обязательствах без указания источника (кроме слов Трампа) и деталей соглашения, тогда он может создавать ложное впечатление о масштабах долга Украины.", "Если термин 'улучшенный' взят в кавычки без пояснений, тогда это может намекать на его условность или скрытые невыгодные условия.", "Если утверждается об 'уверенности' без указания источников, тогда это может быть попыткой создать впечатление неизбежности принятия условий."]

Теперь обработайте следующий ввод:
Новостной отрывок: {instance}
Фрагменты: {spans}
Теперь верните окончательный ответ с тегом <RATIONALES> и без объяснений.
"""

retry_prompt = """You are a formatting and data extraction assistant. Your task is to extract and standardize the information after {tag} tag.

INSTRUCTIONS:

Identify and return the List that can be parsed by json, without any other text or comments.

The block must follow the strict format:

If input has ONE span:
{tag}: ["..."]
You should return:
["..."]

If input has MULTIPLE spans:
{tag}: ["...", "..."]
You should return:
["...", "..."]

If there are any formatting issues, you should fix them. For example:
Input: {tag}: ["supposed “lies""]
You should return:
["supposed 'lies'"]

Ensure:

Only straight double quotes (") are used (no curly quotes).

Do not add explanations or comments—output only the corrected list.

Now correct the following model output:

{model_output}
"""





task_1_prompt_zero_shot_en = """You are a framing and language bias expert. Your task is to classify the severity of problematic language in a news article excerpt. Each excerpt includes a title and up to three sentences.

Classify the severity based on the presence and impact of the following problematic characteristics:

Eventive bias: Describes or refers to events in a way that downplays or distorts responsibility.

Attributive bias: Describes or refers to people using emotionally charged, stereotypical, or exaggerated language.

Sensationalism: Exaggerates or dramatizes facts.

Speculation: Uses vague or speculative statements as if they are factual.

SEVERITY LABELS:

"none" – No problematic characteristics present. The text is factual, balanced, and neutral.

"slightly" – Minor problematic language is present (e.g., a single emotionally charged word or vague phrase), but the overall message remains mostly objective.

"moderately" – Multiple instances of bias or misleading language that may affect the reader’s understanding or promote subtle distortion.

"highly" – Severe and pervasive use of biased, speculative, or emotionally manipulative language. High risk of misinformation, misrepresentation, or harmful framing.

OUTPUT FORMAT:
Only return one of the four labels after by <PREDICTED_LABEL> tag, exactly as shown:
<PREDICTED_LABEL>: none
<PREDICTED_LABEL>: slightly
<PREDICTED_LABEL>: moderately
<PREDICTED_LABEL>: highly


-Do not add any extra text, explanation, label names, or commentary.

-Do not include anything before or after the double-quoted label.

-Only return one valid output.

Now process the following input:
{instance}
"""

task_1_prompt_few_shots_en = """You are a framing and language bias expert. Your task is to classify the severity of problematic language in a news article excerpt. Each excerpt includes a title and up to three sentences.

Classify the severity based on the presence and impact of the following problematic characteristics:

Eventive bias: Describes or refers to events in a way that downplays or distorts responsibility.

Attributive bias: Describes or refers to people using emotionally charged, stereotypical, or exaggerated language.

Sensationalism: Exaggerates or dramatizes facts.

Speculation: Uses vague or speculative statements as if they are factual.

SEVERITY LABELS:

"none" – No problematic characteristics present. The text is factual, balanced, and neutral.

"slightly" – Minor problematic language is present (e.g., a single emotionally charged word or vague phrase), but the overall message remains mostly objective.

"moderately" – Multiple instances of bias or misleading language that may affect the reader’s understanding or promote subtle distortion.

"highly" – Severe and pervasive use of biased, speculative, or emotionally manipulative language. High risk of misinformation, misrepresentation, or harmful framing.

OUTPUT FORMAT:
Only return one of the four labels after by <PREDICTED_LABEL> tag, exactly as shown:
<PREDICTED_LABEL>: none
<PREDICTED_LABEL>: slightly
<PREDICTED_LABEL>: moderately
<PREDICTED_LABEL>: highly

-Do not add any extra text, explanation, label names, or commentary.

-Do not include anything before or after the double-quoted label.

-Only return one valid output.

Example 1 (for reference only — do NOT copy this):
Input: TITLE: Lost sons of the Nimitz, page 1
SENTENCE 1: The Nimitz searched for three days, but no trace of the crew was ever found.The Navy announced the crash, which barely got any coverage, in part because it was the first anniversary of the Challenger disaster.
SENTENCE 2: Pat Price belonged to the classified unit known as Navy Security Group Department: 30.What the crew did on the mission is still unknown, but it's believed that they were evesdropping on Libyan communications, as well as Russian intelligence ships in the area.
SENTENCE 3: So he returned to the ship, as the only option.After making two more attempts, the crew was ordered to rig the barricade.
<PREDICTED_LABEL>: slightly

Example 2 (for reference only — do NOT copy this):
Input: TITLE: Bob Woodward and Carl Bernstein decry media's 'smugness' and 'self-righteousness' toward Trump
SENTENCE 1: "We oughtn’t be too provocative, which we sometimes are with a president who’s putting a lot of bait out there and sometimes we take the bait and get a little petty," said Bernstein.
SENTENCE 2: Appearing Sunday on CNN's "State of the Union," the two longtime reporters said there should be less pettiness and outrage in the media when it comes to President Trump.
SENTENCE 3: "In lots of reporting, particularly on television commentary, there’s a kind of self-righteousness and smugness and people kind of ridiculing the president.
<PREDICTED_LABEL>: none

Example 3 (for reference only — do NOT copy this):
Input:TITLE: TITLE: How to Act Compassionately Towards Transgender People: Do Not Encourage a Delusion
SENTENCE 1: What is accepted as true on CNN is the statement, “We both know, that the chromosomes do not necessarily mean that you are male or female.” But in the real world of biology, that is exactly what that means.
SENTENCE 2: The Compassionate Way to Deal With Gender Dysphoria In the transgender family, the kids wanted to express the opposite gender before the mother.
SENTENCE 3: And I believe it is child abuse to allow a kid to take hormones and mutilate their genitals in an attempt to appear as the opposite sex.
<Predicted Label>: highly

Now process the following input:
input: {instance}
"""


task_1_retry_prompt = """You are a formatting and data extraction assistant. Your task is to extract and standardize the information after <PREDICTED_LABEL> tag.

INSTRUCTIONS:

Identify and return the string without any other unrelated text or comments.

The block must follow the strict format:
If input looks like this: <PREDICTED_LABEL>: "word 1"
You should return: word 1

If there are any formatting issues, you should fix them. For example:
Input: <PREDICTED_LABEL>: "highly OR <PREDICTED_LABEL>: "highly"
You should return: highly

Ensure:
Do not add explanations or comments—output only the corrected string.
Now correct the following model output:
{model_output}"""

