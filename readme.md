# JCJL programmeer taal

## 1 Ontwerp JCJL

Tijdens het typen van code is het onhandig om steeds symbolen in te moeten voeren. Een plus-teken of een accolade is toch altijd weer zoeken, en dat kost tijd. Om sneller te programmeren, kan JCJL gebruikt worden. In JCJL bestaat de hele code uit letters en cijfers. De enige uitzondering is dat strings met het `"`-symbool moeten starten en eindigen.

Lege ruimtes als spaties en tabs worden genegeerd door de interpreter en kunnen gebruikt worden om de code visueel nette weergave te geven. Regeleindes geven wel het einde van een statement of definitie weer en zijn dus wel belangrijk.

JCJL is een functionele programmeertaal. Dit houdt in dat alle code binnen een functie gedefinieerd moet worden. Er bestaan ook geen globale variabelen. Een functie weet alleen wat er binnen zijn eigen definitie gebeurt en neemt geen notie van andere code. 

JCJL kan in de huidige staat geen meerdere bestanden tegelijkertijd verwerken. Alle code moet in een enkel bestand staan en code uit andere bestanden kan niet gebruikt worden.

### 1.1 Commentaar

Om commentaar te gebruiken in JCJL moet de regel met `comment` beginnen. Als dit sleutelwoord aan het begin van de regel staat, zal alles op die regel genegeerd worden.

```text
comment Deze tekst zal genegeerd worden
```

### 1.2 Variabelen

Een variabele houdt een functie vast. De naam van een variabele moet met een kleine letter beginnen, maar kan verder uit kleine letters, hoofdletters, cijfers en laag streepje (`_` / underscore) bestaan. Een variabele moet eerst gedefinieerd worden met een type, maar kan daarna vrij gebruikt worden of nieuwe waardes krijgen

Het toekennen van een waarde gebeurt met het sleutelwoord `is`, gevolgd door een expressie. Dit kan een literal zijn, operatie, vergelijking of een functie-aanroeping zijn. 

Er bestaan 3 verschillende type variabelen. Een getal (int), een booleaanse waarde (bool) of een zin (string). Booleaanse waardes zijn of `true` of `false`. Getallen kunnen in het decimale stelsel gedefinieerd worden of in het hexadecimale stelsel. Voor hexadecimaal moet de waarde met `0x` beginnen. Zinnen beginnen en eindigen met een dubbel aanhalingsteken. 

```text
int first_var is 3
int second_var is 0xFF
second_var is first_var

bool compare_var1 is true
bool compare_var2 is false

string characters is "Dit is een zin"
```


### 1.3 Berekeningen

Binnen JCJL is het mogelijk om te rekenen met variabelen. Dit gebeurt op de volgende manier:

```text
int var1 is 3
int var2 is 4
var2 is var1 plus var2
comment var2 is nu 7

int var4 is 0
var4 notis var2
var4 is var4 and 0xFF

comment alle ints zijn 32bits, door deze bewerking is var4 nu 248

```

Mogelijke operaties zijn:

|     Functie                             |     Wiskundig   symbool    |     JCJL   definitie    |
|-----------------------------------------|----------------------------|-------------------------|
|     Optellen                            |     A + B                  |     plus                |
|     Aftrekken                           |     A – B                  |     min                 |
|     Vermenigvuldigen                    |     A * B                  |     mul                 |
|     Delen                               |     A / B                  |     div                 |
|     Modulo                              |     A % B                  |     mod                 |
|                                         |                            |                         |
|     En                                  |     A & B                  |     and                 |
|     Of                                  |     A &#124; B             |     or                  |
|     Exclusieve of                       |     A ^ B                  |     xor                 |
|     Bit op 0   zetten                   |     A & (~B)               |     bic                 |
|     Shift naar   links                  |     A << B                 |     lshift              |
|     Shift naar   rechts                 |     A >> B                 |     rshift              |

