from personnel.models import Company
from pt.models import PtTest, PtScore

def get_complete_average_scores_dict(filter_expression=None):
    """
    The following code is used to get the average score for each for each company over a given set of scores.
    This returns a good amount of data, which is currently used to send to a bar flot chart to display
    side by side comparisons of how companies did over a given set of scores (per test, for every test, ect.)
    :param filter_expression: A kwargs dict used to filter the scores
    :return:
    """
    avg_overall_scores = {}
    avg_pushup_scores = {}
    avg_situp_scores = {}
    avg_run_scores = {}
    for company in Company.objects.all():
        scores = PtScore.objects.filter(cadet__company=company)
        if filter_expression:
            scores = scores.filter(**filter_expression)
        avg_overall_scores.update({company: PtScore.get_avg_total_score(scores)})
        avg_pushup_scores.update({company: PtScore.get_avg_pushup_score(scores)})
        avg_situp_scores.update({company: PtScore.get_avg_situp_score(scores)})
        avg_run_scores.update({company: PtScore.get_avg_run_score(scores)})
    context = \
        {
        'avg_overall_scores': avg_overall_scores,
        'avg_pushup_scores': avg_pushup_scores,
        'avg_situp_scores': avg_situp_scores,
        'avg_run_scores': avg_run_scores
        }
    return context


def get_avg_scores_by_company(company):
    """
    Returns a dictionary containing the average values of situps, pushups and two mile run times
    for the given Company object.
    Ex.
    To access the average situp value from the returned dictionary, you would do <dict_name>['situps']
    :param company: the company object to find the average scores of
    :return:
    """
    try:
        scores = PtScore.objects.filter(cadet__company=company)
        avg_score = {}

        situps = [score.get_situps() for score in scores]
        avg_situps = sum(situps) / float(len(situps))

        pushups = [score.get_pushups() for score in scores]
        avg_pushups = sum(pushups) / float(len(pushups))

        two_mile = [score.get_two_mile_min() for score in scores]
        avg_two_mile = sum(two_mile) / float(len(two_mile))

        return {
            'situps': avg_situps,
            'pushups': avg_pushups,
            'two_mile': avg_two_mile
        }
    except:
        pass