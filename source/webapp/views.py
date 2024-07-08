from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.forms import IssueForms
from webapp.models import Issue
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        context = {
            'issues': issues
        }
        return render(request, 'index.html', context)


class IssueView(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = get_object_or_404(Issue, pk=kwargs.get('pk'))
        return context


class IssueCreateView(TemplateView):
    template_name = 'issue_create.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IssueForms()
        return render(request, 'issue_create.html', context=context)

    def post(self, request, *args, **kwargs):
        form = IssueForms(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop('types')
            issue = Issue.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
            )
            issue.types.set(types)
            return redirect('issue_view', pk=issue.pk)
        return render(request, 'issue_create.html', {'form': form})


class IssueUpdateView(TemplateView):
    template_name = 'issue_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        form = IssueForms(initial={
            'summary': issue.summary,
            'description': issue.description,
            'status': issue.status,
            'types': issue.types.all()
        })
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        form = IssueForms(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop('types')
            issue.summary = form.cleaned_data.get('summary')
            issue.description = form.cleaned_data.get('description')
            issue.status = form.cleaned_data.get('status')
            issue.types.set(types)
            issue.save()
            return redirect('issue_view', pk=issue.pk)
        else:
            return render(request, 'issue_update.html', {'form': form})


class IssueDeleteView(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs.get('pk'))
        return render(request, 'issue_delete.html', {'issue': issue})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Issue, pk=kwargs.get('pk'))
        task.delete()
        return redirect('index')



