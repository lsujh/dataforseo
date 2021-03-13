from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings

from .forms import SearchForm
from .client import RestClient
from countries import ENGINE
from .models import Tasks, DataSearch, Result

client = RestClient(settings.LOGIN, settings.PASSWORD)


class SearchFormView(FormView):
    template_name = "search/search_form.html"
    form_class = SearchForm
    success_url = reverse_lazy("search:search_form")

    def form_valid(self, form):
        cd = form.cleaned_data
        post_data = dict()
        post_data[len(post_data)] = dict(
            language_code="en",
            location_code=cd["search_region"],
            keyword=cd["keyword"],
        )
        response = client.post(
            f"/v3/serp/{cd['search_engine']}/organic/task_post", post_data
        )
        if (
            response["status_code"] == 20000
            and response["tasks"][0]["status_code"] == 20100
        ):
            res = response["tasks"][0]
            task = Tasks.objects.create(
                id=res["id"],
                status_code=res["status_code"],
                status_message=res["status_message"],
                time=res["time"],
                cost=res["cost"],
            )
            data = DataSearch.objects.create(task=task, **res["data"])
            task.save()
            data.save()
            messages.success(
                self.request,
                'The task has been created. To view the status of a task, click the "Task Status" button',
            )
        else:
            messages.error(
                self.request,
                "error. Code: %d Message: %s"
                % (response["status_code"], response["status_message"]),
            )
        return HttpResponseRedirect(self.get_success_url())


class ListResult(ListView):
    template_name = "search/list_result.html"
    paginate_by = 10
    context_object_name = "results"

    def get_queryset(self):
        for engine in ENGINE:
            response = client.get(f"/v3/serp/{engine[0]}/organic/tasks_ready")
            if response["status_code"] == 20000:
                for task in response["tasks"]:
                    if task["result"]:
                        for result in task["result"]:
                            Tasks.objects.filter(id=result["id"]).update(
                                status_code=task["status_code"],
                                status_message=task["status_message"],
                            )
            else:
                messages.error(
                    self.request,
                    "error. Code: %d Message: %s"
                    % (response["status_code"], response["status_message"]),
                )
        results = Tasks.objects.all().select_related()
        return results


class DetailResult(ListView):
    template_name = "search/detail_result.html"
    context_object_name = "results"

    def get_queryset(self):
        pk = self.kwargs["pk"]
        engine = self.kwargs["se"]
        task_id = Tasks.objects.filter(id=pk).first()
        results = []
        if task_id.status_message == "Downloaded":
            results = Result.objects.filter(task=task_id)
            return results
        response = client.get(f"/v3/serp/{engine}/organic/task_get/regular/{pk}")
        if response["status_code"] == 20000:
            task = response["tasks"][0]
            if task["result"] and (len(task["result"]) > 0):
                for result in task["result"]:
                    res = []
                    if result["items"]:
                        for item in result["items"]:
                            item["task"] = task_id
                            res.append(item)
                        Result.objects.bulk_create([Result(**i) for i in res])
                        Tasks.objects.filter(id=pk).update(status_message="Downloaded")
                    else:
                        Tasks.objects.filter(id=pk).update(
                            status_message="No Search Results."
                        )
                        messages.error(self.request, "No Search Results.")
                        return

            results = Result.objects.filter(task=task_id)
        else:
            messages.error(
                self.request,
                "error. Code: %d Message: %s"
                % (response["status_code"], response["status_message"]),
            )
        return results
