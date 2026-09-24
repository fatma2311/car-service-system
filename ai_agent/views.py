import json
from decouple import config
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
from .tools import get_maintenance_history, get_available_technicians, make_book_appointment_tool, make_cancel_appointment_tool

client = genai.Client(api_key=config('GEMINI_API_KEY'))

system_instruction = (
    "You are a helpful assistant for a car service center. "
    "Always reply in plain text only, no markdown, no asterisks, no bullet points with *. "
    "Use simple line breaks and dashes (-) if you need a list. "
    "Reply in the same language the user used. "
    "When mentioning a maintenance record's status (OPEN, IN_PROGRESS, COMPLETED), "
    "keep it exactly as-is in English, do not translate it."
)


@login_required
def chat_page(request):
    return render(request, 'ai_agent/chat.html')


@login_required
@csrf_exempt
def chat_message(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data = json.loads(request.body)
    user_message = data.get('message', '')

    history = request.session.get('chat_history', [])
    history.append({'role': 'user', 'parts': [{'text': user_message}]})

    book_appointment = make_book_appointment_tool(request.user)
    cancel_appointment = make_cancel_appointment_tool(request.user)
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=history,
        config=types.GenerateContentConfig(
            tools=[get_maintenance_history, get_available_technicians, book_appointment, cancel_appointment],
            system_instruction=system_instruction,
        ),
    )

    history.append({'role': 'model', 'parts': [{'text': response.text}]})
    request.session['chat_history'] = history

    return JsonResponse({'reply': response.text})