#### 1.3.1 Unaire operaties

Het is mogelijk om unaire berekeningen te doen. Hiervoor wordt de functie direct gevolgd door het woord `is`. Enige uitzondering is inverteren (notis). Deze bestaat alleen als unaire versie waarbij de linkerkant gelijk wordt aan de geïnverteerde waarde die rechts staat.

```text
int var1 is 4
var1 plusis 3
comment var1 is nu 7

```

#### 1.3.2 Vergelijkingen

Voor verschillende toepassingen is het handig om twee waardes met elkaar te vergelijken. Dat kan met de volgende functies:

|     Functie                    |     Gebruikelijk   symbool    |     JCJL   definitie     |
|--------------------------------|-------------------------------|--------------------------|
|     Gelijkheid                 |     A == B                    |     equals               |
|     Kleiner dan                |     A < B                     |     lessthan             |
|     Groter dan                 |     A > B                     |     greaterthan          |
|     Kleiner dan   of gelijk    |     A <= B                    |     lessthanequals       |
|     Groter dan of   gelijk     |     A >= B                    |     greaterthanequals    |
|     Ongelijk                   |     A !=                      |     notequals            |

### 1.4 For-loop

Een for-loop bestaat uit 3 delen. Een start, code die herhaald moet worden en een einde. De start van een for-loop heeft een strakke definitie. Na het `for`-sleutelwoord moet een nieuwe variabele gedefinieerd worden, gevolgd door het sleutelwoord `while` waarna een expressie aangeeft hoe lang de for-loop moet herhalen, en als laatste komt het `with`-sleutelwoord met een expressie die elke herhaling uitgevoerd wordt. 

Het afsluiten van een for-loop gebeurt met het `endfor`-sleutelwoord

Zie hier een voorbeeld:

```text
for int i is 10 while i greaterthan 1 with i minmin
    comment Hier komt de code te staan die herhaalt moet worden
endfor
```

### 1.5 While-loop

Een while-loop is een simpelere definitie. Een while-loop begint met het `while`-sleutelwoord gevolgd door een expressie. Daarna komt de code die herhaalt moet worden en de while-loop wordt afgesloten met het `endwhile`-sleutelwoord.

Geldige expressies voor een while-loop moeten een getal of een booleaanse waarde geven. Zolang de expressie `true` is, of groter dan 0, zal de while-loop herhalen. Geldige expressies zijn operaties, functie-aanroepingen, vaste waardes, variabelen en vergelijkingen.

```text
int var1 is 4
while var1
    var1 minmin
endwhile
```

### 1.6 If-else statement

Om de code beslissingen te laten maken, kan een if statement of een if-else statement. Het if statement neemt een vergelijking (equals, lessthan, notequals, ...) tussen twee variabelen of waardes. Als de vergelijking waar is zal het blok dat onder de if staat uitgevoerd worden. Is er een else aanwezig, dan zal de code daaronder uitgevoerd worden als de vergelijking niet waar is.

```text
var1 is 18
var2 is 43

if var1 lessthan var2
    comment als var1 kleiner dat var2 is, zal de code hier uitgevoerd worden
endif

if var1 equals var2
    comment code voor als var1 en var2 aan elkaar gelijk zijn
else
    comment code die wordt uitgevoerd als var1 en var2 van elkaar verschillen.
endif
```

### 1.7 Functies

Omdat JCJL een functionele taal is, zal alle code in een functie gedefinieerd moeten worden. Een functie heeft een type, een naam en optioneel parameters. Een functie geeft altijd een waarde terug. 

De definitie begint met het type dat de functie terug geeft. Na het type komt het `function`-sleutelwoord gevolgd door de functienaam. Eventuele parameters kunnen na de naam aangegeven worden. Elk parameter geeft eerst aan wat voor type het moet zijn, gevolgd door de naam van de parameter.

```text
int sum int left int right
    int result is left plus right
    return result
```

