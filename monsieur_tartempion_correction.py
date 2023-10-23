"""
Monsieur Tartempion - Édition horrifique
420-5GP-BB, automne 2023, Collège Bois-de-Boulogne
Travail pratique 1
A
Ressources sous licences:
  522243__dzedenz__result-10.wav
  par DZeDeNZ, 2020-07-15
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  409282__wertstahl__syserr1v1-in_thy_face_short.wav
  par wertstahl, 2017-11-06
  Licence: https://creativecommons.org/licenses/by-nc/4.0/

  173859__jivatma07__j1game_over_mono.wav
  par jivatma07, 2013-01-11
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav
  par Erokia, 2020-12-26
  Licence: https://creativecommons.org/licenses/by-nc/4.0/
"""





import os
import random
import simpleaudio as audio
import time
import sqlite3 as sql
import PySimpleGUI as SimpleGui

from images import *
from indicateurs import Indicateur


NB_QUESTIONS = 5
TEMPS_TOTAL = NB_QUESTIONS * 2

# Cyrille
DEFAULT_FONT = SimpleGui.DEFAULT_FONT

# Cyrille
FONT_STYLES = {
    'etiquettes': (DEFAULT_FONT, 20, 'normal'),
    'temps': (DEFAULT_FONT, 50, 'normal'),
    'question': (DEFAULT_FONT, 30, 'normal'),
    'reponses': (DEFAULT_FONT, 20, 'normal'),
    'ou': (DEFAULT_FONT, 20, 'italic')
}

# Cryille
def charger_son(nom_son):
    # Vérifier si le fichier audio existe
    if os.path.isfile(nom_son):
        try:
            son = audio.WaveObject.from_wave_file(nom_son)
            return son
        except Exception as e:
            raise Exception(f"Erreur lors du chargement du son {nom_son}: {e}")
    else:
        raise FileNotFoundError(f"Le fichier audio {nom_son} n'existe pas.")
    

# Cyrille
SONS = {
    'VICTOIRE': charger_son('522243__dzedenz__result-10.wav'),
    'ERREUR': charger_son('409282__wertstahl__syserr1v1-in_thy_face_short.wav'),
    'FIN_PARTIE': charger_son('173859__jivatma07__j1game_over_mono.wav'),
    'MUSIQUE_QUESTIONS': charger_son('550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav')
}






####################################################
# Splasher
####################################################
#Affiche l'image en parametre
def splasher(image_data, par_dessus : bool, delais_ms : int, couleur_transparente=None) -> None:
    SimpleGui.Window('Monsieur Tartempion', image_data, transparent_color=couleur_transparente, no_titlebar=True, keep_on_top=par_dessus).read(timeout=delais_ms, close=True)
    
# Cyrille
def combiner_splasher(type_splash):
    image_data = [[SimpleGui.Image(data=type_splash())]]
    par_dessus = True
    delai_ms = 0
    couleur_type = None

    try:
        if type_splash == titre_base64:
            delai_ms = 2000
        elif type_splash == equipe_base64:
            couleur_type = SimpleGui.theme_background_color()
            delai_ms = 1500
        elif type_splash == echec_base64:
            couleur_type = SimpleGui.theme_background_color()
            delai_ms = 3000
        elif type_splash == succes_base64:
            couleur_type = "maroon2"
            delai_ms = 3000
        else:
            raise ValueError("Type de splash non reconnu") 

        splasher(image_data, par_dessus, delai_ms, couleur_type)
    except TypeError as te:
        print(f"Erreur de type : {te}")  # Erreur de type, par exemple, si type_splash est un str ou int
    except ValueError as ve:
        print(f"Une erreur s'est produite : {ve}")  # Erreur de valeur, par exemple, si type_splash n'est pas reconnu
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")  # Autres

    

####################################################
# Modifier l'interface
####################################################

# Cyrille
def gerer_question(fenetre: SimpleGui.Window, question: tuple) -> None:
    if question is None:
        question_text, reponse1, reponse2 = '', '', ''
        is_question = False
    else:
        question_text, reponse1, reponse2 = question
        is_question = True

    fenetre['QUESTION'].update(question_text)

    if is_question:
        reponses_melanges = melanger_reponses((reponse1, reponse2))
        reponse_melange1, reponse_melange2 = reponses_melanges
    else:
        reponse_melange1, reponse_melange2 = '', ''

    fenetre['BOUTON-GAUCHE'].update(reponse_melange1, disabled=not is_question, visible=True)
    fenetre['OU'].update(text_color='white' if is_question else SimpleGui.theme_background_color())
    fenetre['BOUTON-DROIT'].update(reponse_melange2, disabled=not is_question, visible=True)




    
    
    
    
    
    
####################################################
# Manipulation des questions
####################################################

# Cyrille
def charger_questions(fichier_db: str) -> list:
    try:
        connexion = sql.connect(fichier_db)
        with connexion:
            resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')
        return [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in resultat_requete]
    except sql.Error as e:
        print(f"Une erreur s'est produite lors de la récupération des questions depuis la base de données : {e}")
        return []

# Cyrille
def choisir_questions(banque: list, nombre: int) -> list:
    if not banque:
        raise ValueError("La banque de questions est vide.")

    # Cyrille
    # Filtre pour ne pas avoir la mauvaise question
    questions_filtrees = [question for question in banque if (question[0] != "*" and question[1] != "Mauvaise" and question[2] != "Question")]

    # Vérification que nous avons assez de question dans la bd pour les questions demandées
    if len(questions_filtrees) < nombre:
        raise ValueError("Pas assez de questions valides pour répondre à la demande.")

    questions_uniques = random.sample(questions_filtrees, nombre)
    return [[question, Indicateur.VIDE] for question in questions_uniques]


