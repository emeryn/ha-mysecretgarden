# 🌻 My Secret Garden - Intégration Home Assistant

Bienvenue dans l'intégration officielle de **My Secret Garden** pour Home Assistant ! 

Cette intégration fait le pont entre votre application de gestion de potager (Vue.js/FastAPI) et votre maison connectée. Elle permet à Home Assistant de connaître en temps réel les besoins en eau de vos plantes et d'automatiser votre système d'arrosage (électrovannes, pompes, etc.).

## ✨ Fonctionnalités

Pour chaque **Bac de culture** et **Plante en pot** dessinés dans votre application, Home Assistant créera automatiquement un "Appareil" dédié contenant :

* 💧 **Capteur d'alerte arrosage** (`binary_sensor`) : Passe à l'état *Problème / Activé* lorsque la plante ou le bac a soif (selon la météo, la variété et la saison gérées par l'app).
* 🌱 **Capteur de quantité** (`sensor`) : Affiche le nombre de plants actuellement en terre dans un bac.
* 🚿 **Bouton de validation** (`button`) : Permet de signaler à l'application que l'arrosage a été effectué pour réinitialiser les chronomètres virtuels.

## ⚠️ Prérequis

* L'application serveur **My Secret Garden (FastAPI)** doit être en cours d'exécution sur votre réseau local (ex: via Docker/Proxmox).
* Vous devez connaître l'adresse IP locale et le port de ce serveur (ex: `http://192.168.1.50:8000`).

---

## 📥 Installation (via HACS)

1. Ouvrez **HACS** dans Home Assistant.
2. Allez dans **Intégrations**.
3. Cliquez sur les 3 petits points (en haut à droite) > **Dépôts personnalisés**.
4. Ajoutez l'URL de ce dépôt GitHub et choisissez la catégorie **Intégration**.
5. Cliquez sur le bouton **Télécharger** (Download) qui vient d'apparaître.
6. **Redémarrez Home Assistant**.

---

## ⚙️ Configuration

L'intégration se configure entièrement depuis l'interface utilisateur, aucun YAML n'est requis !

1. Allez dans **Paramètres** > **Appareils et services**.
2. Cliquez sur **+ Ajouter une intégration** (en bas à droite).
3. Cherchez **My Secret Garden**.
4. Saisissez l'URL de votre backend API (n'oubliez pas le `http://` et le port).
5. Validez. Vos bacs et pots apparaissent instantanément dans vos appareils !

---

## 🤖 Exemple d'automatisation

Voici comment utiliser l'intelligence de My Secret Garden pour piloter une électrovanne connectée dans Home Assistant :

```yaml
alias: "🌱 Arrosage Auto : Bac des Aromates"
description: "Arrose le bac si My Secret Garden détecte un besoin en eau"
trigger:
  - platform: time
    at: "21:00:00"
condition:
  - condition: state
    entity_id: binary_sensor.bac_des_aromates_besoin_eau
    state: "on"
action:
  # 1. On allume l'électrovanne Zigbee/Wi-Fi
  - service: switch.turn_on
    target:
      entity_id: switch.electrovanne_aromates
  
  # 2. On arrose pendant 10 minutes
  - delay: "00:10:00"
  
  # 3. On coupe l'eau
  - service: switch.turn_off
    target:
      entity_id: switch.electrovanne_aromates
  
  # 4. On prévient l'API que c'est fait (efface l'alerte sur le téléphone !)
  - service: button.press
    target:
      entity_id: button.valider_arrosage_bac_des_aromates