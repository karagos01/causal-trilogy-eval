# Causal Field trilogy — nezávislé vyhodnocení

Reprodukovatelné vyhodnocení tří preprintů, které 25. září 2026 vystavili na
Zenodu M. Mazgal a Gemini AI:

| | DOI | název |
|---|---|---|
| I | [10.5281/zenodo.22959886](https://doi.org/10.5281/zenodo.22959886) | The Causal Quaternionic Field Theory (CQFT) |
| II | [10.5281/zenodo.22962188](https://doi.org/10.5281/zenodo.22962188) | Photonic Causal Tensor Processor (PCTP) |
| III | [10.5281/zenodo.22962557](https://doi.org/10.5281/zenodo.22962557) | Spintronic Octonionic Tensor Processor (SOTP) |

Text je v [`PAPER.cs.md`](PAPER.cs.md), anglicky v [`PAPER.md`](PAPER.md).

**Algebra je správná**, což je proti autorovým dřívějším pracím změna: orientovaná
Fanova rovina v SOTP rov. (3) je jedna z pouhých 16 ze 128 možných orientací těch
sedmi přímek, které dávají normovanou divizní algebru, a překážka tenzorového
součinu v CQFT §2.1 je popsaná správně. Všechny vady jsou v přechodu od algebry
k hardwaru a ta hlavní je, že asociátor — který SOTP nazývá „nenulovou hardwarovou
observablou" — je identicky nulový přesně na těch sedmi trojicích, ze kterých je
pole hradel podle Fanovy roviny postavené.

> Komentáře v kódu a výpisy skriptů jsou anglicky. Anglická verze je
> v [`README.md`](README.md) a [`PAPER.md`](PAPER.md).

## Co je potřeba

```
python3 -m pip install -r requirements.txt   # jen numpy
```

Žádná grafická karta, žádná síť, žádné stahování modelů.

## Reprodukce výsledků

```
./run_all.sh          # všechno, asi minuta na libovolném CPU
```

| Skript | Co spočítá | Čas |
|---|---|---|
| `fano.py` | platnost publikované orientace Fanovy roviny; kolik ze 128 orientací funguje | 20 s |
| `associator.py` | co přečtou „Associator Verification Nodes"; které trojice se nulují; trilinearita | 10 s |
| `closure.py` | jestli je součin dvou fyzikálně přípustných stavů přípustný, pro SOTP a PCTP | 25 s |
| `cqft.py` | ⊠ jako tenzorový součin; zapsatelnost provázanosti; simulace Causal Hysteresis Testu | 3 s |
| `hardware.py` | Landauerův rozpočet, izolace, energie fotonů vs. NV, spinová difuzní délka, škála QCD, frame dragging | 1 s |

Celý výstup jednoho běhu: [`results.log`](results.log).

## Klíčová čísla

| co | publikováno | naměřeno / spočítáno |
|---|---|---|
| orientace Fanovy roviny dávající divizní algebru | — | 16 ze 128; publikovaná je platná |
| asociátor v uzlu na třech spinových kanálech | „nenulová hardwarová observabla" | **1,07·10⁻¹⁵, nenulový v 0,0000 % z 20 000 trojic** |
| trojice imaginárních jednotek s nulovým asociátorem | — | 7 z 35 — přesně těch 7 přímek Fanovy roviny, ze kterých jsou hradla |
| SOTP: součin dvou přípustných stavů je přípustný | předpokládáno | **0,0000 %** (Q_top součinu v rozsahu [−16,6; +16,5]) |
| PCTP: totéž pro optické mapování | předpokládáno | **0,0000 %** (náboj OAM celočíselný v 0,0000 %) |
| změna redukovaného stavu fotonu B v navrženém experimentu | „měřitelný fázový posun" | **6,8·10⁻¹⁸**, v nejhorším případě 4,6·10⁻¹⁶ na 20 000 párech |
| PCTP, energie na bit vs. Landauer | „téměř nulová" | 925 ×, se zdrojem 4,6·10³ × |
| PCTP, Faradayova izolace | > 35 dB | 19,5 dB v jeho vlastní citaci |
| NV latch pumpovaný na 1550 nm | funguje | 0,800 eV proti bezfononové linii 1,946 eV |
| SOTP, vzdálenost spinového routingu | přes čip | spinová difuzní délka 2–3 nm, faktor 3·10⁵ |
| SOTP, modulace chirálního kondenzátu | uskutečnitelné | 41 µeV proti Λ_QCD ≈ 200 MeV, faktor 5·10¹² |
| SOTP, frame dragging setrvačníkem | měřitelné | 7·10⁷ pod výsledkem Gravity Probe B |

## Doprovodná vyhodnocení

- [`octonion-mppt-eval`](https://github.com/karagos01/octonion-mppt-eval) — oktonionová dvouvrstvá šablona s asociátorem a magnonová tvrzení
- [`xternary-eval`](https://github.com/karagos01/xternary-eval) — 2bitový inferenční engine pro LLM
- [`openql-eval`](https://github.com/karagos01/openql-eval) — tenzorová maticová architektura openQL / openOL z října 2026

## Licence

Kód (všechny `*.py` a `run_all.sh`): MIT, viz `LICENSE`.
Text `PAPER.md` a `PAPER.cs.md`: CC BY 4.0.
