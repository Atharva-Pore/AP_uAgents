from uagents import Agent, Context, Model
from googletrans import Translator

CLIENT_AGENT_ADDRESS = "agent1qvyshv0spghjerel0svhfm3w0kpckhg3l35f6gu00lvtyrzrjeudv36k434"

class LanguageTranslatorRequest(Model):
    text: str
    target_language: str

class LanguageTranslatorResponse(Model):
    translated_text: str

LanguageTranslatorAgent = Agent(
    name="LanguageTranslatorServerAgent",
    port=5002,
    endpoint="http://localhost:5002/submit",
    seed="LanguageTranslatorAgentSeed"
)

async def translate_text(text, target_language):
    # Create a Translator object
    translator = Translator()
    
    # Translate the text
    translation = translator.translate(text, dest=target_language)
    
    # Return the translated text
    return translation.text

@LanguageTranslatorAgent.on_message(model=LanguageTranslatorRequest)
async def handle_embedding(ctx: Context, sender: str, request: LanguageTranslatorRequest):

    translated_text = await translate_text(request.text, request.target_language)
    await ctx.send(CLIENT_AGENT_ADDRESS, LanguageTranslatorResponse(translated_text=translated_text))

if __name__ == "__main__":
    LanguageTranslatorAgent.run()
