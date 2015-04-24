from django.test import TestCase
from pt.models import PtScore, PtTest, Grader
from personnel.models import Cadet
from populate_testing import create_graders
from populate_testing import add_cadet, add_mslevel, add_company, add_squad, add_platoon
from pt_utils.confirm_scores import *
import datetime


class ScoreConfirmationTests(TestCase):

    def setUp(self):
        create_graders()
        self.ms1 = add_mslevel('MS1')
        self.ms2 = add_mslevel('MS2')
        self.company = add_company('Alpha')
        self.platoon = add_platoon(1, self.company)
        self.squad = add_squad(1, self.platoon)
        self.test = PtTest(date=datetime.date.today())
        # self.cadet = add_cadet('Joe', 'Cadet', 20, self.ms1, self.company, self.squad, "Male", self.platoon)

        # self.cadet.save()
        self.test.save()

    def test_scores(self):
        scores = []
        for grader in Grader.objects.filter(activity="Situps"):
            min_age = int(grader.age_group[:2])
            max_age = int(grader.age_group[3:])

            for age in range(min_age, max_age):
                cadet = add_cadet(str(grader.gender) + str(age), "Cadet", age, self.ms1, self.company, self.squad, grader.gender, self.platoon)
                cadet.save()
                if grader.activity == "Situps":
                    print grader
                    min_pushups = int(grader.get_first())+2
                    max_pushups = int(grader.get_last())-2
                    for pushup_count in range(min_pushups, max_pushups):
                        print 'situp score for: %s --- %s situp' % (grader, pushup_count)
                        score = PtScore(cadet=cadet, pt_test=self.test, pushups=pushup_count, situps=0, two_mile="30:00")
                        score.save()
                        scores.append(score)

        for score in scores:
            response_dict = make_calculator_request(score.pushups, score.situps, score.two_mile,
                                              score.cadet.get_age(), score.cadet.gender)

            # self.assertEqual(response_dict['pushups'], score.pushups_score)
            # self.assertEqual(response_dict['situps'], score.situps_score)
            # self.assertEqual(response_dict['run'], score.run_score)
            # self.assertEqual(response_dict['score'], score.score)
            # self.assertEqual(response_dict['passing'], score.passing)

            pushup_score = response_dict['pushups']
            situp_score = response_dict['situps']
            run_score = response_dict['run']
            calculated_score = response_dict['score']
            passing = response_dict['passing']

            if not score.scores_match(pushup_score, situp_score, run_score, calculated_score, passing):
                print score.scores_diff(pushup_score, situp_score, run_score, calculated_score, passing)
                self.assertEqual(response_dict['pushups'], score.pushups_score)
                self.assertEqual(response_dict['situps'], score.situps_score)
                self.assertEqual(response_dict['run'], score.run_score)
                self.assertEqual(response_dict['score'], score.score)
                self.assertEqual(response_dict['passing'], score.passing)