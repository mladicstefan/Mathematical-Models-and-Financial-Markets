from data import DataFetcher

df = DataFetcher(is_stock=True)
params = df.input()
data = df.fetch_data(params)
