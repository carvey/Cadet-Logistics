from django.test import TestCase
from pt.models import PtScore, PtTest
from personnel.models import Cadet
from pyquery import PyQuery as pq
from populate_testing import create_graders
from populate_testing import add_cadet, add_mslevel, add_company, add_squad, add_platoon
import datetime
import requests


class ScoreConfirmationTests(TestCase):

    def setUp(self):
        create_graders()
        self.ms1 = add_mslevel('MS1')
        self.ms2 = add_mslevel('MS2')
        self.company = add_company('Alpha')
        self.platoon = add_platoon(1, self.company)
        self.squad = add_squad(1, self.platoon)
        self.test = PtTest(date=datetime.date.today())
        self.cadet = add_cadet('Joe', 'Cadet', 20, self.ms1, self.company, self.squad, "Male", self.platoon)

        self.cadet.save()
        self.test.save()

    def make_request(self, pu, su, ru, age, gender):
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

        # score = jquery(".scoretotal").eq(0).children().children().text()
        # passing = jquery(".scoretotal").eq(0).children().text()
        # pushup_score = jquery(".o").children().eq(2).text()
        # situp_score = jquery(".o").children().eq(3).text()
        # run_score = jquery(".o").children().eq(4).text()

        score = jquery(".scoretotal").eq(0).children().eq(0).text()
        passing = jquery(".scoretotal").eq(1).text()
        pushup_score = jquery('.o').children('td').eq(2).text()
        situp_score = jquery('.o').children('td').eq(4).text()
        run_score = jquery('.o').children('td').eq(6).text()

        if passing:
            passing = True
        else:
            passing = False

        return {
            'pushups': int(pushup_score),
            'situps': int(situp_score),
            'run': int(run_score),
            'score': int(score),
            'passing': passing
        }

    def test_male_19_21(self):
        # score = PtScore(cadet=self.cadet, pt_test=self.test, pushups=71, situps=78, two_mile='13:00')
        # score.save()
        for score in PtScore.objects.all():
            response_dict = self.make_request(score.pushups, score.situps, score.two_mile,
                                              score.cadet.get_age(), score.cadet.gender)

            self.assertEqual(response_dict['pushups'], score.pushups_score)
            self.assertEqual(response_dict['situps'], score.situps_score)
            self.assertEqual(response_dict['run'], score.run_score)
            self.assertEqual(response_dict['score'], score.score)
            self.assertEqual(response_dict['passing'], score.passing)
            print "All scores good for %s" % score