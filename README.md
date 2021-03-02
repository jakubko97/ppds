# Info

- V súbore fibonacci.py sa nachádzajú dané komentáre ku kódu.
- Vypracovanie som robil vo Visual Studio Code, tak je dosť možné, že Vám komentáre možno nebudú dobre sedieť.

# Otázky na zamyslenie (odpovede očakávam vo vypracovaní):

- Pre vypracovanie tohto zadania som použil N semafórov, kde N je počet vlákien. Mutex som použil len pri zdielanej triede Shared.
- Bariéru a signalizáciu som využil tak, že pri poslednom vlákne sa uvolni n-1 vlákien. Kde postup sa opakuje,až kým nenastane podmienka, ktorá vyhodnotí že zdielaný index sa rovná dĺžky poľa, ktorý sme zadali.
