import pytest
from django.contrib.messages.storage.fallback import FallbackStorage

from django.test import RequestFactory, Client
from django.urls import reverse

from search import views, models, forms


client = Client()
pytestmark = pytest.mark.django_db


class TestSearchFormView:
    def test_search_form_get(self):
        req = RequestFactory().get(reverse("search:search_form"))
        resp = views.SearchFormView.as_view()(req)
        assert resp.status_code == 200

    def test_post(self):
        data = dict(
            language_code="en",
            search_region="2010",
            search_engine="google",
            keyword="keyword",
        )
        form = forms.SearchForm(data=data)
        assert form.is_valid
        req = RequestFactory().post(reverse("search:search_form"), data=form.data)
        setattr(req, "session", "session")
        setattr(req, "_messages", FallbackStorage(req))
        resp = views.SearchFormView.as_view()(req)
        assert resp.status_code == 302
        assert models.Tasks.objects.count() == 1


class TestListResultView:
    def test_list_result(self, create_task, create_datasearch):
        task = create_task(
            id="01291721-1535-0066-0000-8f0635c0dc89",
            status_message="Task Created.",
            status_code=20100,
        )
        data_search = create_datasearch(task=task)
        req = RequestFactory().get(reverse("search:list_result"))
        resp = views.ListResult.as_view()(
            req, pk="01291721-1535-0066-0000-8f0635c0dc89", se=data_search.se
        )
        assert resp.status_code == 200


class TestResultView:
    def test_result(self, create_task, create_datasearch):
        task = create_task(
            id="01291721-1535-0066-0000-8f0635c0dc89",
            status_message="Downloaded",
            status_code=20000,
        )
        data_search = create_datasearch(task=task)
        req = RequestFactory().get(
            reverse("search:detail", kwargs={"pk": task.id, "se": data_search.se})
        )
        resp = views.DetailResult.as_view()(req, pk=task.id, se=data_search.se)
        assert resp.status_code == 200

    def test_result_upload(self, create_task, create_datasearch):
        task = create_task(
            id="01291721-1535-0066-0000-8f0635c0dc89",
            status_message="Ok.",
            status_code=20000,
        )
        data_search = create_datasearch(task=task)
        req = RequestFactory().get(
            reverse("search:detail", kwargs={"pk": task.id, "se": data_search.se})
        )
        resp = views.DetailResult.as_view()(req, pk=task.id, se=data_search.se)
        assert resp.status_code == 200