#### 1.7.1 Functies aanroepen

Om een functie aan te roepen wordt het `call`-sleutelwoord gebruikt. Deze wordt dan gevolgd door de naam van de functie, en eventuele parameters die de functie nodig heeft.

```text
int function main
    int var1 is 4
    int var2 is 5

    var2 is call sum var1 3
    comment var2 heeft nu de waarde van 7 (var1 = 4; plus de vaste waarde 3)

    return 0
```

#### 1.7.2 Ingebouwde functies

JCJL heeft maar 3 ingebouwde functies:

- `print`: Print de waarde die in de parameter wordt meegegeven
- `size`: Geeft de lengte van een string die in de parameter wordt gegeven
- `input`: Vraagt invoer van de gebruiker. In de parameter moet een string meegegeven worden die aan de gebruiker aangeeft wat gevraagd wordt..

## 2 JCJL code draaien

Om de JCJL interpreter te gebruiken, is de enige verplichting dat python geïnstalleerd is. De code is geschreven en getest met python versie 3.8, maar zou ook met 3.6 en 3.7 moeten werken (verificatie gedaan aan de hand van change-logs, maar is niet getest in de praktijk). Er worden geen extra libraries of externe modules geïmporteerd. 

De code wordt gedraaid door het bestand `main.py` aan te roepen en als argumenten het bestand met de code en de functie die als eerst aangeroepen wordt te geven. Extra argumenten worden als parameters aan de functie doorgegeven:

```commandline
$ python main.py programs/hello_world.txt hello
$ python main.py programs/loop.txt sommig_for 5
$ python main.py programs/loop.txt sum_three 1 2 3
```

### 2.1 Voorbeelden

Bij de interpreter zijn verschillende voorbeelden meegeleverd. In deze voorbeelden zijn loops, if/else statements en functie aanroepingen te zien. Ook invoer en uitvoer worden behandeld. De voorbeelden zijn in de map `programs` te vinden.

- `hello_world.txt`: Voorbeeld van I/O
    - `hello`: Geeft voorbeeld van invoer en uitvoer
