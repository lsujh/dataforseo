from django.db import models


class Tasks(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    status_code = models.SmallIntegerField()
    status_message = models.CharField(max_length=20)
    time = models.CharField(max_length=20, blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.id


class DataSearch(models.Model):
    task = models.OneToOneField(
        Tasks, on_delete=models.CASCADE, related_name="task_search"
    )
    api = models.CharField(max_length=20, blank=True, null=True)
    function = models.CharField(max_length=20, blank=True, null=True)
    se = models.CharField(max_length=20)
    se_type = models.CharField(max_length=20, blank=True, null=True)
    language_code = models.CharField(max_length=20, blank=True, null=True)
    location_code = models.CharField(max_length=20, blank=True, null=True)
    keyword = models.CharField(max_length=1000)
    device = models.CharField(max_length=20, blank=True, null=True)
    os = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.task


class Result(models.Model):
    task = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, related_name="task_result"
    )
    type = models.CharField(max_length=20, blank=True, null=True)
    rank_group = models.SmallIntegerField(blank=True, null=True)
    rank_absolute = models.SmallIntegerField(blank=True, null=True)
    domain = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    url = models.URLField(max_length=2000, blank=True, null=True)
    breadcrumb = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.task
