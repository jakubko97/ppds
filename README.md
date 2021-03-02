# 1 Vypínač

Implementujte ADT Lightswitch. ADT Lightswitch nech poskytuje 2 metódy: lock a unlock podľa nasledovnej špecifikácie:

1. lock(semaphore)
2. unlock(semaphore)
Interný stav ADT Lightswitch je daný počítadlom counter a mutexom mutex, ktorý chráni integritu počítadla.

Správanie ADT Lightswitch:

1. Ak vlákno zavolá metódu lock, a toto vlákno je prvým, ktoré sa pokúša „dostať do miestnosti“, nech vyvolá nad semaforom, ktorý je argumentom funkcie lock, operáciu wait().
2. Ak vlákno zavolá metódu unlock, a toto vlákno je posledným, ktoré sa pokúša „dostať z miestnosti“, nech vyvolá nad semaforom, ktorý je argumentom funkcie unlock, operáciu signal().
Na jednoduchom príklade overte funkčnosť svojej implementácie. Tento ADT správne využite v niektorej z nasledovných úloh.

# 2 Producent-Konzument
 

Implementujte riešenie problému Konzument-Producent. Experimentujte s rôznymi nastaveniami systému:

- čas produkcie výrobku,
- čas spracovania výrobku,
- počet konzumentov,
- počet producentov,
- veľkosť úložiska (skladu).
Skúste experimentálne zistiť, aké parametre sú optimálne pre váš systém. Kritériom optimality nech sú:

Počet vyrobených výrobkov za jednotku času (v akom vzťahu sú čas produkcie výrobku, veľkosť úložiska, počet producentov a počet konzumentov?),
počet spracovaných výrobkov za jednotku času (v akom vzťahu sú čas spracovania výrobku, veľkosť úložiska, počet producentov a počet konzumentov?).
V prípade experimentov priemerujte hodnoty 10 opakovaní experimentu pri rovnakých nastaveniach systému; grafy vykresľujte aspoň pre 100 rôznych nastavení modelovaného systému.

# 3 Čitatelia-Zapisovatelia
 
Podobne ako v prípade problematiky Producentov-Konzumentov, aj tu experimentujte s rôznymi nastaveniami systému. Implementujte dve verzie riešenia tohto problému:

1. bez riešenia vyhladovenia zapisovateľov,
2. s riešením problému vyhladovenia zapisovateľov.
Experimentujte s nasledovnými parametrami systému, a hľadajte medzi nimi závislosti:

1. počet čitateľov,
2. počet zapisovateľov,
3. doba čítania,
4. doba zápisu.
5. Pre aký počet čitateľov s danou priemernou dobou čítania sa prejavuje problém vyhladovenia?
6. Má počet zapisovateľov vplyv na schopnosť čitateľov dostať sa k údajom a prečítať ich?
7. Je možné, aby sa prejavilo vyhladovenie aj u čitateľov?
8. Ak doplníme implementáciu o turniket, aby neprišlo k vyhladoveniu zapisovateľov, vieme rozhodnúť, ktorý z kódov zo záveru prednášky je lepší?
9. Pre daný počet čitateľov, priemernú dobu čítania, priemernú dobu zápisu vieme určit optimálny počet zapisovateľov?
10. Ak máme danú priemernú dobu zápisu a priemernú dobu čítania, vieme vykresliť graf závislosti medzi počtom zapisovateľov a optimálnym počtom čitateľov (aby sme mohli nasadiť čo najviac čitateľov bez toho, aby prichádzalo k vyhladoveniu zapisovateľov). Vieme urobiť experiment, v ktorom sa bude meniť aj priemerná doba zápisu (mali by sme dostať trojrozmerný graf)?
Podobne ako pri probléme producent-konzument, aj pri týchto experimentoch opakujte merania aspoň 10x pre rovnaké nastavenie systému, a výsledky priemerujte; grafy vykresľujte aspoň pre 100 rôznych nastavení modelovaného systému.

Pri písaní kódu dbajte na prehľadnosť, samočitateľnosť, modularitu a znovupoužiteľnosť kódu. Dodržiavajte štandard [PEP8](https://www.python.org/dev/peps/pep-0008/). Vhodne využívajte možnosť komentovania kódu, viď štandard [PEP257](https://www.python.org/dev/peps/pep-0257/).
