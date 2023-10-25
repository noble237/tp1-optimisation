import unittest
import os
import sqlite3 as sql

from monsieur_tartempion_correction import *

class TestChargerSon(unittest.TestCase):
    
    def test_charger_son_existant(self):
        """Teste le chargement d'un fichier audio existant."""

        nom_son_existant = "522243__dzedenz__result-10.wav"

        son = charger_son(nom_son_existant)        
        self.assertIsNotNone(son)
    
    def test_charger_son_inexistant(self):
        """Teste le chargement d'un fichier audio inexistant."""
        
        nom_son_inexistant = "erreur.wav"
        
        with self.assertRaises(FileNotFoundError):
            charger_son(nom_son_inexistant)



    def test_splash_titre(self):
        """
        Teste le comportement de combiner_splasher avec le type_splash titre_base64.
        """
        self.assertIsNone(combiner_splasher('titre_base64', False))

    def test_splash_equipe(self):
        """
        Teste le comportement de combiner_splasher avec le type_splash equipe_base64.
        """
        self.assertIsNone(combiner_splasher('equipe_base64', False))

    def test_splash_echec(self):
        """
        Teste le comportement de combiner_splasher avec le type_splash echec_base64.
        """
        self.assertIsNone(combiner_splasher('echec_base64', False))

    def test_splash_succes(self):
        """
        Teste le comportement de combiner_splasher avec le type_splash succes_base64.
        """
        self.assertIsNone(combiner_splasher('succes_base64', False))

    def test_splash_inconnu(self):
        """
        Teste le comportement de combiner_splasher avec un type_splash inconnu.
        """
        with self.assertRaises(SystemExit) as cm:
            combiner_splasher('type_splash_inconnu', False)

        self.assertEqual(cm.exception.code, 1)

    def test_charger_questions_valide(self):
        """Teste le chargement des questions depuis une base de données valide."""

        nom_bd = "questions.bd"
        questions = charger_questions(nom_bd)

        self.assertNotEqual(questions, [])
    
    def test_charger_questions_invalide(self):
        """Teste le chargement des questions depuis une base de données invalide (inexistante)."""

        nom_bd = "bd_invalide.bd"

        with self.assertRaises(FileNotFoundError):
            charger_questions(nom_bd)





if __name__ == '__main__':
    unittest.main()



