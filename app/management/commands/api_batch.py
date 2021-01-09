from django.core.management.base import BaseCommand
import sys
sys.path.append('.../')
from ...services.api_service import *

class Command(BaseCommand):
    help = 'yhoofinance-APIを実行します。引数に１だったら企業の基本情報を取得します。引数が2であれば、企業の現在の株価情報などを取得します'

    def add_arguments(self, parser):
        parser.add_argument(
	        "--num",
	        type=int,
	        dest="num",
	        default=1,
            help='企業情報か株価かどちらのバッチ処理ですか？'
	    )

    def handle(self, *args, **options):
        try:
            num = options['num']
            api = exec_api()
            
            if (num == 1):
                api.exec_basic_info_api()

            if (num == 2):
                api.exec_daily_price_api()
            
        except Exception as e:
            print(e)

