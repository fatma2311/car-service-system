
import json

from google.genai import errors
from decouple import config
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types

from .tools import (
    make_get_my_vehicles_tool,
    make_get_maintenance_history_tool,
    get_available_technicians,
    make_book_appointment_tool,
    make_cancel_appointment_tool,
    get_available_service_slots,
    make_get_due_services_tool,
)




client = genai.Client(
    api_key=config('GEMINI_API_KEY')
)


system_instruction = (
    "You are a helpful assistant for a car service center. "
    "Always reply in plain text only, no markdown, no asterisks, "
    "no bullet points with *. "
    "Use simple line breaks and dashes (-) if you need a list. "
    "Reply in the same language the user used. "
    "When the user asks about their own car or vehicle, "
    "or uses phrases such as 'my car' or 'my vehicle', "
    "use the get_my_vehicles tool to retrieve the vehicles "
    "belonging to the currently logged-in user. "
    "Do not ask the user for a license plate if you can determine "
    "the vehicle from their available vehicles. "
    "When mentioning a maintenance record's status "
    "(OPEN, IN_PROGRESS, COMPLETED), "
    "keep it exactly as-is in English and do not translate it."
)


@login_required
def chat_page(request):
    return render(request, 'ai_agent/chat.html')


@login_required
@csrf_exempt
def chat_message(request):

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'POST only'},
            status=405
        )

    data = json.loads(request.body)

    user_message = data.get('message', '').strip()

    if not user_message:
        return JsonResponse(
            {'error': 'Message is required'},
            status=400
        )

    my_vehicles = make_get_my_vehicles_tool(request.user)

    maintenance_history = make_get_maintenance_history_tool(
        request.user
    )

    book_appointment = make_book_appointment_tool(
        request.user
    )

    cancel_appointment = make_cancel_appointment_tool(
        request.user
    )


    due_services = make_get_due_services_tool(
    request.user
    )



    try:

        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(

            tools=[
    my_vehicles,
    maintenance_history,
    get_available_technicians,
    get_available_service_slots,
    due_services,
    book_appointment,
    cancel_appointment,
],


                system_instruction=system_instruction,
            ),
        )

    except errors.ClientError as e:

        if e.code == 429:
            return JsonResponse({
                'reply': (
                    'The AI Assistant is temporarily unavailable '
                    'because the AI service quota has been reached. '
                    'Please try again later.'
                )
            }, status=200)

        return JsonResponse({
            'reply': (
                'The AI Assistant is temporarily unavailable. '
                'Please try again later.'
            )
        }, status=200)

    except Exception:

        return JsonResponse({
            'reply': (
                'Something went wrong while contacting the AI Assistant. '
                'Please try again later.'
            )
        }, status=200)

    request.session['chat_history'] = request.session.get(
        'chat_history',
        []
    )

    request.session['chat_history'].append({
        'role': 'user',
        'parts': [
            {
                'text': user_message
            }
        ]
    })

    request.session['chat_history'].append({
        'role': 'model',
        'parts': [
            {
                'text': response.text
            }
        ]
    })

    request.session.modified = True

    return JsonResponse({
        'reply': response.text
    })

