# 6. Týždeň

# Pre tento týždeň som sa rozhodol vypracovať problém v holičstve.

Tento problém sa riešil vzájomnou signalizáciou medzi zákazníkom a barberom. Kód je naprogramovaný tak, že zákazníci prichádzaju a "sadajú" do čakárne až kým nebude plno. Ak je plna čakáreň, zákazník odíde a vráti sa neskôr. Pojem "sadnutia" v čakárni sa riešil pomocou FIFO fronty. Tu je potrebné, aby zákaznici sa išli strihať v poradí v akom prišli do čakárne (fronty). To som vyriešil spôsobom, že inicializoval som si semafór barbera pre každé vlákno a vďaka tomu je možné vo funkcií barbera, dať signál zákaznikovi ktorý je na rade, že sa môže ísť strihať. Môžem si to tak imaginárne prestaviť, že keď zákaznik vôjde do čakárne holičstva, dostane lístok (semafor) a ten lístok sa appende do fronty. Barber ak bude pripravený, pozrie sa aký lístok vytiahne (pop), tak ten dany zákaznik dostane signál že môže dostať účes:D (getHaircut). Ak sa dostrihá, zákazník odíde a dekrementuje customers lenght.

Inicializované hodnoty v kóde:

1. customers = 10
2. barbers = 2
3. max size in barbershop = 5