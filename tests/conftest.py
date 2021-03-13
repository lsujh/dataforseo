import pytest

from search.models import Tasks, DataSearch, Result


@pytest.fixture
def create_task(db):
    def make_task(**kwargs):
        kwargs["time"] = "0.0038 sec."
        kwargs["cost"] = 0.0015
        return Tasks.objects.create(**kwargs)

    return make_task


@pytest.fixture
def create_datasearch(db):
    def mark_datasearch(**kwargs):
        kwargs["api"] = "serp"
        kwargs["function"] = "task_post"
        kwargs["se"] = "google"
        kwargs["se_type"] = "organic"
        kwargs["language_code"] = "en"
        kwargs["location_code"] = 2840
        kwargs["keyword"] = "albert enstein"
        kwargs["device"] = "desktop"
        kwargs["os"] = "windows"
        return DataSearch.objects.create(**kwargs)

    return mark_datasearch


@pytest.fixture
def create_result(db):
    def mark_result(**kwargs):
        kwargs["type"] = "paid"
        kwargs["rank_group"] = 1
        kwargs["rank_absolute"] = 1
        kwargs["domain"] = "www.bookingbuddy.com"
        kwargs[
            "title"
        ] = "Flights To Lwo | Unbelievably Cheap Flights | BookingBuddy.com‎"
        kwargs[
            "description"
        ] = "Compare Airlines & Sites. Cheap Flights on BookingBuddy, a TripAdvisor Company"
        kwargs["url"] = "https://www.bookingbuddy.com/en/hero/"
        kwargs["breadcrumb"] = "www.bookingbuddy.com/Flights"
        return Result.objects.create(**kwargs)

    return mark_result
