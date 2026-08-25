#%% packages
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
import re
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
load_dotenv()

# Initialize ChatOpenAI with the desired model
chat_model = ChatOpenRouter(model_name="openai/gpt-5.6-luna")

# %% Pydantic model
class FeedbackResponse(BaseModel):
    rating: str = Field(..., description="Bewertung in Prozent")
    feedback: str = Field(..., description="Ausführliches Feedback")
    revised_output: str = Field(..., description="Eine verbesserte Antwort, die die wichtigsten Elemente des Themas beschreibt")

parser = PydanticOutputParser(pydantic_object=FeedbackResponse)

# %% Self-feedback function
def self_feedback(user_prompt: str, max_iterations: int = 5, target_rating: int = 90):
    content = ""
    feedback = ""
    
    for i in range(max_iterations):
        # Define the prompt based on iteration
        prompt_content = user_prompt if i == 0 else ""
        
        # Create a ChatPromptTemplate for system and user prompts
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """
                Beurteile die Eingabe dahingehend, wie gut sie die ursprüngliche Aufgabe erfüllt, die wichtigsten Elemente und die Bedeutung des Themas zu erklären. Berücksichtige dabei folgende Faktoren: Umfang und Tiefe des bereitgestellten Kontexts; Abdeckung der wichtigsten Elemente; Falls du Lücken oder Bereiche erkennst, die weiter ausgeführt werden sollten: Gib die Antwort als JSON mit folgenden Feldern zurück: 'rating': 'Bewertung in Prozent', 'feedback': 'ausführliches Feedback', 'revised_output': 'gib eine verbesserte Antwort. 
                Halte dich strikt an die Formatinstruktionen {format_instructions} 
           
                """),
            ("user", "<prompt_content>{prompt_content}</prompt_content><revised_output>{revised_output}</revised_output><feedback>{feedback}</feedback>")
        ])
        prompt_template = prompt_template.partial(format_instructions=parser.get_format_instructions())
        
        # Get response from the model
        chain = prompt_template | chat_model | parser
        response = chain.invoke({"prompt_content": prompt_content, "revised_output": content, "feedback": feedback})
        
        
        try:
            
            # Extract rating
            rating_num = int(re.findall(r'\d+', response.rating)[0])

            # Extract feedback and revised output
            feedback = response.feedback
            content = response.revised_output
            
            # Print iteration details
            print(f"i={i}, Prompt Content: {prompt_content}, Rating: {rating_num}, \nFeedback: {feedback}, \nRevised Output: {content}")
            
            # Return if rating meets or exceeds target
            if rating_num >= target_rating:
                return content
        except ValidationError as e:
            print("Validation Error:", e.json())
            return "Invalid response format."
    
    return content

#%% Test
user_prompt = "KI Modelle erstellen ihre Antworten auf Basis von Wahrscheinlichkeiten."
res = self_feedback(user_prompt=user_prompt, max_iterations=3, target_rating=95)
res
# %%
from pyperclip import copy
copy(res)
# %%
