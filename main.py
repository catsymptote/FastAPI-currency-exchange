import json
from fastapi import FastAPI


app = FastAPI()


# Load data
with open('data.json', 'r') as file:
    text = file.read()
    data = json.loads(text)
# print(data['rates']['NOK'])


def get_rate_from_data(currency: str):
    '''Support function.'''
    if currency.upper() in data['rates']:
        return data['rates'][currency]
    return None


@app.get("/")
async def get_info():
    '''Return info.'''
    return {'Endpoint': 'Description',
        '/': 'Get info on how to use.',
        '/all': 'List all internal data, including all rates.',
        '/rate/c': 'Get the currency-to-USD ratio. (c = currency code.)',
        '/convert/c1,c2,amount': 'Convert the amount of c1 into c2.'
    }


@app.get("/all")
async def get_all():
    '''Return all data.'''
    return data


@app.get("/rate/{currency}")
async def get_rate(currency: str):
    '''Return the currency rate.'''
    # Because USD doesn't work for some reason?
    rate = get_rate_from_data(currency)

    # Construct and return message.
    if rate is not None:
        message = {'currency': currency, 'rate': rate}
    else:
        message = {'error': 'Did not work. Probably non-existent currency.'}
    return message


@app.get("/convert/{currency1},{currency2},{amount}")
async def convert_currency(currency1: str, currency2: str, amount: int):
    '''Convert between currencies.'''
    rate1 = get_rate_from_data(currency1)
    rate2 = get_rate_from_data(currency2)
    in_usd = amount / rate1
    in_currency2 = in_usd * rate2
    return {'money': in_currency2}


if __name__ == '__main__':
    import subprocess
    subprocess.run(["hypercorn", "main:app", "--reload"])
