from vectorbtpro import Portfolio, settings

# settings["plotting"]["layout"]["paper_bgcolor"] = "rgb(0,0,0)"
# settings["plotting"]["layout"]["plot_bgcolor"] = "rgb(0,0,0)"


def plot_results(portfolio):
    portfolio.plot().show()
