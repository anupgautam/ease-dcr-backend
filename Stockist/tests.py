from django.test import TestCase
from model_bakery import baker
from p
import pytest

class TestStockistModel(TestCase):

    @pytest.fixture
    def setUp(self):
        self.stockist = baker.make('DCR.Stockist', _quantity=10000)
        p
