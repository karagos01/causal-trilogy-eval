# Asociátor je nulový na každém hradle: vyhodnocení „Causal Field trilogy"

**karagos01**, září 2026

Nezávislé vyhodnocení tří preprintů, které 25. září 2026 vystavili na Zenodu
M. Mazgal a Gemini AI:

| | DOI | název |
|---|---|---|
| I | [10.5281/zenodo.22959886](https://doi.org/10.5281/zenodo.22959886) | The Causal Quaternionic Field Theory (CQFT) |
| II | [10.5281/zenodo.22962188](https://doi.org/10.5281/zenodo.22962188) | Photonic Causal Tensor Processor (PCTP) |
| III | [10.5281/zenodo.22962557](https://doi.org/10.5281/zenodo.22962557) | Spintronic Octonionic Tensor Processor (SOTP) |

## Abstrakt

Ty tři práce navrhují nemarkovovskou kvaternionovou teorii pole a dvě procesorové
architektury na ní postavené. Tohle vyhodnocení kontroluje to, co se dá spočítat.
Algebra je správná, což je proti autorovým dřívějším pracím změna: orientovaná
Fanova rovina vytištěná v SOTP rov. (3) je jedna z pouhých 16 ze 128 možných
orientací těch sedmi přímek, které dávají normovanou divizní algebru, a překážka
kvaternionového tenzorového součinu popsaná v CQFT §2.1 je popsaná správně. Vady
jsou všechny v přechodu od algebry k hardwaru a ta hlavní je strukturní: asociátor,
který SOTP nazývá „nenulovou hardwarovou observablou", je identicky nulový přesně
na těch sedmi trojicích bázových jednotek, ze kterých je pole hradel podle Fanovy
roviny postavené — a zejména na těch třech spinových kanálech, kam §4.2 umisťuje
své Associator Verification Nodes. Kromě toho stavový prostor není uzavřený na
operaci, kterou hardware musí provádět — 0,0000 % součinů dvou fyzikálně
přípustných stavů je samo přípustné, a to v obou architekturách — kauzální index τ
nevstupuje do žádné počítané veličiny, operátor ⊠ není tenzorový součin a neumí
vůbec zapsat dvoučásticový stav, a vlastní falzifikační experiment CQFT je porušení
no-signalling teorému, jehož „ladicí" krok je pro stav, který sám předepisuje,
prázdný. Pět hardwarových tvrzení se míjí faktorem od 35 do 5·10¹².

Všechno níž reprodukuje `./run_all.sh` (jen CPU, bez sítě, asi minuta).

## 1. Co je správně

Patří to na začátek, protože je to nové. Autorovy dřívější preprinty obsahovaly
aritmetiku, která kontrolu nepřežila. Tyhle ano.

**Orientace Fanovy roviny.** SOTP rov. (3) zafixuje strukturní konstanty oktonionů
vypsáním sedmi orientovaných triád. Množina těch sedmi přímek je Fanovou rovinou
vynucená, ale orientace ne: je 2⁷ = 128 možností a `fano.py` je projde všechny.
Normovanou divizní algebru dává jen **16 ze 128**. Publikovaná orientace je jedna
z těch šestnácti. Její multiplikativní tabulka splňuje |XY| = |X||Y| na 5·10⁻¹⁶
relativně na 4000 náhodných párech, je alternativní se stejnou přesností a nemá
dělitele nuly. Pro srovnání: ty samé sedmy přímky zapsané s triádami ve vzestupném
pořadí — což je ta volba, která vypadá samozřejmě — dávají algebru, která porušuje
multiplikativitu normy až o 60 % a má explicitní dělitele nuly. Obsah nese
orientace, a tu má správně.

**Překážka tenzorového součinu.** CQFT §2.1 argumentuje, že bilinearita
s kvaternionovými skaláry vynucuje −(k ⊗ k) = i ⊗ i pro c = j, A = i, B = k.
Protože ji = −k a jk = i, je to přesně tak a je to poctivá formulace té klasické
obtíže (Adler 1995).

**Materiály.** Si₃N₄ je správně preferovaný před SOI z uvedených důvodů (zakázaný
pás ≈5 eV, chybějící dvoufotonová absorpce, <0,1 dB/cm na 1550 nm). Ce:YIG je
správný magnetooptický granát, Pt a W správné spin-Hallovy kovy, CoFeB na těžkém
kovu správná vrstva pro mezivrstvové DMI. Ty součástky existují a ty volby nejsou
nahodilé.

Pro čtení toho, co následuje, je to důležité: ty chyby nejsou neznalost
literatury. Jsou to chyby toho kroku, ve kterém se matematika připojuje k fyzice —
a ten krok nikdo nezkontroloval.

## 2. Asociátor je nulový na každém hradle

SOTP staví architekturu z **triádových hradel uspořádaných podle grafu Fanovy
roviny** (§4.2) a umisťuje **Associator Verification Nodes** „do průsečíku tří
spinových kanálů", kde je asociátor „nenulová hardwarová observabla, která
uchovává kontextové seskupení minulých interakcí" (§2.2).

Tabulka 1 v SOTP mapuje e₁, e₂, e₃ na tři složky spinové polarizace σx, σy, σz.
Spolu s e₀ generují kvaternionovou podalgebru 𝕆, a kvaterniony jsou asociativní.
`associator.py` měří, co ten uzel přečte:

| na kterých směrech leží tři vstupy | průměr \|[A,B,C]\| | podíl ≠ 0 |
|---|---|---|
| celý oktonion, e₀…e₇ | 2,26·10¹ | 1,0000 |
| **jen spinové kanály, e₀,e₁,e₂,e₃ — §4.2** | **1,07·10⁻¹⁵** | **0,0000** |
| spin + skyrmionový náboj, e₀…e₄ | 6,36 | 1,0000 |

Na 20 000 náhodných trojicích ten uzel čte nulu na úrovni strojové přesnosti. Není
to vlastnost jen té spinové trojice. Z 35 trojic různých imaginárních jednotek má
28 nenulový asociátor a **7 se nuluje — a těch 7 je přesně 7 přímek Fanovy
roviny** (v `associator.py` ověřeno po jedné). Každá čtyřrozměrná podalgebra
generovaná e₀ a jednou přímkou Fanovy roviny má max |asociátor| < 10⁻¹⁴.

Ta architektura je tedy hradlo po hradle složená právě z těch sedmi konfigurací,
ve kterých je její centrální observabla identicky nulová. Aby hradlo přečetlo
nenulový asociátor, muselo by kombinovat bázové jednotky, které *neleží* na
společné přímce Fanovy roviny — čili nesmělo by to být triádové hradlo.

Asociátor navíc nese méně informace, než práce předpokládá. Je trilineární, takže
|[sA, sB, sC]| = s³|[A,B,C]| přesně (ověřeno na 12 desetinných míst pro
s = 1, 2, 5, 10). Jako výstup ho dominuje velikost stavu, ne jeho „historie
seskupení".

## 3. Stavový prostor není na té operaci uzavřený

Procesor může spočítat X ⊠ Y jen tehdy, když je výsledek stav, který hardware umí
držet. Obě práce mapují algebraické souřadnice na fyzikální veličiny s tvrdými
omezeními. `closure.py` vygeneruje 200 000 párů fyzikálně přípustných stavů
a vynásobí je.

**SOTP.** Tabulka 1 přiřazuje e₄ skyrmionovému topologickému náboji Q_top,
explicitně „Q = ±1"; e₁,e₂,e₃ spinové polarizaci, |σ| ≤ 1; e₆ valleyové polarizaci
v [−1, 1].

| omezení, které má splňovat součin | splněno |
|---|---|
| \|σ\| = 1 na (e₁,e₂,e₃) | 0,0000 % |
| Q_top je pořád celé číslo ±1 | 0,0000 % |
| valleyová polarizace v [−1,1] | 17,53 % |
| všechna tři zároveň | **0,0000 %** |

Q_top součinu má průměr −0,014 a směrodatnou odchylku 4,45, v rozsahu
[−16,6; +16,5]. 82,5 % součinů vyžaduje skyrmion s |Q| > 1 a 14,0 % vyžaduje
neceločíselné vinutí. Topologický náboj je celé číslo *proto*, že je topologický;
nemůže nabýt hodnoty 0,37. Operace, pro kterou je ten hardware postavený, opouští
stavový prostor prakticky na každém vstupu.

**PCTP.** §3 mapuje q_a na amplitudu a fázi nosné, q_i a q_j na Stokesovy
parametry S₂ a S₃ a q_k na topologický náboj OAM l ∈ ℤ.

| omezení, které má splňovat součin | splněno |
|---|---|
| náboj OAM l je pořád celé číslo | 0,0000 % |
| \|(S₂,S₃)\| ≤ 1 | 8,82 % |
| amplituda v [0,1] | 10,89 % |
| všechna tři zároveň | **0,0000 %** |

Nezávisle na tom nevychází ani počet stupňů volnosti. Jeden koherentní vlnový
paket nese amplitudu (1) + fázi nosné (1) + bod na Poincarého sféře (2) +
celočíselný náboj OAM (1, diskrétní). Rovnice (6) přiřazuje jediné reálné
souřadnici q_a *obojí*, amplitudu i fázi, a S₁ vypadává úplně. To zobrazení není
injektivní, takže z toho světla se ten kvaternion nedá zpátky přečíst.

## 4. Kauzální index nedělá nic

CQFT rov. (2) a SOTP rov. (4) definují (X₁,τ₁) ⊠ (X₂,τ₂) = (X₁X₂, τ₁ ≺ τ₂).
Hodnotová složka je X₁X₂ pro každé přiřazení τ₁ a τ₂; `cqft.py` potvrzuje, že čtyři
různá přiřazení dají jednu jedinou hodnotu. τ zaznamenává pořadí, ve kterém už byly
operandy napsané, a do žádné počítané veličiny nevstupuje.

Každá předpověď, kterou ty tři práce z ⊠ vyvozují, je tedy předpovědí obyčejného
kvaternionového nebo oktonionového násobení — Hamilton 1843, Graves 1843,
Cayley 1845. „Odmítnutí zaměnitelnosti číselných hodnot" přidává k pořadí operandů
značku, kterou ta notace už nesla. A nekomutativita není pro kvantovou mechaniku
nic nového: operátory standardní teorie jsou matice a nikdy nekomutovaly.

## 5. ⊠ není tenzorový součin a neudrží provázaný stav

Deklarovaným účelem ⊠ je „vyřešit problém tenzorového součinu". Jeho signatura je
ℍ × ℍ → ℍ: osm reálných vstupů, čtyři reálné výstupy. Tenzorový součin dvou
čtyřrozměrných prostorů má dimenzi 16. Předobraz každého součinu je
čtyřparametrická rodina — `cqft.py` ukazuje šest různých vstupních párů se stejným
součinem — takže polovina vstupu se při každém použití zničí a operace není
invertibilní.

Důsledek pro §3.2, která reinterpretuje provázanost, je fatální. CQFT rov. (4) píše
Ψ_AB = (q_A, τ₀) ⊠ (q_B, τ₀), tedy jeden kvaternion. V `cqft.py` dávají (1) ⊠ (i)
a (j) ⊠ (−k) tentýž stav až na znaménko. Ten formalismus nemá reprezentaci pro
korelaci mezi dvěma podsystémy, a tedy ani pro provázanost, což je přesně jev,
o kterém ta sekce je.

## 6. Navržený experiment nic nerozliší

CQFT §5 navrhuje *Causal Hysteresis Test*: provázaný pár, foton A poslaný jednou
cestou přes X̂ a pak Ŷ a druhou přes Ŷ a pak X̂, naladěné tak, aby výsledná
polarizace A na reálné ose byla stejná. „Standardní kvantová mechanika předpovídá
identické statistické korelace pro foton B v obou scénářích. CQFT předpovídá
deterministický, měřitelný fázový posun na fotonu B."

Simulováno v `cqft.py` na Bellově stavu, X̂ a Ŷ jako rotace o 0,7 a 1,3 rad kolem
ortogonálních os:

- ty dvě cesty dávají skutečně různé společné stavy, ‖p₁ − p₂‖ = 0,415;
- redukovaná matice hustoty fotonu B se liší o **6,8·10⁻¹⁸** — tedy přesně nula;
- na 20 000 náhodných nekomutujících párech lokálních unitárních operací je
  největší rozdíl v ρ_B 4,6·10⁻¹⁶.

Žádná operace na A, v žádném pořadí, nezmění nic měřitelného na samotném B. Není to
náhoda parametrů, je to no-signalling teorém (Ghirardi, Rimini a Weber 1980;
Eberhard a Ross 1989). „Měřitelný fázový posun na fotonu B" je signál a byla by to
komunikace nadsvětelnou rychlostí.

Dva další problémy. Ten ladicí krok je prázdný: u maximálně provázaného páru je
foton A úplně nepolarizovaný bez ohledu na to, co se s ním lokálně dělá, a simulace
dává ‖ρ_A¹ − ρ_A²‖ = 0,000000 bez jakéhokoli ladění. A předpověď připsaná
standardní kvantové mechanice je taky špatně — QM předpovídá, že se budou lišit
*společné* korelátory, a to o −0,227 a +0,472 ve dvou ze tří vyzkoušených
měřicích konfigurací. Ten experiment tedy nerozlišuje nikde: kde je rozdíl
pozorovatelný, předpovídá ho i standardní QM; kde standardní QM žádný nepředpovídá,
je signatura CQFT zakázaná.

## 7. Hardwarová tvrzení proti jejich vlastním konstantám

Z `hardware.py`.

| tvrzení | jak je publikované | spočítáno | faktor |
|---|---|---|---|
| PCTP, „téměř nulová produkce termodynamické entropie" | ≈ Landauer | jediný foton na 1550 nm je sám 44,6 × kT ln2; 20,7 fotonu na bit na výstřelové hranici pro BER 10⁻⁹ je 925 ×; se zdrojem s 20 % účinností 4,6·10³ × | **10³–10⁴** |
| PCTP, Faradayova izolace | > 35 dB | 19,5 dB naměřeno v jeho vlastní citaci (Bi a kol. 2011), a to na platformě s vyšším indexem | **35 × ve výkonu** |
| PCTP, NV latch pumpovaný evanescentním polem na 1550 nm | funguje | vedený foton má 0,800 eV, bezfononová linie NV⁻ je 1,946 eV; diamant je na 1550 nm průhledný | **žádná absorpce** |
| SOTP, „čisté spinové proudy s J_c = 0", disipace „True Zero" | nula | rov. (7) je J_s = (ℏ/2e)·θ_SH·(J_c × σ), takže J_c = 0 dává J_s = 0; jedno SOT přepnutí při 5·10¹¹ A/m² disipuje 3,75 fJ v platině | **1,3·10⁶ × Landauer** |
| SOTP, Fanova mřížka přes čip nesená čistým spinovým proudem | mm | spinová difuzní délka 2–3 nm v Pt/W/CoFeB, ≈20 nm v povrchových stavech Bi₂Se₃ | **3·10⁵** |
| SOTP §6.1, modulace chirálního kondenzátu ⟨q̄q⟩ | uskutečnitelné | kvantum spinové vlny o 10 GHz je 41 µeV proti Λ_QCD ≈ 200 MeV | **5·10¹²** |
| SOTP §6.2, frame-dragging setrvačníkem | měřitelné | 1 kg, 10 cm, 10⁵ ot/min dává Ω_LT = 7,8·10⁻²³ rad/s; Gravity Probe B naměřila 5,7·10⁻¹⁵ rad/s čtyřmi SQUID gyroskopy při 1,8 K | **7·10⁷ pod nejmenším kdy naměřeným** |

Dvě z nich jsou vnitřní protiřečení, ne chyby v řádu. Rovnice (7) vyvrací větu
vytištěnou nad sebou. A tabulka 1 v PCTP uvádí disipaci jako „téměř nulovou
(geometrická fáze)", zatímco §3 předepisuje elektrooptické fázové posouvače
z LiNbO₃; geometrická fáze a elektrooptický modulátor nejsou tatáž součástka.
Tabulka 1 taky uvádí latenci jako „okamžitý optický transit", zatímco §3 definuje
kauzální index τ jako fyzickou podélnou hloubku průchodu — pokud je transit
okamžitý, τ neexistuje.

Tvrzení o SAF „imunitě vůči parazitním magnetickým polím až do 10 T" potřebuje
J_ex ≈ 5,6 mJ/m² přes rutheniovou vrstvu, na samé horní hranici publikované vazby
Co/Ru. Není tak špatné jako spíš irelevantní: rozptylová pole v zapouzdřeném čipu
jsou mikrotesly až militesly, čtyři až sedm řádů pod tou uvedenou hodnotou.

## 8. Tvrzení o standardním modelu

SOTP §1 a §6.1 stojí na „přirozeném izomorfismu" oktonionů „s kalibrační grupou
standardního modelu" a tvrdí, že „8D oktonionová algebra se přirozeně projektuje na
Gell-Mannovy matice SU(3)_C". dim 𝕆 = 8, z toho 7 imaginárních jednotek; dim su(3)
= 8 generátorů. To jsou různé objekty — dimenze algebry a dimenze Lieovy algebry —
a shoda čísla 8 není projekce. Skutečný vztah je, že Aut(𝕆) = G₂ o dimenzi 14 a
SU(3) vzniká jako podgrupa fixující jednu imaginární jednotku. Furey (2016),
citovaná jako opora, pracuje s levou adjungovanou akcí komplexifikovaných
oktonionů na sebe, ne s osmi souřadnicemi oktonionového stavu; v té konstrukci není
nic, co by dovolilo vektoru magnetizace modulovat barevné pole.

Závěrečný slib šestnáctirozměrných sedenionů je sebevyvracející v pojmech té práce
samé: správně poznamenává, že sedeniony mají dělitele nuly, a to je přesně ta
vlastnost, která je činí nepoužitelnými jako stavový prostor procesoru, jehož
výstupem je norma.

## 9. Co se změnilo

V autorových dřívějších preprintech neprošla kontrolu už samotná matematika. Tady
prochází — a obě hardwarové práce uvádějí Gemini AI jako spoluautora za
„Mathematical Synthesis & System Modeling", zatímco lidský autor je uvedený za
„Conceptualization & Hardware Architecture". To rozdělení práce je na výsledku
vidět: algebra je čistá a všechny vady jsou teď v tom fyzikálním mapování.
Delegování formální vrstvy zvedlo podlahu pod rovnicemi a nechalo nedotčený ten
krok, který rozhoduje, jestli je práce o něčem — která fyzikální veličina se
identifikuje s kterým symbolem a jestli ta identifikace přežije kontakt s tím, že
topologický náboj je celé číslo, že diamant na 1550 nm neabsorbuje nebo že spinový
proud umře do tří nanometrů.

Je to tentýž způsob selhání, jaký je naměřený v autorových ostatních pracích, kde
se optimalizovaná veličina ukázala být nekorelovaná s deklarovaným cílem. Rozdíl
je, že teď je to hůř vidět, protože okolní formalismus je správný.

## 10. Omezení

Tohle vyhodnocení je celé analytické a numerické. Nebylo vyrobeno žádné zařízení
a žádný materiálový parametr tady nebyl naměřen; spinové difuzní délky, izolační
poměr, hladinová struktura NV a výsledek Gravity Probe B jsou z citované
publikované literatury a vlastní čísla těch dvou preprintů se používají všude, kde
je uvádějí. Test uzavřenosti v §3 předpokládá omezení, která si ty práce napsaly
samy (Q = ±1, l ∈ ℤ, |σ| ≤ 1); jiná normalizační konvence by změnila procenta, ale
ne závěr, že se ta omezení nezachovávají, protože kvaternionové ani oktonionové
násobení nezachovává celočíselnost jedné souřadnice při žádném škálování. Simulace
v §6 používá qubity místo plných optických modů, což je standardní redukce pro
polarizačně provázaný pár a nemá vliv na výsledek o no-signalling, který platí pro
libovolnou lokální operaci na libovolném Hilbertově prostoru.

## 11. Dostupnost dat

Skripty, celý výstup (`results.log`) a tento text:
<https://github.com/karagos01/causal-trilogy-eval>. Ty tři preprinty jsou volně
dostupné pod CC BY 4.0 na uvedených DOI. Doprovodná vyhodnocení dalších prací
téhož autora: <https://github.com/karagos01/octonion-mppt-eval> a
<https://github.com/karagos01/xternary-eval>.

## Literatura

1. Adler, S. L. *Quaternionic Quantum Mechanics and Quantum Fields.* Oxford University Press (1995).
2. Allen, L., Beijersbergen, M. W., Spreeuw, R. J. C. a Woerdman, J. P. Orbital angular momentum of light and the transformation of Laguerre-Gaussian laser modes. *Phys. Rev. A* **45**, 8185 (1992).
3. Baez, J. C. The octonions. *Bull. Amer. Math. Soc.* **39**, 145–205 (2002).
4. Bi, L. a kol. On-chip optical isolation in monolithically integrated non-reciprocal optical resonators. *Nature Photonics* **5**, 758–762 (2011).
5. Doherty, M. W. a kol. The nitrogen-vacancy colour centre in diamond. *Physics Reports* **528**, 1–45 (2013).
6. Eberhard, P. H. a Ross, R. R. Quantum field theory cannot provide faster-than-light communication. *Found. Phys. Lett.* **2**, 127–149 (1989).
7. Everitt, C. W. F. a kol. Gravity Probe B: Final results of a space experiment to test general relativity. *Phys. Rev. Lett.* **106**, 221101 (2011).
8. Fert, A., Reyren, N. a Cros, V. Magnetic skyrmions: advances in physics and potential applications. *Nature Reviews Materials* **2**, 17031 (2017).
9. Furey, C. *Standard Model Physics from an Algebra?* Disertace, University of Waterloo (2016). arXiv:1611.09182.
10. Ghirardi, G. C., Rimini, A. a Weber, T. A general argument against superluminal transmission through the quantum mechanical measurement process. *Lettere al Nuovo Cimento* **27**, 293–298 (1980).
11. Landauer, R. Irreversibility and heat generation in the computing process. *IBM J. Res. Dev.* **5**, 183–191 (1961).
12. Manchon, A. a kol. Current-induced spin-orbit torques in ferromagnetic and antiferromagnetic systems. *Rev. Mod. Phys.* **91**, 035004 (2019).
13. Schmiegelow, C. T. a kol. Transfer of optical orbital angular momentum to a bound electron. *Nature Communications* **7**, 12998 (2016).

---

*Tento text je pod CC BY 4.0, kód pod MIT. Ani jedno není schváleno autorem
vyhodnocovaných preprintů.*
