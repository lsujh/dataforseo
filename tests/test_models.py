import pytest

from search.models import Result


@pytest.mark.django_db
def test_task_create(create_task):
    task = create_task(
        id="01291721-1535-0066-0000-8f0635c0dc89",
        status_message="Task Created.",
        status_code=20100,
    )
    assert task.status_code == 20100
    assert task.status_message == "Task Created."
    assert task.__str__() == "01291721-1535-0066-0000-8f0635c0dc89"


@pytest.mark.django_db
def test_datasearch_create(create_task, create_datasearch):
    task = create_task(
        id="01291721-1535-0066-0000-8f0635c0dc89",
        status_message="Ok.",
        status_code=20100,
    )
    data = create_datasearch(task=task)
    assert data.keyword == "albert enstein"
    assert data.language_code == "en"
    assert data.__str__() == task


@pytest.mark.django_db
def test_create_result(create_task, create_result):
    task = create_task(
        id="01291721-1535-0066-0000-8f0635c0dc89",
        status_message="Ok.",
        status_code=20000,
    )
    result = create_result(task=task)
    assert result.domain == "www.bookingbuddy.com"
    assert Result.objects.count() == 1
    assert result.__str__() == task
