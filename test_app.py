import json

from pokemon_service import PokemonService
from pokemon_name_translator import PokemonNameTranslator
from pokemon_report import PokemonReport

import unittest
from unittest.mock import MagicMock, patch
'''
1. class PokemonService:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon"
    
2. from google.cloud import translate

class PokemonNameTranslator:
    def __init__(self):
        self.client = translate.TranslationServiceClient()

3. pdfkit, не конвертити html
'''

sample_pokemon_data = json.loads(open("sample_pokemon_bulbasaur.json").read())

class TestPokemonService(unittest.TestCase):
    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_pokemon_data
        mock_get.return_value = mock_response

        service = PokemonService()
        data = service.get_pokemon_info("bulbasaur")

        self.assertEqual(data, sample_pokemon_data)

class TestPokemonNameTranslator(unittest.TestCase):
    @patch("pokemon_name_translator.translate.TranslationServiceClient")
    def test_translate(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_response = MagicMock()
        fake_translation = MagicMock()
        fake_translation.translated_text = "Bulbasaur"
        mock_response.translations = [fake_translation]
        mock_client.translate_text.return_value = mock_response
        translator = PokemonNameTranslator()
        result =  translator.translate("Sad Lukashenko")
        self.assertEqual(result, "Bulbasaur")

class TestPokemonReport(unittest.TestCase):
    @patch("pokemon_report.pdfkit.from_file")
    def test_generate_report_pdf(self, mock_pdf):
        report = PokemonReport()
        report.generate_report(pokemon_info=sample_pokemon_data, translated_name="Bulbasaur", output_pdf="pokemon_report.pdf")
        mock_pdf.assert_called_once()

    def test_create_html_report(self):
        report = PokemonReport()
        html_file = report.create_html_report(pokemon_info=sample_pokemon_data, translated_name="Bulbasaur")

        self.assertEqual(html_file, "report_template.html")

        content = open("report_template.html", encoding="utf-8").read()

        self.assertIn("Bulbasaur", content)
        self.assertIn(str(sample_pokemon_data["height"]), content)
        self.assertIn(str(sample_pokemon_data["weight"]), content)
        self.assertIn("overgrow", content)
        self.assertIn("chlorophyll", content)

if __name__ == "__main__":
    unittest.main()