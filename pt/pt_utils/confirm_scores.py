
from pt.models import PtScore
from pyquery import PyQuery as pq
import requests


class ScoresConfirmation():
    """
    This class can handle testing pt scores generated in Eagletrack with scores generated at apftscore.com
    """

    #TODO should be able to test all scores or one off scores
    def __init__(self):
        pass

    def make_calculator_request(self, pu, su, ru, age, gender):
        """
        Should make the request to apftscore.com to check Eagletrack scoring
        :param pu: Raw pushup count
        :param su: Raw situp count
        :param ru: Raw run time
        :param age: Age
        :param gender: Gender
        :return: The parsed response content containing the scores for the test
        """
        payload = {'soldier[0][pu]': pu, 'soldier[0][su]': su, 'soldier[0][ru]': ru,
                   'soldier[0][age]': age, 'soldier[0][gender]': gender}

        header = {"Content-Type": "application/x-www-form-urlencoded"}

        return self.parse_request(requests.post('http://apftscore.com/score.php', headers=header, data=payload))

    def parse_request(self, response):
        """
        This method should parse the response of a POSTed response to http://apftscore.com/score.php
        :param response: the response object whose content should be parsed
        :return: A dict with the score for each event
        """
        jquery = pq(response.content)

        score = jquery(".scoretotal").eq(0).children().eq(0).text()
        passing = jquery(".scoretotal").eq(1).text()
        pushup_score = jquery('.o').children('td').eq(2).text()
        situp_score = jquery('.o').children('td').eq(4).text()
        run_score = jquery('.o').children('td').eq(6).text()

        if passing == "Pass":
            passing = True
        elif passing == "Fail":
            passing = False

        return {
            'pushups': int(pushup_score),
            'situps': int(situp_score),
            'run': int(run_score),
            'score': int(score),
            'passing': passing
        }

    def test_current_scores(self):
        for score in PtScore.objects.all():
            response_dict = self.make_calculator_request(score.pushups, score.situps, score.two_mile,
                                              score.cadet.get_age(), score.cadet.gender)

            error = None
            if response_dict['pushups'] != score.pushups_score:
                error = "Wrong pushups calculation for %s" % score
                print "%s --- Eagletrack: %s, Calculator: %s" % (error, score.pushups_score, response_dict['pushups'])
            if response_dict['situps'] != score.situps_score:
                error = "Wrong situps calculation for %s" % score
                print "%s --- Eagletrack: %s, Calculator: %s" % (error, score.situps_score, response_dict['situps'])
            if response_dict['run'] != score.run_score:
                error = "Wrong two mile calculation for %s" % score
                print "%s --- Eagletrack: %s, Calculator: %s" % (error, score.run_score, response_dict['run'])
            if response_dict['score'] != score.score:
                error = "Wrong score calculation for %s" % score
                print "%s --- Eagletrack: %s, Calculator: %s" % (error, score.score, response_dict['score'])
            if response_dict['passing'] != score.passing:
                error = "Wrong passing calculation for %s" % score
                print "%s --- Eagletrack: %s, Calculator: %s" % (error, score.passing, response_dict['passing'])

            if not error:
                print "All scores good for %s" % score