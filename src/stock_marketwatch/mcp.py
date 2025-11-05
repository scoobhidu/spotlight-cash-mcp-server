import json
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP, Context
from pydantic import Field

from config import API_HOST, _build_api_headers, DISCLAIMER, TRY_LOGIN

equity_mktwatch_mcp = FastMCP(name="Equity Marketwatch")


@equity_mktwatch_mcp.tool(
    name="stock_movers_today",
    description="Paginated tool to get the stocks in Nifty 500 that were near their 52week high or 52week low or 1day high or 1day low",
)
def stock_movers_today(
    ctx: Context,
    time_period: Annotated[Literal["1d", "52w"], Field(description="identifier to get stocks near high or low of 1day or 52week")],
    high_or_low: Annotated[Literal["high", "low"], Field(description="identifier to get stocks near high or low of specified duration")],
    page: Annotated[int, Field(description="page number to get stocks near high or low of specified duration because this is a paginated tool, increase the number only to get more stocks if any")] = 0,
) -> str:
    url = f"{API_HOST}/"

    if time_period == "1d":
        if high_or_low == "high":
            url = f"{url}1d_high?page={page}"
        else:
            url = f"{url}1d_low?page={page}"
    else:
        if high_or_low == "high":
            url = f"{url}52w_high?page={page}"
        else:
            url = f"{url}52w_low?page={page}"

    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return (
            f"Stocks that were near their {time_period} {high_or_low}:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the selected filter: {exc}\n{TRY_LOGIN}"


@equity_mktwatch_mcp.tool(
    name="stock_gainers_losers_today",
    description="Paginated tool to get the stocks in Nifty 100 that were top gainer or losers for the day",
)
def stock_gainers_losers_today(
    ctx: Context,
    gainer_or_loser: Annotated[Literal["gainers", "losers"], Field(description="identifier to get stocks that were gaining or losing")],
    page: Annotated[int, Field(description="page number to get stocks near high or low of specified duration because this is a paginated tool, increase the number only to get more stocks if any")] = 0,
) -> str:
    url = f"{API_HOST}/{gainer_or_loser}?page={page}"

    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return (
            f"{gainer_or_loser}:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the selected filter: {exc}\n{TRY_LOGIN}"


@equity_mktwatch_mcp.tool(
    name="curated_stock_filters",
    description="Paginated tool to get the stocks in Nifty 100 sorted by PE ratio in ascending manner, Return on equity in descending manner, Dividend yield in descending manner, Return on capital employed in descending manner, Debt/Equity ratio in ascending manner, Return on Net worth ratio in ascending manner, Earning per share ratio in descending manner",
)
def curated_stock_filters(
    ctx: Context,
    curated_filter: Annotated[Literal["peratio", "roe", "dividend", "roce", "zerodebt", "ronw", "eps"], Field(description="identifier of filter for PE ratio, Return on equity, Dividend yield, Return on capital employed, Debt/Equity ratio, Return on Net worth ratio, Earning per share ratio respectively")],
    page: Annotated[int, Field(description="page number to get stocks because this is a paginated tool, increase the number only to get more stocks if any")] = 0,
) -> str:
    url = f"{API_HOST}/curated/{curated_filter}?page={page}"

    headers = _build_api_headers(ctx.session_id)
    try:
        resp = requests.post(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return (
            f"Stocks arranged by {curated_filter}:\n{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
            f"{DISCLAIMER}"
        )
    except requests.RequestException as exc:
        return f"Error fetching the selected filter: {exc}\n{TRY_LOGIN}"


# @equity_mktwatch_mcp.tool(
#     name="search_nse_stocks",
#     description="Paginated tool to get the NSE stocks according to a range of Market Cap or PE Ratio or subsectors or a keyword or part of index, queries by the user",
# )
# def search_nse_stocks(
#     ctx: Context,
#     mcap_range: Annotated[tuple[int], Field(description="filter out stocks on the basis of Market Capital, the Mcap range is 0 - 2000000 crores")],
#     pe_range: Annotated[tuple[int], Field(description="filter out stocks on the basis of PE ratio, the PE Ratio range is 0 - 100")],
#     indices: Annotated[tuple[int], Field(description='''{
#         "1": "Nifty 50",
#         "3": "Nifty Bank",
#         "6": "Nifty Next 50",
#         "8": "Nifty 100",
#         "11": "Nifty Midcap 50",
#         "12": "Nifty Smlcap 100",
#         "19": "Nifty 200",
#         "20": "Nifty 500",
#         "21": "Nifty Midcap 100",
#         "23": "Nifty Smlcap 250"
#         "2": "S&P Bse Sensex",
#         "42": "S&P Bse 100",
#         "43": "S&P Bse 200",
#         "44": "S&P Bse 500",
#         "60": "S&P Bse Bharat 22 Index"
#     }
#     use any of the following key to get the corresponding stocks that are constituents of that index.
#     ''')],
#     subsectors: Annotated[tuple[int], Field(description='''
#     {
#         "111": "Abrasives"
#         "42": "Sugar",
#         "51": "Solvent  Extraction",
#         "69": "Floriculture",
#         "78": "Rubber  Products",
#         "89": "Agriculture",
#         "91": "Aquaculture",
#         "119": "Tea/Coffee"
#         "142": "Airport Management Services"
#         "60": "Breweries & Distilleries"
#         "141": "Animal Feed"
#         "3": "Bearings",
#         "7": "Automobile Two & Three Wheelers",
#         "16": "Fasteners",
#         "20": "Automobiles - Dealers & Distributors",
#         "25": "Diesel Engines",
#         "27": "Tyres & Allied",
#         "30": "Batteries",
#         "32": "Railways Wagons",
#         "33": "Automobiles - Passenger Cars",
#         "38": "Automobiles-Tractors",
#         "45": "Castings/Forgings",
#         "52": "Lubricants",
#         "59": "Cycles",
#         "75": "Automobiles-Trucks/Lcv",
#         "102": "Forgings",
#         "106": "Auto Ancillary"
#         "81": "Airlines"
#         "4": "Bank - Private",
#         "24": "Bank - Public"
#         "136": "Business Support"
#         "11": "Electrodes & Welding Equipment",
#         "14": "Refractories",
#         "26": "Defence",
#         "61": "Engineering - Industrial Equipments",
#         "88": "Electric Equipment",
#         "96": "Compressors / Pumps",
#         "108": "Engineering"
#         "5": "Carbon Black",
#         "9": "Dyes & Pigments",
#         "62": "Paints",
#         "70": "Pesticides & Agrochemicals",
#         "90": "Chemicals",
#         "117": "Fertilizers"
#         "18": "Cement & Construction Materials",
#         "76": "Laminates/Decoratives",
#         "92": "Wood & Wood Products",
#         "103": "Ceramics/Marble/Granite/Sanitaryware",
#         "118": "Glass"
#         "131": "Construction Vehicles"
#         "56": "Air Conditioners",
#         "64": "Consumer Durables - Electronics",
#         "83": "Watches & Accessories",
#         "98": "IT - Hardware",
#         "114": "Consumer Durables - Domestic Appliances"
#         "2": "Petrochemicals",
#         "19": "Refineries",
#         "48": "Oil Exploration"
#         "140": "Depository Services"
#         "35": "Diamond  &  Jewellery"
#         "100": "Diversified"
#         "54": "Educational Institutions"
#         "39": "Cable",
#         "44": "Electronics - Components"
#         "135": "Environmental Services"
#         "77": "ETF"
#         "104": "Ferro & Silica Manganese"
#         "123": "Finance - Asset Management",
#         "124": "Finance - Investment",
#         "125": "Finance - NBFC",
#         "126": "Finance Term Lending",
#         "127": "Finance - Housing",
#         "128": "Finance - Stock Broking",
#         "129": "Finance - Others"
#         "6": "Detergents & Soaps",
#         "8": "Edible Oil",
#         "29": "Packaging",
#         "50": "Consumer Food",
#         "53": "Printing & Stationery",
#         "66": "Household & Personal Products",
#         "82": "Leather",
#         "85": "Cigarettes/Tobacco",
#         "95": "Footwear"
#         "12": "Gas Transmission/Marketing"
#         "113": "G-Sec"
#         "10": "Pharmaceuticals & Drugs",
#         "23": "Hospital & Healthcare Services",
#         "65": "Medical Equipment/Supplies/Accessories"
#         "40": "Hotel, Resort & Restaurants",
#         "107": "Amusement Parks/Recreation/Club",
#         "115": "Travel Services"
#         "41": "Industrial  Gases & Fuels"
#         "15": "Transmission Towers / Equipments",
#         "47": "Engineering - Construction"
#         "21": "Insurance"
#         "68": "Steel/Sponge Iron/Pig Iron",
#         "74": "Metal - Ferrous",
#         "79": "Steel & Iron Products"
#         "17": "Animation",
#         "36": "IT - Education",
#         "46": "BPO/ITeS",
#         "49": "IT - Software",
#         "63": "IT - Networking",
#         "130": "Fintech"
#         "72": "Courier  Services",
#         "73": "Port",
#         "116": "Logistics",
#         "121": "Shipping"
#         "80": "Printing And Publishing",
#         "94": "Film Production, Distribution & Entertainment",
#         "122": "TV Broadcasting & Software Production"
#         "58": "Mining & Minerals"
#         "57": "Miscellaneous"
#         "37": "Aluminium & Aluminium Products",
#         "43": "Metal - Non Ferrous"
#         "99": "Unspecified",
#         "105": "Cash and Cash Equivalents",
#         "109": "Other",
#         "120": "Index"
#         "28": "Paper & Paper Products"
#         "101": "Photographic Products"
#         "55": "Plastic Products"
#         "31": "Power Generation/Distribution"
#         "137": "Professional Services"
#         "84": "Ratings"
#         "97": "Construction - Real Estate"
#         "132": "Restaurants"
#         "22": "Retailing",
#         "112": "e-Commerce"
#         "110": "Ship Building"
#         "34": "Telecommunication - Equipment",
#         "86": "Telecommunication - Service  Provider"
#         "138": "Telecom-Infrastructure"
#         "1": "Textile - Weaving",
#         "13": "Textile - Spinning",
#         "67": "Textile - Machinery",
#         "71": "Textile - Manmade  Fibres",
#         "93": "Textile"
#         "87": "Trading"
#     }
#     use any of the following keys to get the corresponding stocks that are part of that subsector industry
#     ''')],
#     searchkey: Annotated[str, Field(description="search key to filter stocks by name")] = "",
#     page: Annotated[int, Field(description="page number to get stocks near high or low of specified duration because this is a paginated tool, increase the number only to get more stocks if any")] = 0,
# ) -> str:
#     url = f"{API_HOST}/filter/stocks/nse"
#
#     payload = {
#       "page": page,
#       "size": 10,
#       "indices": indices,
#       "subsector": subsectors,
#       "mcap_range": mcap_range,
#       "pe_range": pe_range,
#       "sortby": "DESC",
#       "filterby": "ltp",
#       "searchkey": searchkey
#     }
#
#     headers = _build_api_headers(ctx.session_id)
#     try:
#         resp = requests.post(url, headers=headers, timeout=30, data=json.dumps(payload))
#         resp.raise_for_status()
#         return (
#             f"{json.dumps(resp.json(), indent=2, ensure_ascii=False)}"
#             f"{DISCLAIMER}"
#         )
#     except requests.RequestException as exc:
#         return f"Error fetching the selected filter: {exc}"