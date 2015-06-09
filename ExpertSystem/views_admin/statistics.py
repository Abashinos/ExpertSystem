from django.views.generic import TemplateView
from ExpertSystem.utils.managers import get_statistics


class StatisticsView(TemplateView):
    template_name = 'admin/statistics.html'

    def get_context_data(self, **kwargs):

        statistics = get_statistics()

        return {
            'statistics': statistics
        }
