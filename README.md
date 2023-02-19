# Mielialasovellus

Sovelluksen perusidea pohjaa mielenterveystalon sivuilta löytyvään harjoitukseen: https://www.mielenterveystalo.fi/fi/omahoito/tietoinen-lasnaolo/12-toiminta-ja-mieliala

Sovelluksen tarkoitus on antaa vaihtoehto mielialan kohottamiseen ja seurata, millaisia vaikutuksia kullakin toiminnalla on ollut mielialaan. Käyttäjä saa joko valita mieluisan vaihtoehdon tai pyytää sovellusta arpomaan soveltuvan tehtävän. 

Sovelluksen ominaisuuksia: 
- Käyttäjä voi antaa numeerisen arvion päivän tämänhetkisestä mielialastaan. 
- Käyttäjä voi nähdä listauksen tarjolla olevista toiminnoista
- Käyttäjä voi suodattaa listaa antamillaan parametreilla (hinta, kesto, toiminnan tyyppi), nähden tilanteelle sopivat, tarjolla olevat aktiviteetit
- Käyttäjä voi lisätä itselleen tarjolla olevia aktiviteetteja tai piilottaa itseltään globaaleja tehtäviä
- Käyttäjä voi seurata oman mielialansa kehittymistä
- Käyttäjä voi antaa arvion siitä, kohottiko vai laskiko toiminta mielialaa
- Ylläpitäjä voi lisätä kaikille saatavilla olevia aktiviteetteja
- Ylläpitäjä voi nähdä globaalien toimintojen vaikutuksista mielialaan

Sovelluskehityksen tilanne

Tietokantataulut
- Luotu, poislukien oman mielialan taulu (mahdollista, että jää pois kokonaan)
- Ongelmakohta: paikallisessa tuotannossa en ole päässyt testaamaan kirjautumista - herjaa että users-taulukkoa ei ole

HTML-sivut
- Kirjautuminen, rekisteröityminen käytännössä valmiita. 
- Muita ei ole testattu, johtuen tietokantatauluissa mainitusta ongelmakohdasta, mutta sivut pääsääntöisesti luotu

Funktiot
- Uuden aktiviteetin lisääminen, käyttäjän luominen ja kirjautuminen valmiita
- Aktiviteettien valinta hyvällä mallilla
- Arvostelujen tekeminen aloitettu
- Reitityksessä parannettavaa
