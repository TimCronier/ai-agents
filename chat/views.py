import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from .agents import get_shared_group_chat, CycleTermination

@csrf_exempt                  # simplifie le POC
async def chat_api(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide"}, status=400)

    question = (payload.get("message") or "").strip()
    if not question:
        return JsonResponse({"error": "Message vide"}, status=400)

    chat = await get_shared_group_chat()
    await chat.add_chat_message(ChatMessageContent(
        role=AuthorRole.USER,
        content=question,
    ))

    # Concatène tous les morceaux retournés
    parts = []
    async for chunk in chat.invoke():
        if chunk and chunk.name:
            parts.append(chunk.content)
    answer = "\n".join(parts)

    return JsonResponse({"answer": answer})
