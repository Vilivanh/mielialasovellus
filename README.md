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

## Sovelluskehityksen tilanne:

**TIETOKANTATAULUT**
- Luotu
- Vaikutusten kohdentaminen ko. käyttäjälle puuttuu
- Kommentointi mielialoihin olisi kiva lisä

**HTML-sivut**
- Valmiita nykyisille ominaisuuksille

**Funktiot**
- Funktioita voisi siirtää enemmän omikseen, pois reitityksen alta
- Supervisor-komennot puuttuvat

## SOVELLUKSEN KÄYNNISTÄMINEN 

Koska fly.io-käynnistäminen ei ole toiminut, pitää sovellus käynnistää paikallisesti. 

Lataa repositorio omalle koneellesi. Luo sovellukseen kansio .env ja kopioi kansioon seuraavat tiedot: 

```
DATABASE_URL = postgresql:///<käyttäjä>
SECRET_KEY = <secret_key>
```

jossa <käyttäjä> sekä <secret_key> pitää korvata omalla käyttäjänimellä ja itse asettamallasi salaisella avaimella.

Käynnistä sovellusta varten virtuaaliympäristö

```
python3 -m venv venv
source venv/bin/activate
```

Lataa sovelluksen käynnistämiseen tarvittavat paketit (ei tarpeen, jos koneessa ovat jo vaadittavat tiedot)
```
pip install -r requirements.txt
```
Käynnistä tietokanta

```
start-pg.sh
```
siirry tulkkiin komennolla

```
psql
```

Luo tietokanta komennolla

```
CREATE DATABASE <database_name>
```

Valitse tietokannalle itse valitsemasi nimi ja aseta se kohtaan <database_name>
Aseta sovelluksen tietokanta luomaasi tietokantaan komennolla

```
psql -d <database_name> < schema.sql
```

Tietokannan ollessa käynnissä käynnistä sovellus komennolla

```
flask run 
```

Avaa verkkoselain, itselläni sovellus löytyy osoitteesta http://127.0.0.1:5000
