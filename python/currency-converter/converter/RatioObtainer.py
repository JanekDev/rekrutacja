import json, datetime, urllib.request

url = 'https://api.exchangerate.host/latest'
now = datetime.datetime.now().strftime('%Y-%m-%d')

class RatioObtainer:
    base = None
    target = None

    def __init__(self, base, target):
        self.base = base
        self.target = target

    def was_ratio_saved_today(self):
        # TODO
        # This function checks if given ratio was saved today and if the file with ratios is created at all
        # should return false when file doesn't exist or if there's no today's exchange rate for given values at all
        # should return true otherwise
        try:
            with open('ratios.json', 'r') as f:
                data = json.load(f)
                if [record for record in data if record['date_fetched'] == now and record['base_currency'] == self.base and record['target_currency'] == self.target]:
                    return True
                return False
        except:
            return False

    def fetch_ratio(self):
        # TODO
        # This function calls API for today's exchange ratio
        # Should ask API for today's exchange ratio with given base and target currency
        # and call save_ratio method to save it
        response = urllib.request.urlopen(f'{url}?base={self.base}&symbols={self.target}')
        data = json.loads(response.read())
        self.save_ratio(data['rates'][self.target])

    def save_ratio(self, ratio):
        data = []
        record = {
            'base_currency': self.base, 
            'target_currency': self.target,
            'date_fetched': now,
            'ratio': ratio
        }
                
        with open('ratios.json', 'r') as f:
            data = [i for i in json.load(f) if i['base_currency'] != self.base or i['target_currency'] != self.target]
        data.append(record)
        with open('ratios.json', 'w') as f:
            json.dump(data, f, indent=2)

    def get_matched_ratio_value(self):
        # TODO
        # Should read file and receive exchange rate for given base and target currency from that file
        with open('ratios.json', 'r') as f:
            data = json.load(f)
        return float([record for record in data if record['base_currency'] == self.base and record['target_currency'] == self.target][0]['ratio'])
