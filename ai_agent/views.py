import json

from google.genai import errors
from decouple import config
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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

    "When the user gives a date without a year, "
    "use the current year, not an older or arbitrary year. "
    "For example, if the current year is 2026 and the user says "
    "'September 25 at 10 AM', interpret it as "
    "'2026-09-25 10:00', not 2023-09-25 or another year. "
    "Never invent an old year when the user did not provide one. "

    "When mentioning a maintenance record's status "
    "(OPEN, IN_PROGRESS, COMPLETED), "
    "keep it exactly as-is in English and do not translate it. "

    "When canceling an appointment, the user must explicitly "
    "confirm the cancellation. "
    "If the cancel_appointment tool asks for confirmation, "
    "do not cancel anything yet. "
    "Only call cancel_appointment with confirm=True after "
    "the user clearly confirms the cancellation."
)


@login_required
def chat_page(request):
    return render(
        request,
        'ai_agent/chat.html'
    )


@login_required
def chat_message(request):

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'POST only'},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )

    user_message = data.get('message', '').strip()

    if not user_message:
        return JsonResponse(
            {'error': 'Message is required'},
            status=400
        )

    # Create tools for the currently logged-in user.

    my_vehicles = make_get_my_vehicles_tool(
        request.user
    )

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

    tools = [
        my_vehicles,
        maintenance_history,
        get_available_technicians,
        get_available_service_slots,
        due_services,
        book_appointment,
        cancel_appointment,
    ]

    # Get previous conversation.

    chat_history = request.session.get(
        'chat_history',
        []
    )

    # Convert old session format to simple text history.

    history = []

    for message in chat_history:

        role = message.get('role')

        if 'text' in message:
            text = message['text']

        elif 'parts' in message:

            parts = message.get(
                'parts',
                []
            )

            text = ''

            if parts and isinstance(parts[0], dict):
                text = parts[0].get(
                    'text',
                    ''
                )

        else:
            text = ''

        if role in ['user', 'model'] and text:

            history.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=text
                        )
                    ]
                )
            )

    try:

        # Create a chat session for this request.

        chat = client.chats.create(
            model='gemini-3.5-flash-lite',
            config=types.GenerateContentConfig(
                tools=tools,
                system_instruction=system_instruction,
            ),
            history=history,
        )

        response = chat.send_message(
            user_message
        )

    except errors.ClientError as e:

    # Gemini quota/rate limit.

        if getattr(e, 'code', None) == 429:

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

    except errors.ServerError as e:

    # Gemini 503 = temporary model/server problem.

        if getattr(e, 'code', None) == 503:

            return JsonResponse({
                'reply': (
                    'The AI Assistant is temporarily unavailable '
                    'because the AI service is currently busy. '
                    'Please try again in a moment.'
                )
            }, status=200)

        return JsonResponse({
            'reply': (
                'The AI service is temporarily unavailable. '
                'Please try again later.'
            )
        }, status=200)

    except Exception as e:

        return JsonResponse({
            'reply': (
                'Something went wrong while contacting '
                'the AI Assistant. Please try again later.'
            )
        }, status=200)

    # Save the conversation.

    chat_history.append({
        'role': 'user',
        'text': user_message
    })

    chat_history.append({
        'role': 'model',
        'text': response.text
    })

    request.session['chat_history'] = chat_history
    request.session.modified = True

    return JsonResponse({
        'reply': response.text
    })