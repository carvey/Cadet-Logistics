import ast, collections
import datetime

from itertools import cycle

from django.db import models
from personnel.models import Cadet, MsLevel, Squad, Platoon
from django.core.validators import RegexValidator

from decimal import Decimal
from pt.managers import FilteredTestManager, FutureTestManager

male = 'Male'
female = 'Female'
GENDER_CHOICES = (
    (male, 'Male'),
    (female, 'Female')
)
group_1 = '17-21'
group_2 = '22-26'
group_3 = '27-31'
group_4 = '32-36'
group_5 = '37-41'
group_6 = '42-46'
group_7 = '47-51'
group_8 = '52-56'

AGE_GROUPS = (
    (group_1, '17-21'),
    (group_2, '22-26'),
    (group_3, '27-31'),
    (group_4, '32-36'),
    (group_5, '37-41'),
    (group_6, '42-46'),
    (group_7, '47-51'),
    (group_8, '52-56')
)
pushups = 'Pushups'
situps = 'Situps'
two_mile = 'Two-mile run'
ACTIVITY_CHOICES = (
    (pushups, 'Pushups'),
    (situps, 'Situps'),
    (two_mile, 'Two-mile run')
)


# This class handles the pt test itself, identified by a date
class PtTest(models.Model):
    date = models.DateField(default=datetime.date.today(), blank=False)
    ms_levels = models.ManyToManyField(MsLevel)
    record = models.BooleanField(default=False)
    diagnostic = models.BooleanField(default=False)

    objects = models.Manager()
    filtered_tests = FilteredTestManager()
    future_tests = FutureTestManager()

    def __unicode__(self):
        format_date = self.date.strftime('%d %b, %Y')
        return '%s PT Test' % format_date

    def formatted_date(self):
        """
        To be used for full calendar event objects
        :return: A Y-m-d formatted date string
        """
        return self.date.strftime('%Y-%m-%d')

    def has_past(self):
        if datetime.date.today() > self.date:
            return True
        return False

    def passing_rate(self):
        """
        This method calculates the passing rate for a particular instance
        :return: a percantage of the passing rate
        :type return: Decimal
        """
        passing = Decimal(PtScore.objects.filter(pt_test=self, passing=True).count())
        failing = Decimal(PtScore.objects.filter(pt_test=self, passing=False).count())
        if failing == 0 and passing == 0:
            return 0
        rate = (passing/failing * 100).quantize(Decimal(10) ** -2)

        return rate

    def getNumberOfScores(self):
        return len(PtScore.objects.filter(pt_test=self))

    def getHighestScore(self):
        scores = PtScore.objects.filter(pt_test=self)
        if not scores:
            return 0
        highest_score = scores[0].score
        for score in scores:
            if score.score > highest_score:
                highest_score = score.score

        return highest_score

    def get_highest_scoring_cadet(self, scores):
        highest_scoring_cadet = scores[0].cadet
        highest_score = scores[0]
        for score in scores:
            if score.score > highest_score.score:
                highest_score = score
                highest_scoring_cadet = score.cadet
        #returns {cadet : score}
        return {highest_scoring_cadet: highest_score}

    @staticmethod
    def order_scores_dict(scores, n):
        """
        Will take a dict and generate a dict of n of the top scores
        :param scores: The dict to be evaluated. Should be in the format {score: cadet/grouping, ...}
        :type scores: dict
        :param n: the number of top scores to return
        :type n: int
        :return: The top n scores and their respective cadet/grouping
        :type return: OrderedDict
        """
        #TODO: Can this be done with some lambda function instead? Might be complex, but worth checking out
        top_scores = collections.OrderedDict()
        for count in range(0, n):
            # this conditional will break the loop if scores_dict runs out of scores
            # this would happen, and cause errors, when n > len(scores)
            if scores:
                highest_score = max(scores)
                top_scores.update({highest_score: scores[highest_score]})
                scores.pop(highest_score)
            else:
                break
        return top_scores

    def grouping_has_scores(self, grouping):
        cadets = grouping.cadets.all()
        scores = self.ptscore_set.filter(cadet__in=cadets)
        return bool(scores)

    #returns the n highest scores over a set/subset of cadets
    def get_n_highest_scores(self, filter_expression=None, n=5):
        """
        Get the cadets with the top overall pt scores for this test
        :param n: the number of top cadets to return. Default=5
        :param filter_expression: an expression to further filter the scores to be evaluated
        :return: a sorted dict (descending order) of {score: cadet} or {score: [cadet, cadet, ...]} pairs
        """
        scores = PtScore.objects.filter(pt_test=self)
        if filter_expression:
            scores = scores.filter(**filter_expression)
        scores_dict = {}
        #The following loop is to consolidate all of the scores into a dict - {score: cadet}
        for score in scores:
            #if there is a repeat score (ex: 1st and 2nd place cadets both have 300s)
            if score.score in scores_dict:
                #if this value is already a list (more than 2 cadets with score score already), then append the cadet
                if isinstance(scores_dict[score.score], list):
                    scores_dict[score.score].append(score.cadet)
                #if this is the first occurrence of repeated scores, then make a list out of the two cadets
                else:
                    scores_dict[score.score] = [scores_dict[score.score], score.cadet]
            #no repeated scores, so just insert the score and cadet as a default key,value pair
            else:
                scores_dict.update({score.score: score.cadet})
        #Get the highest scores from scores_dict and put them in a separate dict to be returned
        top_scores = PtTest.order_scores_dict(scores_dict, n)
        return reversed(sorted(top_scores.items()))

    def get_n_highest_squads(self, n=5):
        squads = Squad.objects.all()
        squad_scores = {}
        for squad in squads:
            if self.grouping_has_scores(squad):
                squad_scores[self.get_average_score(squad=squad)] = squad
        top_squads = PtTest.order_scores_dict(squad_scores, n)
        return reversed(sorted(top_squads.items()))

    def get_n_highest_platoons(self, n=5):
        platoons = Platoon.objects.all()
        platoon_scores = {}
        for platoon in platoons:
            if self.grouping_has_scores(platoon):
                platoon_scores[self.get_average_score(platoon=platoon)] = platoon
        top_platoons = PtTest.order_scores_dict(platoon_scores, n)
        return reversed(sorted(top_platoons.items()))

    def get_average_score(self, company=None, platoon=None, squad=None):
        scores = PtScore.objects.filter(pt_test=self)
        if company:
            scores = scores.filter(cadet__company=company)
        elif platoon:
            scores = scores.filter(cadet__platoon=platoon)
        elif squad:
            scores = scores.filter(cadet__squad=squad)
        return PtScore.get_avg_total_score(scores)

    def get_optimal_cadet_count(self):
        ms_classes = [ms for ms in self.ms_levels.all()]
        return Cadet.objects.filter(ms_level__in=ms_classes).count()

    def get_actual_cadet_count(self):
        return self.ptscore_set.all().count()

    def get_missing_record_count(self):
        return self.get_optimal_cadet_count() - self.get_actual_cadet_count()

    class Meta:
        db_table = 'PtTest'


