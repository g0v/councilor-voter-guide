# -*- coding: utf-8 -*-
from haystack import indexes

from .models import Suggestions


class SuggestionsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    uid = indexes.CharField(model_attr='uid')
    county = indexes.CharField(model_attr='county')
    election_year = indexes.CharField(model_attr='election_year')
    suggest_year = indexes.CharField(model_attr='suggest_year')
    suggest_month = indexes.CharField(model_attr='suggest_month')
    suggestion = indexes.CharField(model_attr='suggestion')
    position = indexes.CharField(model_attr='position')
    suggest_expense = indexes.IntegerField(default=0, model_attr='suggest_expense')
    suggest_expense_avg = indexes.IntegerField(default=0, model_attr='suggest_expense_avg')
    approved_expense = indexes.IntegerField(default=0, model_attr='approved_expense')
    approved_expense_avg = indexes.IntegerField(default=0, model_attr='approved_expense_avg')
    expend_on = indexes.CharField(default=None, model_attr='expend_on')
    brought_by = indexes.CharField(default=None, model_attr='brought_by')
    bid_type = indexes.CharField(default=None, model_attr='bid_type')
    bid_by = indexes.MultiValueField(model_attr='bid_by')
    councilors = indexes.MultiValueField()

    def get_model(self):
        return Suggestions

    def prepare_councilors(self, obj):
        return [
            (x.councilor.councilor_id, x.councilor.name, )
            for x in
            self.get_model().objects.get(uid=obj).councilors.all()
        ]