- `loop.txt` Functies voor berekenen van driehoekig nummer met loops (https://en.wikipedia.org/wiki/Triangular_number)
    - `sommig_while`: Bereken met een while-loop 
    - `sommig_while`: Bereken het een for-loop
- `dubble_recursive.txt` Laat recursie en conditionele logica zien
    - `even_or_odd`: Controleer of een gegeven waarde even of oneven is
- `examples.txt`: Assortiment voorbeelden wat de code kan
    - `power`: Bereken 2 waardes waarbij de eerste parameter tot de macht van de tweede parameter wordt genomen
    - `sum_three`: Tel drie gegeven parameters bij elkaar op en geeft het resultaat terug
    - `main`: Hoe worden variabelen gedefinieerd en aan een andere functie gegeven
    - `main2`: Assortiment voorbeelden van uitvoer met regeleinde, functies aanroepen en gebruik for-loop
    - `crash`: Functie die bedoeld een foutmelding genereert om het gebruik van stack-trace aan te tonen

## 3 Foutmeldingen

Tijdens het verwerken van de gegeven code, maar ook tijdens het uitvoeren van de code, kunnen er fouten voorkomen. Wanneer het bekend is, zal de foutmelding aangeven op welke regel de code plaatsvindt. 

Als een fout tijdens het draaien plaats vind, zal eerst het type error weergegeven worden, gevolgd door welke functies aangeroepen zijn om tot de foutmelding te komen.

De volgende fouten kunnen voorkomen:


|       Foutmelding            |       Betekenis                                                                                                                     |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
|     FILE_NOT_FOUND_ERROR     |     Het bestand dat   uitgevoerd zou moeten worden, kan niet gevonden worden                                                        |
|     SYNTAX_ERROR             |     Er zit een   fout in de code waardoor deze niet verwerkt kan worden                                                             |
|     NO_RETURN_FOUND          |     Er is geen   functie-einde gevonden                                                                                             |
|     INVALID_NAME_ERROR       |     Functie heeft   geen geldige naam                                                                                               |
|     UNKNOWN_TYPE_ERROR       |     Het type voor   de variabele is niet bekend                                                                                     |
|     STATEMENT_ERROR          |     Wanneer een   statement geen geldige vorm of syntax heeft.                                                                      |
|     PARAMETER_ERROR          |     Functie wordt   aangeroepen met ongeldige parameters. Dit kan het verkeerde aantal parameters   zijn, als het verkeerde type    |
|     UNKNOW_VARIABLE_ERROR    |     De   aangeroepen variabele is niet bekend binnen de functie                                                                     |
|     RUNTIME_ERROR            |     Er is een   fout opgetreden tijdens het uitvoeren van de code                                                                   |

## 4 Turing test

JCJL kan als Turing-compleet beschouwd worden. De taal ondersteund namelijk belangrijke functies die nodig zijn om een taal Turing-compleet te maken:

- Loops: Zowel for-loops als while-loops zijn geïmplementeerd
- If/else: De code kan aan de hand van condities verschillende code uitvoeren
- Functies: De code ondersteund het aanroepen, en waardes verkrijgen uit functies
- Recursie: De code ondersteund recursie, functies kunnen zichzelf aanroepen
- I/O: De code kan gegevens naar de gebruiker weergeven en gegevens van de gebruiker vragen

## 5 Structuur code

De stappen voor het verwerken en uitvoeren van de code zijn in 3 delen te onderscheiden: lexen, parsen en interpreteren. De uitvoer van de lexer wordt gebruikt in de parser, en de parser geeft uitvoer die geïnterpreteerd kan worden.

### 5.1 Lexer

De eerste stap is het lexen. In `decoder/lexer.py` staan alle functies met betrekking tot het lexen. De uitvoer van de lexer is een lijst met Tokens die een representatie van de code is.

De eerste stap is dat de functie `lexer(file: str)` een bestand inleest (met behulp van functies in `decoder/io/jcjlreader.py`). Het resultaat is een lijst van regels.

Stap 2 is dat elke regel omgezet wordt in een lijst van woorden. String-literals zullen niet gesplitst worden maar als 1 woord behandeld worden ondanks er spaties in staan.

De laatste is dat elk woord in een token wordt omgezet. De functie `lex_token(word: str, line_nmr: int)` zet elk woord in een token om. In `decoder.enums.py` staan alle typen die een token kan zijn. Om een woord in een token om te zetten, wordt eerst gekeken of het een sleutelwoord is. Zo niet wordt gekeken of het een string of getal is. Als laatste wordt gekeken of het wel een valide variabele naam is.

### 5.2 Parser

Om waarde te geven aan de lijst van tokens, zal deze geparsed moeten worden. In `decoder/parser.py` staan de functies die de lijst van tokens verwerkt naar een lijst van functies die elk een AST (abstract syntax tree) heeft. 

De AST bestaat uit nodes (gedefinieerd in `decoder/nodes.py`) die door de interpreter uitgevoerd kunnen worden.

Stap 1 in het parsen is om het begin van de functie te controleren op de correcte syntax. 

In stap 2 worden de tokens 1 voor 1 gecontroleerd of het een return-token is. Zolang geen return gevonden is, wordt de token tot de code van de functie beschouwd. 

In stap 3 wordt de expressie die achter het return-token staat in een node omgezet.

Stap 4 is alle tokens die binnen de functie omzetten in nodes. Hiervoor wordt gekeken wat de eerste token is:

- For-token: er is een forloop gevonden. Hierbij zal het einde van de for-loop gezocht worden, en de token binnen de for-loop zullen dan volgens stap 4 omgezet worden in nodes.
- While-token: er is een while-loop gevonden. Hetzelfde als bij de for-loop zal naar het einde gezocht worden en alle tokens in de loop in nodes omgezet worden
- If-token: er is een if-statement gevonden. Zodra het einde van het if-statement gevonden is, zal gezocht worden of er een else aanwezig is. Alle tokens binnen de if en else zullen ook apart in nodes omgezet worden.
- Call-token: dit houdt in dat er een functie aangeroepen wordt. Tijdens het parsen wordt niet gekeken of de functie al dan niet bestaat. Ook wordt in de Call-node bijgehouden welke parameters meegegeven worden.
- Type-token: dit houdt in dat een nieuwe variabele wordt aangemaakt. Het type zal dan ook gevolgd worden door de naam van de nieuwe variabele, en een waarde.
- Identifier-token: Dit kan verschillende inhouden. Maar in alle gevallen betekend het dat er een nieuwe waarde aan de variabele toegekend wordt. Of dit via een expressie, unaire operatie of verhoging/verlaging is.

Stap 5 is dat de functie-node opgeslagen wordt onder de gegeven functie-naam. Hierdoor kan de functie aangeroepen en de nodes binnen de functie uitgevoerd worden.

### 5.3 Interpreter

De interpreter krijg van de gebruiker de functie mee waarmee gestart moet worden. De interpreter kijkt dan naar de functie-map die door de parser is gemaakt. De aangeroepen functie wordt dan gepakt en de lijst met nodes binnen de functie worden uitgevoerd. 

Wanneer een functie wordt aangeroepen, bestaat er een lijst met variabelen waar alleen de parameters in zijn. De nodes binnen de functie kunnen de lijst gebruiken en aanpassen. Zodra alle nodes uitgevoerd zijn, wordt de expressie in de return op deze lijst uitgevoerd. Hierdoor wordt de juiste waarde verkregen om terug te geven naar de aanroeper van de functie.

Elke node bevat alle gegevens die de interpreter nodig zou kunnen hebben om de juiste uitvoering te doen.

### 5.4 Decorator

Om de status van het interpreteren van de code weer te geven zijn sleutelfuncties aangevuld met een decorator die aangeeft of de functie aangeroepen is. De functies die hiervan gebruik maken zijn: 

- `decoder.io.jcjlreader.read_program`: Bestand wordt gelezen
- `decoder.lexer.lex_lines`: De interpreter is begonnen met het lexen van de code
- `decoder.parser.parse`: De interpreter is begonnen met het parsen van de code

De decorator staat op de locatie: `decorder.utils.status_logger`

Het gebruik van de status_logger is door deze een bericht mee te geven. Wanneer de functie aangeroepen wordt, zal eerst het bericht naar de console geprint worden. 

Voorbeeld
```python
from decoder.utils import status_logger

@status_logger('Belangrijke functie is aangeroepen')
def important():
    pass
```

### 5.5 Hogere orde functies

De opdracht verplicht om ten minste 3 hogere order functies gebruikt moeten worden. De functies die gebruikt worden zijn:

- map
- filter
- reduce

Daarnaast is er nog een eigen geschreven hogere order functie geschreven. Deze functie neemt een lijst van functie in met twee waardes.
De functies worden dan in volgorde aangeroepen. De eerste waarde die niet None is, zal terug gegeven worden. Geven echter alle functies None terug, zal het resultaat ook None zijn

De functie locatie is: `decoder.utils.literal_identifier_function_looper`

## 6 Testcases

Er zijn 3 type tests bijgeleverd met de code. Voor de lexer bestaan er unittests, er is een integratietest tussen de lexer en de parser, en er is een volledige systeemtest aanwezig. De tests kunnen op de volgende manier uitgevoerd worden:

- Alle tests: `python -m tests.full_test`
- Unittests: `python -m tests.unit_tests`
- Integratie test: `python -m tests.integration_test`
- Systeem test: `python -m tests.system_test`
