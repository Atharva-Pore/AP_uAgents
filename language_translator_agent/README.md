![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:research](https://img.shields.io/badge/research-3D8BD3)
![domain:natural-language-processing](https://img.shields.io/badge/natural--language--processing-3D8BD3)
![domain:machine-learning](https://img.shields.io/badge/machine--learning-3D8BD3)
![domain:artificial-intelligence](https://img.shields.io/badge/artificial--intelligence-3D8BD3)
![domain:language-translation](https://img.shields.io/badge/language--translation-3D8BD3)
![domain:google-translate](https://img.shields.io/badge/google--translate-3D8BD3)
![domain:text-analysis](https://img.shields.io/badge/text--analysis-3D8BD3)

# Language Translator Agent

**Description**: This Language Translator Agent allows users to send text to be translated into a target language. The server utilizes the Google Translate API to perform the translation, and the client sends the text and target language to the server, receiving the translated text in response.

---

## Input Data Model

```python
class LanguageTranslatorRequest(Model):
    text: str
    target_language: str
```

## Output Data Model

```python
class LanguageTranslatorResponse(Model):
    translated_text: str
```

## Functionality:
- The client sends a request with the text to be translated and the target language to the server.
- The server uses the Google Translate API to perform the translation.
- The translated text is returned to the client for display.

---

## How to Use

### 1. Install Required Packages

Before running the agent, ensure you have the necessary Python packages installed:

```sh
pip install googletrans==4.0.0-rc1
pip install uagents
```

### 2. Client Code

Run the following client code. The client will prompt you for the text you want to translate and the target language.

```python
from uagents import Agent, Context, Model
from difflib import get_close_matches

text = ''
targetLanguage = ''

LANGUAGE_TRANSLATOR_AGENT = 'agent1qvjxyhqfu4r5u89jccqzd9f9wy3t8uhqlt30euczjf4dyqgh6ftegwypmsl'

LANGUAGE_CODES = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
    "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs",
    "Bulgarian": "bg", "Catalan": "ca", "Cebuano": "ceb", "Chichewa": "ny", "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw", "Corsican": "co", "Croatian": "hr", "Czech": "cs", "Danish": "da",
    "Dutch": "nl", "English": "en", "Esperanto": "eo", "Estonian": "et", "Filipino": "tl", "Finnish": "fi",
    "French": "fr", "Frisian": "fy", "Galician": "gl", "Georgian": "ka", "German": "de", "Greek": "el",
    "Gujarati": "gu", "Haitian Creole": "ht", "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "iw", "Hindi": "hi",
    "Hmong": "hmn", "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga",
    "Italian": "it", "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km",
    "Korean": "ko", "Kurdish (Kurmanji)": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la", "Latvian": "lv",
    "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms", "Malayalam": "ml",
    "Maltese": "mt", "Maori": "mi", "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my", "Nepali": "ne",
    "Norwegian": "no", "Pashto": "ps", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
    "Romanian": "ro", "Russian": "ru", "Samoan": "sm", "Scots Gaelic": "gd", "Serbian": "sr", "Sesotho": "st",
    "Shona": "sn", "Sindhi": "sd", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so", "Spanish": "es",
    "Sundanese": "su", "Swahili": "sw", "Swedish": "sv", "Tajik": "tg", "Tamil": "ta", "Telugu": "te", "Thai": "th",
    "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh",
    "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
}

class LanguageTranslatorRequest(Model):
    text: str
    target_language: str

class LanguageTranslatorResponse(Model):
    translated_text: str

client_agent = Agent(
    name="LanguageTranslatorClientAgent",
    port=5060,
    seed="LanguageTranslatorClientAgentSeed",
    endpoint="http://localhost:5060/submit"
)

def get_language_code(language_name: str) -> str:
    """
    Finds the closest matching language name and returns the corresponding language code.
    """
    language_name = language_name.title().strip()
    if language_name in LANGUAGE_CODES:
        return LANGUAGE_CODES[language_name]
    closest_match = get_close_matches(language_name, LANGUAGE_CODES.keys(), n=1, cutoff=0.6)
    return LANGUAGE_CODES[closest_match[0]] if closest_match else "en"  # Default to English if no match found

def prepare_query(usr_query: str, target_language: str) -> None:
    """
    Sets the global text and targetLanguage variables after converting the target language to its code.
    """
    global text, targetLanguage
    text = usr_query
    targetLanguage = get_language_code(target_language)

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending request to translate text: {text[:50]}...")
    request = LanguageTranslatorRequest(text=text, target_language=targetLanguage)
    await ctx.send(LANGUAGE_TRANSLATOR_AGENT, request)

@client_agent.on_message(model=LanguageTranslatorResponse)
async def handle_response(ctx: Context, sender: str, msg: LanguageTranslatorResponse):
    print(f'{"=" * 20}:Translation:{"=" * 20}')
    print(f"Original Text: {text}")
    print(f"Translated Text: {msg.translated_text}")
    print(f'{"=" * 20}============={"=" * 20}')

if __name__ == "__main__":
    query = input('Enter your text to be translated: ')
    language = input('Enter your target Language: ')
    prepare_query(query, language)
    client_agent.run()
```

### 3. Running the Client

1. Ensure the server is running first, as the client will connect to it.
2. Run the client code.
3. Enter the text and the target language when prompted.
4. The translated text will be displayed in the console.

---

## Deployment Instructions:
- Run the client code after ensuring that all required packages are installed.
- The client will send a translation request to the server, and the server will return the translated text.
