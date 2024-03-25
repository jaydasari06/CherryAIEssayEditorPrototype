import google.generativeai as genai

from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 0.5,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001", generation_config=generation_config, safety_settings=safety_settings)

@app.route('/genai', methods=['GET'])
def genai():
  essay = """Shadows flickered on the walls as heavy footsteps echoed up the stairs, sending shivers down my spine. My parents had left for a movie, so the logical conclusion for my nine-year-old mind was to assume there was an intruder. Gripping my trusty Thomas the Train chair (the weapon of choice for any child in distress), I whispered urgent instructions to my little brother, Tanish: “Hide in the bathroom. There’s someone downstairs.”

  I crouched behind a wall at the top of the staircase, paranoid. The thief made no effort to conceal his movements; fortunately, he was unaware of my presence. As I leaped out, chair raised high, ready to confront the mysterious burglar on the stairs, I saw a familiar face. My dad had returned for his wallet, and in the process, unknowingly turned our evening into a scene straight out of Home Alone, with me as the brave Kevin McAllister. 

  Looking back, it's amusing that I believed I could defeat a burglar with a foam-padded kiddie chair. That belief wasn’t just adrenaline or childhood naivety; it was my desire to be the superhero older brother. I felt responsible for Tanish, and I genuinely wanted to be his role model. His unwavering faith in me pushed me to excel, creating an image in my mind – and perhaps in his – of a perfect, invincible protector. This illusion of perfection, though comforting, soon became a burden on my maturing mind.

  During my freshman year, caught between the self-induced pressure to be flawless and the reality of my shortcomings, I reluctantly hid a precalculus translations quiz from my parents. When my brother, who idolized me, discovered the crumpled piece of paper, he laughed. "Why'd you hide this? An 85 on three questions isn't even bad." 

  His offhand remark made me confront a difficult truth: I was concealing myself, even from the very person I aimed to inspire. Upholding the facade became increasingly difficult, exhausting my morals and consuming my thoughts. Rather than embodying the brave brother, I was letting my insecurities control me.

  As high school progressed, I was determined to change this, and I forced myself to reveal my flaws to my family, constantly remembering the moment with Tanish. One evening, palms sweating and heart pounding, I found myself telling my dad that with my rigorous schedule and daily tennis commitments, a 10 PM bedtime would be impossible. Getting through these vulnerable conversations taught me to build up my courage with the strength to face my flaws. 

  In my sophomore year, I transformed, embracing my flaws as growth opportunities. No longer burdened by the paralyzing fear of imperfection, I became a confident individual, curious about the challenges around me and eager to address them head-on. One issue was the clunky 1990s website (apparently, the Y2K bug never hit Leander ISD) where students selected a class for a 40-minute flex-time period. As a 17-year-old, the thought of addressing this with administration and district professionals was intimidating. Yet, instead of shrinking back with my old fear of imperfection, I channeled my newfound courage; I took a deep breath and reached out to the CTO of Leander ISD, describing my vision to modernize the interface and centralize student resources within an app. What started as an enthusiastic email evolved into innovative pitches to the tech department, something I wouldn’t have attempted in previous years. This experience culminated in a rewarding summer internship where I developed an app for over 20,000 student users.

  Becoming less perfect made me who I am today. My courage doesn’t come from perfection, but instead, it comes from the resilience to accept and overcome my flaws. Today, I am a fearless leader, an actionable innovator, and an authentic and compassionate role model for my brother. As I prepare for my next endeavor, I will lean into my flaws for bravery, turning every challenge into an opportunity for growth. 

  """

  response = model.generate_content("""This is the essay content provided by the student. It will be a longer piece of text, with various sections that need feedback.

  Feedback Categories: 
  Elaborate: Identify sections where additional detail or examples are needed to strengthen the argument or narrative.
  Reduce: Point out areas where the text is overly verbose or repetitive and can be made more concise.
  Grammar: Highlight grammatical errors, including issues with tense, punctuation, and sentence structure.
  Coherence: Assess the logical flow of ideas and suggest improvements for better cohesion and clarity.

  Example of System Output in JSON
  json{
    "feedback": [
      {
        "category": "Elaborate",
        "text": "This is the essay content",
        "suggestion": "Consider providing more specific examples to support your argument here."
      },
      {
        "category": "Reduce",
        "text": "It will be a longer piece of text",
        "suggestion": "This section is repetitive and can be condensed for clarity."
      },
      {
        "category": "Grammar",
        "text": "This is the essay content provided by the student",
        "suggestion": "Check the verb tense consistency in this sentence."
      },
      {
        "category": "Coherence",
        "text": "It will be a longer piece of text, with various sections that need feedback",
        "suggestion": "Ensure the transition between sections is smooth and logical."
      }
      **KEEP GOING IF YOU HAVE MORE FEEDBACK WITH REPEATS***
    ]
  }
  *** Give 1 feedback per 70 words**

  Here is the essay: 

  """ + essay)

  return response.text

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8082)


# Keep these commands in mind (be in server directory):
# gcloud builds submit --tag gcr.io/<Server-ID>/<Service-Name>
# gcloud run deploy --image gcr.io/<Server-ID>/<Service-Name>