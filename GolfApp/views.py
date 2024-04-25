from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .grouping import group_participants
from .models import Participant, GroupingResult, Group
from django.contrib import messages

class ParticipantCreateView(CreateView):
    model = Participant
    fields = ['name', 'kana_name', 'average_score', 'gender' , 'email', 'transportation', 'postal_code', 'prefecture', 'city', 'address', 'building']
    template_name = 'participant_form.html'
    success_url = reverse_lazy('index')

def index(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('participants[]')
        print("選択された参加者ID:", selected_ids)
        selected_participants = Participant.objects.filter(id__in=selected_ids)
        if len(selected_participants) < 3:
            needed_participants = 3 - len(selected_participants)
            messages.error(request, f'参加者が足りません。あと{needed_participants}名の参加者が必要です。')
            return redirect('index')

        groups = group_participants(list(selected_participants))
        print(selected_participants)
        if any(len(group) < 3 for group in groups):
            messages.error(request, 'グループ分けに失敗しました。各グループは3名以上でなければなりません。')
            return redirect('index')

        grouping_result = GroupingResult()
        grouping_result.save()

        group_ids = []
        for group_members in groups:
            group = Group(result=grouping_result)
            group.save()
            for participant in group_members:
                group.participants.add(participant)
            group.save()
            group_ids.append(group.id)

        request.session['groups'] = group_ids  # セッションにグループIDを保存
        return redirect('group_results')
    else:
        participants = Participant.objects.all().order_by('kana_name')
        participant_count = participants.count()

        return render(request, 'index.html', {
            'participants': participants,
            'participant_count': participant_count
        })

def group_results(request):
    group_ids = request.session.get('groups', [])
    groups_with_sorted_participants = []
    for group_id in group_ids:
        group = Group.objects.get(id=group_id)
        sorted_participants = group.participants.all().order_by('average_score')
        groups_with_sorted_participants.append((group, sorted_participants))
   
    return render(request, 'group_results.html', {'groups_with_sorted_participants': groups_with_sorted_participants})

def delete_participants(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('delete_participants[]')
        Participant.objects.filter(id__in=selected_ids).delete()
        messages.success(request, '選択された参加者を削除しました。')
    return redirect('index')

def show_delete_participants_form(request):
    participants = Participant.objects.all()
    return render(request, 'delete_participants.html', {'participants': participants})

class ParticipantUpdateView(UpdateView):
    model = Participant
    fields = ['name', 'kana_name', 'average_score', 'gender', 'email', 'transportation', 'postal_code', 'prefecture', 'city', 'address', 'building']
    template_name = 'participant_edit_form.html'
    success_url = reverse_lazy('index')

def result_list(request):
    results = GroupingResult.objects.all().order_by('-created_at')
    return render(request, 'grouping_result_list.html', {'results': results})

def result_detail(request, result_id):
    result = GroupingResult.objects.get(id=result_id)
    groups = result.groups.all()
    return render(request, 'grouping_result_detail.html', {'result': result, 'groups': groups})

def get_group_ids(grouping_result_id):
    group_ids = Group.objects.filter(result_id=grouping_result_id).values_list('id', flat=True)
    return list(group_ids)