def melanger_reponses(reponses: tuple) -> tuple:
    return (reponses[0], reponses[1]) if bool(random.getrandbits(1)) else (reponses[1], reponses[0])




###################################################
# Modification et affichage de l'interface
###################################################    
    
def afficher_jeu() -> SimpleGui.Window:

    titre_jeu = 'Monsieur Tartempion'

    temps = [[SimpleGui.Text('Temps restant', font=FONT_STYLES['etiquettes'], size=70, justification='center')], [SimpleGui.Text(str(TEMPS_TOTAL), key='TEMPS', font=FONT_STYLES['temps'])]]

    boutons_reponse = [SimpleGui.Column([[SimpleGui.Button(key='BOUTON-GAUCHE', font=FONT_STYLES['reponses'], button_color=('white', SimpleGui.theme_background_color()),
                   border_width=0, disabled=True, visible=True),
        SimpleGui.Text(' ou ', key='OU', font=FONT_STYLES['ou'], text_color=SimpleGui.theme_background_color()),
        SimpleGui.Button(key='BOUTON-DROIT', font=FONT_STYLES['reponses'], button_color=('white', SimpleGui.theme_background_color()),
                   border_width=0, disabled=True, visible=True)]], element_justification='center')]

    question = [SimpleGui.Text(' ', key='QUESTION', font=FONT_STYLES['question'])]

    action = [SimpleGui.Button(image_data=bouton_jouer_base64(), key='BOUTON-ACTION', border_width=0, button_color=(SimpleGui.theme_background_color(), SimpleGui.theme_background_color()), pad=(0, 10)),
              SimpleGui.Image(data=bouton_inactif_base64(), key='IMAGE-BOUTON-INACTIF', visible=False, pad=(0, 10))]

    indicateurs = [*[SimpleGui.Image(data=indicateur_vide_base64(), key=f'INDICATEUR-{i}', pad=(4, 10)) for i in range(NB_QUESTIONS)]]

   
    fenetre = SimpleGui.Window(titre_jeu, [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True, element_padding=(0, 0),
                    element_justification='center', resizable=False, finalize=True)

    return fenetre






###################################################
# Programme primcipal
###################################################

def programme_principal() -> None:
    """Despote suprême de toutes les fonctions."""

    SimpleGui.theme('Black')

    # Cyrille
    combiner_splasher(equipe_base64)
    combiner_splasher(titre_base64)


    toutes_les_questions = charger_questions("questions.bd")
    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)

    fenetre = afficher_jeu()
    temps_restant = TEMPS_TOTAL
    prochaine_question = 0
    decompte_actif = False

    quitter = False
    while not quitter:
        event, valeurs = fenetre.read(timeout=10)
        if decompte_actif:
            dernier_temps = temps_actuel
            temps_actuel = round(time.time())
            if dernier_temps != temps_actuel:
                temps_restant -= 1
                fenetre['TEMPS'].update(str(temps_restant))
                if temps_restant == 0:
                    decompte_actif = False
                    fenetre.hide()
                    gerer_question(fenetre, None)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                    SONS['FIN_PARTIE'].play()
                    musique_questions_controles.stop()

                    # Cyrille
                    combiner_splasher(echec_base64)

                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    temps_restant = TEMPS_TOTAL
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0
                    continue

        if event == 'BOUTON-ACTION':
            fenetre['BOUTON-ACTION'].update(disabled=True, visible=False)
            fenetre['IMAGE-BOUTON-INACTIF'].update(visible=True)
            temps_actuel = round(time.time())
            decompte_actif = True
            gerer_question(fenetre, questions[prochaine_question][0])
            musique_questions_controles = SONS['MUSIQUE_QUESTIONS'].play()
        elif event == 'BOUTON-GAUCHE' or event == 'BOUTON-DROIT':
            if (event == 'BOUTON-GAUCHE' and fenetre['BOUTON-GAUCHE'].get_text() != questions[prochaine_question][0][1]) or \
               (event == 'BOUTON-DROIT' and fenetre['BOUTON-DROIT'].get_text() != questions[prochaine_question][0][1]):
                # le joueur a choisi la mauvaise réponse
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_vert_base64())
                questions[prochaine_question][1] = Indicateur.VERT
                prochaine_question += 1
                if prochaine_question < NB_QUESTIONS:
                    gerer_question(fenetre, questions[prochaine_question][0])
                elif NB_QUESTIONS <= prochaine_question:
                    decompte_actif = False
                    fenetre.hide()
                    gerer_question(fenetre, None)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                        questions[i][1] = Indicateur.VIDE
                    musique_questions_controles.stop()
                    SONS['VICTOIRE'].play()

                    # Cyrille
                    combiner_splasher(succes_base64)

                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    temps_restant = TEMPS_TOTAL
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0
                    continue
            else:
                # le joueur a choisi la bonne réponse
                decompte_actif = False
                gerer_question(fenetre, None)
                for i in range(prochaine_question):
                    fenetre[f'INDICATEUR-{i}'].update(data=indicateur_jaune_base64())
                    questions[i][1] = Indicateur.JAUNE
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_rouge_base64())
                questions[prochaine_question][1] = Indicateur.ROUGE
                prochaine_question = 0
                fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                SONS['ERREUR'].play()
                musique_questions_controles.stop()
        elif event == SimpleGui.WIN_CLOSED:
            decompte_actif = False
            quitter = True

    fenetre.close()
    del fenetre



if __name__ == "__main__":
	programme_principal()
