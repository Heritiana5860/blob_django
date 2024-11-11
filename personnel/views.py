from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from requests import delete

from personnel.models import Message

# Create your views here.
def index(request):
    if request.method == 'POST':

        # Si le bouton de suppression est cliqué
        if 'delete' in request.POST:
            message_id = request.POST.get('message_id')

            try:
                message = Message.objects.get(id=message_id)

                # Vérifier que l'utilisateur est le propriétaire du message
                if message.user == request.user:
                    message.delete()

            except Message.DoesNotExist:
                pass
            return redirect('index')

        content = request.POST.get('content')
        user = request.user

        if content:
            Message.objects.create(content=content, user=user)
        return redirect('index')

    context= {'messages': Message.objects.order_by('-created_at')}
    return render(request, 'index.html', context=context)