#The PTscore information for each cadet. Indentified by a foreign key linking to a specific cadet
class PtScore(models.Model):
    cadet = models.ForeignKey('personnel.Cadet', related_name='cadet_score', blank=False)
    pt_test = models.ForeignKey(PtTest, default='', blank=False, null=False)
    grader = models.ForeignKey('personnel.Cadet', related_name='grader', blank=True, null=True)
    cadre_grader = models.ForeignKey('personnel.Cadre', blank=True, null=True)

    pushups = models.PositiveIntegerField(default=0)
    situps = models.PositiveIntegerField(default=0)
    two_mile = models.CharField(max_length=5, null=True, validators=[
        RegexValidator(
            regex='^[0-5]?[0-9]:[0-5]?[0-9]',
            message="Time must be in the mm:ss format",
            code="Invalid_time_format"
        ),
    ])

    score = models.PositiveIntegerField(default=0)
    pushups_score = models.PositiveIntegerField(default=0)
    situps_score = models.PositiveIntegerField(default=0)
    run_score = models.PositiveIntegerField(default=0)

    passing = models.BooleanField(default=False)

    def __unicode__(self):
        format_date = self.pt_test.date.strftime('%d %b, %Y')
        return 'PT Score %s for cadet: %s' % (format_date, self.cadet)


    @staticmethod
    def assemble_instance(cadet_id=None, raw_situps=None, raw_pushups=None, run_time=None):
        """
        Used to assemble a cadet instance based on raw scores and a cadet id.
        :param cadet_id: The id of the cadet to calculate the scores for
        :param raw_situps: the raw number of situps to calculate for
        :param raw_pushups: the raw number of pushups to calculate for
        :param run_time: the raw run time to calculate for. Use mm:ss format
        :return: a non committed PtScore instance
        """
        cadet = Cadet.objects.get(id=cadet_id)
        raw_pushups = int(raw_pushups)
        raw_situps = int(raw_situps)
        run_time = str(run_time)
        instance = PtScore(cadet=cadet, pushups=raw_pushups, situps=raw_situps, two_mile=run_time)
        return instance

    @staticmethod
    def calculate_score(instance=None):
        """
        Static method that will calculate the PT score based on a pt instance that already has a cadet and the
        three raw scores assigned.
        This method does not save that instance to the database.\n

        If a score needs to be calculated and an instance has not been assembled yet, use the assemble_instance
        method to get the instance
        --

        :param instance: the instance to calculate the score on
        :type instance: PtScore
        :return: {'score': calculated_score, 'passing': True/False'}
        :type return: dict
        """

        age_group = instance.get_age_group()
        # Gets the graders for the cadet
        pushups_grader = Grader.objects.filter(age_group=age_group, gender=instance.cadet.gender, activity='Pushups')[0]
        situps_grader = Grader.objects.filter(age_group=age_group, gender=instance.cadet.gender, activity='Situps')[0]
        two_mile_grader = Grader.objects.filter(age_group=age_group, gender=instance.cadet.gender, activity='Two-mile run')[0]

        # Sets the score to zero to prevent the score increasing each time the object
        # is saved, if there is already a score
        instance.score = 0

        # Get the score dictionary from the pushups grader object
        pushups_score_dict = pushups_grader.get_ordered_dict()
        # Format the value to have a leading 0 if it is a single digit
        # This is the key used to check if the value is in the dictionary of grades
        string_pushups = "%02d" % instance.pushups
        # Check to see if the number of pushups for the PtScore object is
        # in the list of keys. If it is then we use the pushups value as the key to get the grade.
        if string_pushups in pushups_score_dict.keys():
            score_from_dict = int(pushups_score_dict[string_pushups])
            instance.pushups_score = score_from_dict
            instance.score += score_from_dict
        # The value of pushups was not found in the keys so we determine if it was below the lowest
        # or above the highest pushups value
        else:
            if float(instance.pushups) < float(pushups_grader.get_first()):
                instance.pushups_score = 0
                instance.score += instance.pushups_score
            elif float(instance.pushups) > float(pushups_grader.get_last()):
                instance.pushups_score = 100
                instance.score += instance.pushups_score

        # Get the score dictionary from the situps grader object
        situps_score_dict = situps_grader.get_ordered_dict()

        # Format the value to have a leading 0 if it is a single digit
        # This is the key used to check if the value is in the dictionary of grades
        string_situps = "%02d" % instance.situps
        # Check to see if the number of situps for the PtScore object is
        # in the list of keys. If it is then we use the situps value as the key to get the grade.
        if string_situps in situps_score_dict.keys():
            score_from_dict = int(situps_score_dict[string_situps])
            instance.situps_score = score_from_dict
            instance.score += instance.situps_score

        # The value of situps was not found in the keys so we determine if it was below the lowest
        # or above the highest situps value
        else:
            if float(instance.situps) < float(situps_grader.get_first()):
                instance.situps_score = 0
                instance.score += instance.situps_score
            elif float(instance.situps) > float(pushups_grader.get_last()):
                instance.situps_score = 100
                instance.score += instance.situps_score

        # Calculate the two-mile score
        if instance.empty_run_time():  # checks to see whether a value has been entered
            instance.run_score = 0
        else:
            instance.run_score = int(instance.get_run_score(two_mile_grader))
        instance.score += instance.run_score

        if instance.situps_score >= 60 and instance.pushups_score >= 60 and instance.run_score >= 60:
                instance.passing = True


        return {'score': instance.score,
                'passing': instance.passing}

    def save(self, *args, **kwargs):
        PtScore.calculate_score(instance=self)

        # Call the actual save method to save the score in the database
        super(PtScore, self).save(*args, **kwargs)

    def empty_run_time(self):
        """
        Checks if the time contains only zeros
        :return:
        """
        time = self.two_mile
        for char in time:
            if char != ':':
                if int(char) != 0:
                    return False
        return True

    @staticmethod
    def valid_run_time(run_string):
        """
        To be used when a run string needs to be input by the user
        :param run_string:
        :return:
        """
        if not ':' in run_string or run_string.count(':') != 1:
            return False

        for char in run_string:
            if char != ':':
                if not char.isdigit():
                    return False
        return True

    @staticmethod
    def get_top_cadets(cadets, n=5):
        """
        Get the cadets with the top average pt scores
        :param cadets: the cadets (or subset of cadets) to be sorted and ranked
        :param n: the number of top cadets to return. Default=5
        :return: a sorted dict (descending order) of {score: cadet} or {score: [cadet, cadet, ...]} pairs
        """
        all_scores = PtScore.objects.all()
        avg_scores = {}
        for cadet in cadets:
            scores = all_scores.filter(cadet=cadet)
            avg_scores[cadet] = PtScore.get_avg_total_score(scores)
        avg_scores = collections.OrderedDict(reversed(sorted(avg_scores.items(), key=lambda t: t[1])))
        top_scores = collections.OrderedDict()
        count = 0
        for cadet, score in avg_scores.items():
            count += 1
            #if there is a repeat score (ex: 1st and 2nd place cadets both have 300s)
            if score in top_scores:
                #if this value is already a list (more than 2 cadets with score score already), then append the cadet
                if isinstance(top_scores[score], list):
                    top_scores[score].append(cadet)
                #if this is the first occurrence of repeated scores, then make a list out of the two cadets
                else:
                    top_scores[score] = [top_scores[score], cadet]
            #no repeated scores, so just insert the score and cadet as a default key,value pair
            else:
                top_scores.update({score: cadet})
            #the number of top cadets to get
            if count == n:
                break
        return reversed(sorted(top_scores.items()))

    @staticmethod
    def get_worst_cadets(cadets, n=5):
        all_scores = PtScore.objects.all()
        avg_scores = {}
        for cadet in cadets:
            scores = all_scores.filter(cadet=cadet)
            if scores:
                avg_scores[cadet] = PtScore.get_avg_total_score(scores)
        avg_scores = collections.OrderedDict(sorted(avg_scores.items(), key=lambda t: t[1]))
        top_scores = collections.OrderedDict()
        count = 0
        for cadet, score in avg_scores.items():
            count += 1
            #if there is a repeat score (ex: 1st and 2nd place cadets both have 300s)
            if score in top_scores:
                #if this value is already a list (more than 2 cadets with score score already), then append the cadet
                if isinstance(top_scores[score], list):
                    top_scores[score].append(cadet)
                #if this is the first occurrence of repeated scores, then make a list out of the two cadets
                else:
                    top_scores[score] = [top_scores[score], cadet]
            #no repeated scores, so just insert the score and cadet as a default key,value pair
            else:
                top_scores.update({score: cadet})

            #the number of top cadets to get
            if count == n:
                break
        return sorted(top_scores.items())

    @staticmethod
    def get_max_score(scores):
        max_score = 0
        for score in scores:
            if score.score > max_score:
                max_score = score.score
        return max_score

    @staticmethod
    def get_min_score(scores):
        min_score = scores[0].score
        for score in scores:
            if score.score < min_score:
                min_score = score.score
        return min_score

    @staticmethod
    def get_avg_pushups(scores):
        """Returns the avg **number** of pushups over the given set of scores"""
        sum_pushups = 0
        length = len(scores)
        for score in scores:
            sum_pushups += int(score.pushups)
        avg = sum_pushups / length
        return avg

    @staticmethod
    def get_avg_pushup_score(scores):
        """Returns the avg **score** for the number of pushups over the given set of scores.
        Note that this function takes the average of the scores for each PtScore, it does not get
        the score of the average pushup count. These two numbers can be different."""
        avg_pushup_score = 0
        for score in scores:
            avg_pushup_score += score.pushups_score
        if scores.count():
            avg = avg_pushup_score / scores.count()
        else:
            avg = 0
        return avg

    @staticmethod
    def get_avg_situps(scores):
        """Returns the avg **number** of situps over the given set of scores"""
        sum_situps = 0
        length = len(scores)
        for score in scores:
            sum_situps += int(score.situps)
        if length:
            avg = sum_situps / length
        else:
            avg = 0
        return avg

    @staticmethod
    def get_avg_situp_score(scores):
        """Returns the avg **score** for the number of situps over the given set of scores
        Note that this function takes the average of the scores for each PtScore, it does not get
        the score of the average situp count. These two numbers can be different."""
        avg_situp_score = 0
        for score in scores:
            avg_situp_score += score.situps_score
        if scores.count():
            avg = avg_situp_score / scores.count()
        else:
            avg = 0
        return avg

    @staticmethod
    def get_avg_run_time(scores):
        """Returns the avg **time** over the given set of scores"""
        sum_time = 0
        length = len(scores)
        for score in scores:
            time = score.get_two_mile_min()
            sum_time = sum_time + time
        avg = str(sum_time / length)
        return scores[0].convert_time_mins_secs(avg)

    @staticmethod
    def get_avg_run_score(scores):
        """Returns the avg run **score** of the given set of scores
        Note that this function takes the average of the scores for each PtScore, it does not get
        the score of the average run time. These two numbers can be different."""
        avg_run_score = 0
        for score in scores:
            avg_run_score += score.run_score
        if scores.count():
            avg = avg_run_score / scores.count()
        else:
            avg = 0
        return avg


    @staticmethod
    def get_avg_total_score(scores):
        """Returns the avg **score** over the given set of scores"""
        sum = 0
        length = len(scores)
        for score in scores:
            sum += int(score.score)
        if length:
            avg = sum / length
        else:
            avg = 0
        return avg

    def get_run_time(self):
        """
         This method takes the two_mile info (CharField) of the cadet at hand and splits it into a list
         So a time of 15:43 should return a list value of [15, 43]
        """
        time = str(self.two_mile)
        split_time = time.split(':')
        split_time = [int(x) for x in split_time]
        return split_time

    def get_run_time_str(self):
        """
         Helper method to return the run time with
         a zero place holder if the minutes has
         only one number. So a time of 15:4 will
         be returned as 15:04.
        """
        time = self.get_run_time()
        return '%02d:%02d' % (time[0], time[1])

    def get_pt_test(self):
        return self.pt_test

    def get_pushups(self):
        return self.pushups

    def get_situps(self):
        return self.situps

    def get_two_mile_min(self):
        """
         Helper method to get the two mile time
         in minutes for computation. So a time of
         15:43 will be returned as 15.72 minutes
        """
        time_list = self.get_run_time()
        minutes = time_list[0]
        seconds = time_list[1]
        return minutes + (seconds / 60.0)

    def get_time_mins(self, time):
        """
         Converts a given time string in the form of '[mm]:[ss]' into a decimal minutes format
         So a time of '13:30' will be returned as 13.5
        """
        time_list = time.split(':')
        time_list = [int(t) for t in time_list]
        minutes = time_list[0]
        seconds = time_list[1]
        return minutes + (seconds / 60.0)

    def convert_time_mins_secs(self, time):
        """
         Converts a given time string from minutes into the form '[mm]:[ss]'.
         So a time of '13.5' will be returned as '13:30'
        """
        time_split = time.split('.')
        minutes = float(time_split[0])
        formatted_seconds = (float(time) - minutes) * 60.0
        return '%02.0f:%02.0f' % (minutes, formatted_seconds)

    def get_age_group(self):
        """
         Gets the age range that a cadet is a part of. Used for getting the correct Grader (score value) object
        """
        score_values = Grader.objects.all()

        cadet_age = self.cadet.get_age()
        for score_value in score_values:
            value = score_value.age_group.split('-')
            if cadet_age >= int(value[0]) and cadet_age <= int(value[1]):
                return score_value.age_group

    def get_run_score(self, two_mile_grader):
        """
         Used to calculate the score for two-mile run
        """
        # Gets the list of keys in minute format, so a key of '17:30' will be represented
        # as '17.5'
        times_in_mins_list = [self.get_time_mins(time) for time in two_mile_grader.get_ordered_dict()]

        # The two-mile time for this score object, in minute format
        run_time = self.get_two_mile_min()

        # Creates a cycle to iterate through the key values
        times_cycle = cycle(times_in_mins_list)

        # Store the first time in the list, so that in the for loop we can tell when the cycle
        # is complete since the next_time will be equal to the first_time
        first_time = times_in_mins_list[0]

        # Gets the next time in the list before we begin the loop
        next_time = times_cycle.next()

        # Time key defaults to zero
        time_key = 0

        # Iterate through the list of keys
        for time in times_in_mins_list:
            # Get the current time object in the list, and also the next time object
            this_time, next_time = time, times_cycle.next()

            # If this is true we found an exact match, so return the current time value as the key
            if run_time == this_time:
                time_key = this_time

            # Check to see if our two-mile time is between this_time and next_time. Also makes sure
            # that we aren't at the end of the cycle by checking that next_time is not equal to first_time.
            # If true we return next_time as the key, since it is the slower of the two times.
            elif run_time > this_time and run_time < next_time and next_time != first_time:
                time_key = next_time
            # Checks if run_time is less than this_time and if this_time is the first time in the list.
            # If so it means they had a faster time than the fastest time on the scale, so they make a 100.
            elif run_time < this_time and this_time == first_time:
                time_key = 100

        # If time_key is equal to zero it means that their time was too slow and was not on the scale,
        # so they make a 0.
        if time_key == 0:
            return 0
        elif time_key == 100:
            return 100
        else:
            # Convert the key from decimal minute format back to mm:ss format
            score_key = self.convert_time_mins_secs(str(time_key))
            # Get the grade from the grader dictionary
            grade = two_mile_grader.get_ordered_dict()[str(score_key)]

            return grade


    class Meta:
        db_table = 'PtScore'


class Grader(models.Model):
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False, null=True)
    activity = models.CharField(max_length=15, choices=ACTIVITY_CHOICES, blank=False, null=True)
    age_group = models.CharField(max_length=5, choices=AGE_GROUPS, blank=False, null=True)
    score_table = models.TextField(default="'number pushups or situps/time' : 'grade', \
        'number pushups or situps/time' : 'grade'", blank=False)

    def __unicode__(self):
        return '%s grader for %s (%s)' % (self.activity, self.gender, self.age_group)

    def get_score_dict(self):
        return ast.literal_eval("{%s}" % self.score_table)

    def get_ordered_dict(self):
        return collections.OrderedDict(sorted(self.get_score_dict().items()))

    def get_first(self):
        ordered_dict = self.get_ordered_dict()
        return next(ordered_dict.iterkeys())

    def get_last(self):
        ordered_dict = self.get_ordered_dict()
        return next(reversed(ordered_dict))