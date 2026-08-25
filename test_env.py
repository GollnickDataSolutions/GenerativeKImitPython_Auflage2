
#%% packages
import os
import openai
import unittest

#%% Laden der Umgebungsvariablen
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))


#%% test class
class TestEnvironment(unittest.TestCase):

    skip_env_variable_tests = True
    skip_openai_test = True
    
    def test_env_file_exists(self):
        env_file_exists = True if find_dotenv() > "" else False
        if env_file_exists:
            TestEnvironment.skip_env_variable_tests = False
        self.assertTrue(env_file_exists, ".env file not found.")

    def env_variable_exists(self, variable_name):
        self.assertIsNotNone(
            os.getenv(variable_name),
            f"{variable_name} not found in .env file")

    def test_openai_variable(self):
        if TestEnvironment.skip_env_variable_tests:
            self.skipTest("Skipping OpenAI env variable test")

        self.env_variable_exists('OPENAI_API_KEY')
        TestEnvironment.skip_openai_test = False

    def test_openai_connection(self):
        if TestEnvironment.skip_openai_test:
            self.skipTest("Skipping OpenAI test")

        llm = openai.OpenAI()
        
        try:
            models = llm.models.list()
        except openai.AuthenticationError as e:
            models = None
        self.assertIsNotNone(
            models,
            "OpenAI is not working. Check API_KEY key in .env file.")

    def test_openrouter_variable(self):
        if TestEnvironment.skip_env_variable_tests:
            self.skipTest("Skipping Anthropic env variable test")

        self.env_variable_exists('OPENROUTER_API_KEY')
        TestEnvironment.skip_anthropic_test = False
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEnvironment('test_env_file_exists'))
    suite.addTest(TestEnvironment('test_openai_variable'))
    suite.addTest(TestEnvironment('test_openai_connection'))
    suite.addTest(TestEnvironment('test_openrouter_variable'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    