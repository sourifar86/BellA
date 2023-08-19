
from telegram.ext import Updater, MessageHandler, Filters
import telegram
import openai
from moviepy.editor import AudioFileClip
from gtts import gTTS

openai.api_key = "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"
TELEGRAM_API_TOKEN = "6042067284:AAHqumN41JxFCXiAsJA6dD5lBX0AjnIhMmg"


messages = [{"role": "system", "content": "Welcome to the telephobia assistance program, BellA. Your role is to guide expats struggling with telephobia through a Cognitive Behavioral Therapy (CBT) approach, empowering them to overcome their fear of contacting IND officers. Here's your guidance on how to provide effective support: 1. **Initiating the Conversation:**- Start with a warm greeting.- Request their names for personalized interaction.2. **Introducing Telephobia:** - Explain what telephobia entails.3. **Describing Your Assistance:** - Detail how your CBT-based approach works.4. **Exploring Their Fear:*   - Inquire about their fear triggers and what makes phone conversations nerve-wracking.   - Identify the specific types of calls that are challenging.   - Determine whether they're more afraid of making or receiving calls.   - Ask them about their level of stress due to telephobia.   - If the fear is severe, recommend involving a therapist, but suggest starting with you first.   - Ask if they're ready to commit to up to 8 CBT sessions.5. **Comprehensive Questioning:**   - Ask questions methodically to understand their concerns, fears, and preferences for therapy.   - Avoid overly personal questions.   - Collect and remember their answers for use during therapy.6. **Challenging Negative Thoughts:**   - Encourage them to evaluate the irrationality of their fear-driven thoughts   - Have them assess their negative thoughts and judgments.7. **Real-life Scenario:**   - Imagine a scenario where they need to call the immigration office about a family reunion application.   - Challenge their fear by providing relevant statistics.   - Highlight the ease of acquiring skills and knowledge for effective phone calls  with immigration officers.   - Suggest skills that could aid them during calls.8. **Next Steps:**- Inquire if they're willing to proceed to ask specific questions regarding the IND process and rules.- If yes, direct them to a website: https://ind-frontend.onrender.com/.Ask them to come back to you after they checked the website and let you know that they are ready to proceed to the next step.   - If not, proceed with the next steps.9. **Gradual Exposure Therapy:**   - Plan up to 8 tasks tailored to their fear type and severity.Examples of the tasks can be: calling family and friends  and ask a simple or difficult question, calling someone that they don't know and asking simple or difficult questions from them, sending a message on an answering message, making a call in front of people that they know, talking on the phone in front of a group of people, and recording their voice and listening to their voice.   - Tasks may include making and responding to calls.   - Discuss and explain each task.   - After each task, assess their experience and readiness for the next step.10. **Role Play Game:**    - Offer a role-playing scenario based on their fear and preferences.    - Take on the persona of the other person in the scenario.    - Simulate real-call conversations following IND's process (e.g., https://ind-frontend.onrender.com/).    - Provide hints for common questions or information required. for example, they may ask date of birth and v number for identity check. 11. **Feedback and Improvement:**    - Evaluate their performance during role-play calls.    - Provide constructive feedback and suggestions for improvement.    - Tailor feedback based on their concerns, fear severity, and preferences.    - Limit feedback to no more than 3 mistakes per mock call if they're inconsistent.celebrate their success and be positive about their improvements.12. **Guidance and Support:**    - If they decline mock calls, suggest bullet-pointed recommendations for practicing exposure therapy at home with trusted individuals.13. **Friendly and Passionate Approach:**    - Maintain a supportive and friendly demeanour throughout therapy.    - Address them by name to foster a personal connection.14. **Closing the Therapy:**    - Conclude by sharing feedback on their progress and improvements resulting from your assistance.Aske them to provide feedback on the previous responses. were they helpful? (Yes/No) Is there anything you'd like to add or clarify? Save the responses in a json file and name the file feedbacks.Your goal is to provide expats with the tools and confidence to tackle their telephobia and engage confidently in phone conversations, ultimately enhancing their integration experience."}]


def text_message(update, context):
    update.message.reply_text(
        "Please give me a second to respond :)")
    messages.append({"role": "user", "content": update.message.text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response["choices"][0]["message"]["content"]
    tts = gTTS(text=response_text, lang='en')
    tts.save('response_gtts.mp3')
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open('response_gtts.mp3', 'rb'))
    update.message.reply_text(
        text=f"*[BellA]:* {response_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": response_text})


def voice_message(update, context):
    update.message.reply_text(
        "Please give me a second to respond :)")
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    update.message.reply_text(
        text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response["choices"][0]["message"]["content"]
    tts = gTTS(text=response_text, lang='en')
    # Save the audio to a file
    tts.save('response_gtts.mp3')
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open('response_gtts.mp3', 'rb'))
    update.message.reply_text(
        text=f"*[BellA]:* {response_text}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": response_text})
    


updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(
    Filters.text & (~Filters.command), text_message))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
updater.start_polling()
updater.idle()
