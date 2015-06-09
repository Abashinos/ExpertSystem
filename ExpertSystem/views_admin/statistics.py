from django.views.generic import TemplateView


class StatisticsView(TemplateView):
    template_name = 'admin/statistics.html'

    def get_context_data(self, **kwargs):

        return {
        }
