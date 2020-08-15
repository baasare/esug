from django.contrib import messages
from django.shortcuts import render, redirect

from election.forms import QueryForm
from election.models import Position, Candidate, Vote, Voter


def index(request):
    if request.method == 'GET':
        form = QueryForm()
    else:
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.save()
            return redirect('index')
        else:
            args = {'form': form}
            return render(request, 'election/index.html', args)

    args = {'form': form}
    return render(request, "election/index.html", args)


def candidates(request):
    pos = {}
    context = {}

    try:
        positions = Position.objects.filter(election__is_active=True).order_by("-my_order")
        all_candidates = Candidate.objects.filter(position__election__is_active=True)
        for position in positions:
            pos[position.name] = Vote.objects.filter(candidate__position=position)

        context['positions'] = positions
        context['candidates'] = all_candidates
        context['votes'] = pos

        return render(request, "election/candidates.html", context)
    except Position.DoesNotExist:
        return render(request, "election/candidates.html", context)


def candidate_detail(request, candidate_id):
    context = {}
    candidate = Candidate.objects.get(id=candidate_id)
    context['candidate'] = candidate

    return render(request, "election/candidate-details.html", context)


def vote(request):
    positions = Position.objects.filter(election__is_active=True, contestable=True).order_by("-my_order")
    context = {}

    if request.method == 'GET':
        # if request.session.get('browser_has_been_used'):
        #     del request.session['browser_has_been_used']

        if positions.count() > 0:
            all_candidates = {}
            print(positions.count())
            for position in positions:
                all_candidates[position.name] = Candidate.objects.filter(position=position).order_by("my_order")
            context['candidates'] = all_candidates
        else:
            messages.info(request, "No candidate available.")
            return redirect('vote')

    elif request.method == 'POST':
        selected_voter_pass_code = request.POST["pass_code"]

        try:
            selected_voter = Voter.objects.get(pass_code=selected_voter_pass_code)
            current_vote = Vote.objects.filter(voter_id=selected_voter).exists()

            if current_vote:
                messages.error(request, selected_voter.full_name + ", your pass code has already been used.")
                return redirect('vote')
            else:
                if request.session.get('browser_has_been_used'):
                    messages.info(request, 'Sorry you can only vote once')
                    return redirect('results')
                else:
                    for position in positions:
                        if position.name in request.POST:
                            selected_candidate_id = request.POST[position.name]
                            selected_candidate = Candidate.objects.get(pk=selected_candidate_id)

                            new_vote = Vote(voter=selected_voter, candidate=selected_candidate)
                            new_vote.save()

                            selected_candidate.votes.add(new_vote)
                            selected_candidate.save()

                            request.session['browser_has_been_used'] = True

                request.session['browser_has_been_used'] = True
            return redirect('results')
        except Voter.DoesNotExist:
            messages.error(request, "Incorrect Passcode.")
            return redirect('vote')

    return render(request, 'election/vote.html', context)


def results(request):
    context = {}
    positions = Position.objects.filter(election__is_active=True, contestable=True)

    if request.method == 'GET':
        all_candidates = {}
        pos = {}
        for position in positions:
            all_candidates[position.name] = Candidate.objects.filter(position=position).order_by('-full_name')
            pos[position.name] = Vote.objects.filter(candidate__position=position)

        context['candidates'] = all_candidates
        context['votes'] = pos

    return render(request, 'election/results.html', context)
