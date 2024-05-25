Actualizarea aplicatiilor la distanta:

* Pe server exista o serie de aplicatii executabile, lista care nu se modifica pe durata rularii procesului server;
* Clientii se conecteaza la server si solicita lista acestora;
* Un client poate solicita descarcarea unei aplicatii;
* Server-ul mentine o lista cu toate aplicatiile descarcate de un client;
* Pe server se pot publica noi versiuni ale unei aplicatii prin suprascrierea celei existente;
* In acest caz, server-ul trimite tuturor clientilor care au descarcat aplicatia respectiva noua versiune;
* In cazul in care aplicatia ruleaza pe client, acesta salveaza versiunea primita si reincearca s-o suprascrie pe cea veche pana reuseste.

Pentru a testa functionalitatile acestei mini aplicatii, folosim script-uri `.py` drept aplicatii executabile.

