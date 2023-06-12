import gc

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import pandas as pd
import concurrent.futures
import yfinance as yf

from multiprocessing import Pool

PATH = "D:\chromedriver\chromedriver.exe"
tickers = []


def create_folders():
    print("_____________________Start Creating Folders____________________")

    for index, ticker in df["Ticker"].iteritems():
        ticker = str(ticker)
        if "*" in ticker:
            continue

        if not os.path.exists("./Data/" + ticker):
            os.makedirs("./Data/" + ticker)
            print(f"Folder '{ticker}' created successfully.")
        else:
            # os.rmdir(ticker)
            print(f"Folder '{ticker}' already exists.")

    print("_____________________End Folders Creation____________________")


def delete_ticker_folder(ticker):
    if not os.path.exists("./Data/" + ticker):
        print(f"Folder '{ticker}' not exists.")
    else:
        os.rmdir("./Data/" + ticker)
        print(f"N---'{ticker}'!!!")


def get_financial_statements_by_ticker(ticker):
    if "*" in ticker:
        return

    service = Service(executable_path=PATH)
    driver = webdriver.Chrome(service=service)

    df_fs_moomoo = pd.DataFrame(columns=[
    'Total revenue', 'Cost of revenue', 'Gross profit', 'Operating expense',
    'Operating profit', 'Net non-operating interest income expense',
    'Other net income (expense)', 'Income before tax', 'Income tax',
    'Net income', 'Minority interest income',
    'Net income attributable to the parent company', 'Preferred stock dividends',
    'Other preferred stock dividends',
    'Net income attributable to common stockholders',
    'Basic earnings per share', 'Diluted earnings per share',
    'Dividend per share'
])
    ticker = str(ticker)

    driver.get(f"https://www.moomoo.com/stock/{ticker}-US/financial-statement")
    driver.implicitly_wait(2)

    try:
        period_type_selector = driver.find_element(By.CSS_SELECTOR, ".select-compoent.select-period.en-us-select")
    except:
        return

    period_type_selector.click()
    annual_choice = driver.find_element(By.CSS_SELECTOR,
                                        "div[class='select-compoent select-period active en-us-select'] div:nth-child(2)")
    annual_choice.click()

    while (True):
        time = []
        raw_diluted_earnings_per_share = ""
        raw_dividend_per_share = ""

        for i in range(2, 6):
            try:
                item = driver.find_element(By.CSS_SELECTOR, f"div[class='date-title'] span:nth-child({i})")
                time.append(item.text)
            except:
                continue

        try:
            raw_total_revenue = driver.find_element(By.CSS_SELECTOR, 'span[title="Total revenue"] + div.value').text
            raw_cost_of_revenue = driver.find_element(By.CSS_SELECTOR, 'span[title="Cost of revenue"] + div.value').text
            raw_gross_profit = driver.find_element(By.CSS_SELECTOR, 'span[title="Gross profit"] + div.value').text
            raw_operating_expense = driver.find_element(By.CSS_SELECTOR,
                                                        'span[title="Operating expense"] + div.value').text
            raw_operating_profit = driver.find_element(By.CSS_SELECTOR,
                                                       'span[title="Operating profit"] + div.value').text
            raw_net_non_operating_interest_income_expense = driver.find_element(By.CSS_SELECTOR,
                                                                                'span[title="Net non-operating interest income expense"] + div.value').text
            raw_other_net_income_expense = driver.find_element(By.CSS_SELECTOR,
                                                               'span[title="Other net income (expense)"] + div.value').text
            raw_income_before_tax = driver.find_element(By.CSS_SELECTOR,
                                                        'span[title="Income before tax"] + div.value').text
            raw_income_tax = driver.find_element(By.CSS_SELECTOR, 'span[title="Income tax"] + div.value').text
            raw_net_income = driver.find_element(By.CSS_SELECTOR, 'span[title="Net income"] + div.value').text
            raw_minority_interest_income = driver.find_element(By.CSS_SELECTOR,
                                                               'span[title="Minority interest income"] + div.value').text
            raw_net_income_attributable_to_parent_company = driver.find_element(By.CSS_SELECTOR,
                                                                                'span[title="Net income attributable to the parent company"] + div.value').text
            raw_preferred_stock_dividends = driver.find_element(By.CSS_SELECTOR,
                                                                'span[title="Preferred stock dividends"] + div.value').text
            raw_other_preferred_stock_dividends = driver.find_element(By.CSS_SELECTOR,
                                                                      'span[title="Other preferred stock dividends"] + div.value').text
            raw_net_income_attributable_to_common_stockholders = driver.find_element(By.CSS_SELECTOR,
                                                                                     'span[title="Net income attributable to common stockholders"] + div.value').text
            raw_basic_earnings_per_share = driver.find_element(By.CSS_SELECTOR,
                                                               'span[title="Basic earnings per share"] + div.value').text
            raw_diluted_earnings_per_share = driver.find_element(By.CSS_SELECTOR,
                                                                 'span[title="Diluted earnings per share"] + div.value').text
            raw_dividend_per_share = driver.find_element(By.CSS_SELECTOR,
                                                         'span[title="Dividend per share"] + div.value').text

        except:
            break

        total_revenue = []
        cost_of_revenue = []
        gross_profit = []
        operating_expense = []
        operating_profit = []
        net_non_operating_interest_income_expense = []
        other_net_income_expense = []
        income_before_tax = []
        income_tax = []
        net_income = []
        minority_interest_income = []
        net_income_attributable_to_parent_company = []
        preferred_stock_dividends = []
        other_preferred_stock_dividends = []
        net_income_attributable_to_common_stockholders = []
        basic_earnings_per_share = []
        diluted_earnings_per_share = []
        dividend_per_share = []

        for num in range(1, len(time) + 1):

            try:
                total_revenue_value = driver.find_element(
                    By.CSS_SELECTOR, f'span[title="Total revenue"]:nth-child({num}) + div.value').text

                if total_revenue_value is None or str(total_revenue_value) == "" or str(
                        total_revenue_value) == " ":
                    total_revenue.append("")
                else:
                    total_revenue.append(total_revenue_value)
            except:
                total_revenue.append("")

            try:
                cost_of_revenue_value = driver.find_element(
                    By.CSS_SELECTOR, f'span[title="Cost of revenue"]:nth-child({num}) + div.value').text
                if cost_of_revenue_value is None or str(cost_of_revenue_value) == "" or str(
                        cost_of_revenue_value) == " ":
                    cost_of_revenue.append("")
                else:
                    cost_of_revenue.append(cost_of_revenue_value)
            except:
                cost_of_revenue.append("")

            try:
                gross_profit_value = driver.find_element(
                    By.CSS_SELECTOR, f'span[title="Gross profit"]:nth-child({num}) + div.value').text
                if gross_profit_value is None or str(gross_profit_value) == "" or str(
                        gross_profit_value) == " ":
                    gross_profit.append("")
                else:
                    gross_profit.append(gross_profit_value)
            except:
                gross_profit.append("")

            try:
                operating_expense_value = raw_operating_expense.find_element(By.CSS_SELECTOR,
                                                                             f'span:nth-child({num}) > span:nth-child(2)').text
                if operating_expense_value is None or str(operating_expense_value) == "" or str(
                        operating_expense_value) == " ":
                    operating_expense.append("")
                else:
                    operating_expense.append(operating_expense_value)
            except:
                operating_expense.append("")

            try:
                operating_profit_value = raw_operating_profit.find_element(By.CSS_SELECTOR,
                                                                           f'span:nth-child({num}) > span:nth-child(2)').text
                if operating_profit_value is None or str(operating_profit_value) == "" or str(
                        operating_profit_value) == " ":
                    operating_profit.append("")
                else:
                    operating_profit.append(operating_profit_value)
            except:
                operating_profit.append("")

            try:
                net_non_operating_interest_income_expense_value = raw_net_non_operating_interest_income_expense.find_element(
                    By.CSS_SELECTOR,
                    f'span:nth-child({num}) > span:nth-child(2)').text
                if net_non_operating_interest_income_expense_value is None or str(
                        net_non_operating_interest_income_expense_value) == "" or str(
                        net_non_operating_interest_income_expense_value) == " ":
                    net_non_operating_interest_income_expense.append("")
                else:
                    net_non_operating_interest_income_expense.append(net_non_operating_interest_income_expense_value)
            except:
                net_non_operating_interest_income_expense.append("")

            try:
                other_net_income_expense_value = raw_other_net_income_expense.find_element(By.CSS_SELECTOR,
                                                                                           f'span:nth-child({num}) > span:nth-child(2)').text
                if other_net_income_expense_value is None or str(other_net_income_expense_value) == "" or str(
                        other_net_income_expense_value) == " ":
                    other_net_income_expense.append("")
                else:
                    other_net_income_expense.append(other_net_income_expense_value)
            except:
                other_net_income_expense.append("")

            try:
                income_before_tax_value = raw_income_before_tax.find_element(By.CSS_SELECTOR,
                                                                             f'span:nth-child({num}) > span:nth-child(2)').text
                if income_before_tax_value is None or str(income_before_tax_value) == "" or str(
                        income_before_tax_value) == " ":
                    income_before_tax.append("")
                else:
                    income_before_tax.append(income_before_tax_value)
            except:
                income_before_tax.append("")

            try:
                income_tax_value = raw_income_tax.find_element(By.CSS_SELECTOR,
                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if income_tax_value is None or str(income_tax_value) == "" or str(
                        income_tax_value) == " ":
                    income_tax.append("")
                else:
                    income_tax.append(income_tax_value)
            except:
                income_tax.append("")

            try:
                net_income_value = raw_net_income(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if net_income_value is None or str(net_income_value) == "" or str(
                        net_income_value) == " ":
                    net_income.append("")
                else:
                    net_income.append(net_income_value)
            except:
                net_income.append("")

            try:
                minority_interest_income_value = raw_minority_interest_income.find_element(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if minority_interest_income_value is None or str(minority_interest_income_value) == "" or str(
                        minority_interest_income_value) == " ":
                    minority_interest_income.append("")
                else:
                    minority_interest_income.append(minority_interest_income_value)
            except:
                minority_interest_income.append("")

            try:
                net_income_attributable_to_parent_company_value = raw_net_income_attributable_to_parent_company.find_element(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if net_income_attributable_to_parent_company_value is None or str(net_income_attributable_to_parent_company_value) == "" or str(
                        net_income_attributable_to_parent_company_value) == " ":
                    net_income_attributable_to_parent_company.append("")
                else:
                    net_income_attributable_to_parent_company.append(net_income_attributable_to_parent_company_value)
            except:
                net_income_attributable_to_parent_company.append("")

            try:
                preferred_stock_dividends_value = raw_preferred_stock_dividends.find_element(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if preferred_stock_dividends_value is None or str(preferred_stock_dividends_value) == "" or str(
                        preferred_stock_dividends_value) == " ":
                    preferred_stock_dividends.append("")
                else:
                    preferred_stock_dividends.append(preferred_stock_dividends_value)
            except:
                preferred_stock_dividends.append("")

            try:
                other_preferred_stock_dividends_value = raw_other_preferred_stock_dividends.find_element(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if other_preferred_stock_dividends_value is None or str(other_preferred_stock_dividends_value) == "" or str(
                        other_preferred_stock_dividends_value) == " ":
                    other_preferred_stock_dividends.append("")
                else:
                    other_preferred_stock_dividends.append(other_preferred_stock_dividends_value)
            except:
                other_preferred_stock_dividends.append("")

            try:
                net_income_attributable_to_common_stockholders_value = raw_net_income_attributable_to_common_stockholders.find_element(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if net_income_attributable_to_common_stockholders_value is None or str(net_income_attributable_to_common_stockholders_value) == "" or str(
                        net_income_attributable_to_common_stockholders_value) == " ":
                    net_income_attributable_to_common_stockholders.append("")
                else:
                    net_income_attributable_to_common_stockholders.append(net_income_attributable_to_common_stockholders_value)
            except:
                net_income_attributable_to_common_stockholders.append("")

            try:
                basic_earnings_per_share_value = raw_basic_earnings_per_share.find_element(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if basic_earnings_per_share_value is None or str(basic_earnings_per_share_value) == "" or str(
                        dividend_per_share_value) == " ":
                    basic_earnings_per_share.append("")
                else:
                    basic_earnings_per_share.append(basic_earnings_per_share_value)
            except:
                basic_earnings_per_share.append("")

            try:
                diluted_earnings_per_share_value = raw_diluted_earnings_per_share.find_element(By.CSS_SELECTOR,
                                                                                               f'span:nth-child({num}) > span:nth-child(2)').text

                if diluted_earnings_per_share_value is None or str(diluted_earnings_per_share_value) == "" or str(
                        diluted_earnings_per_share_value) == " ":
                    diluted_earnings_per_share.append("")
                else:
                    diluted_earnings_per_share.append(diluted_earnings_per_share_value)
            except:
                diluted_earnings_per_share.append("")

            try:
                dividend_per_share_value = raw_dividend_per_share.find_element(By.CSS_SELECTOR,
                                                                               f'span:nth-child({num}) > span:nth-child(2)').text
                if dividend_per_share_value is None or str(dividend_per_share_value) == "" or str(
                        dividend_per_share_value) == " ":
                    dividend_per_share.append("")
                else:
                    dividend_per_share.append(dividend_per_share_value)
            except:
                dividend_per_share.append("")


        temp_df = pd.DataFrame({
            'Time': time,
            'Total revenue': total_revenue,
            'Cost of revenue': cost_of_revenue,
            'Gross profit': gross_profit,
            'Operating expense': operating_expense,
            'Operating profit': operating_profit,
            'Net non-operating interest income expense': net_non_operating_interest_income_expense,
            'Other net income (expense)': other_net_income_expense,
            'Income before tax': income_before_tax,
            'Income tax': income_tax,
            'Net income': net_income,
            'Minority interest income': minority_interest_income,
            'Net income attributable to the parent company': net_income_attributable_to_parent_company,
            'Preferred stock dividends': preferred_stock_dividends,
            'Other preferred stock dividends': other_preferred_stock_dividends,
            'Net income attributable to common stockholders': net_income_attributable_to_common_stockholders,
            'Basic earnings per share': basic_earnings_per_share,
            'Diluted earnings per share': diluted_earnings_per_share,
            'Dividend per share': dividend_per_share
        })
        # print(temp_df)
        df_fs_moomoo = df_fs_moomoo.append(temp_df, ignore_index=True)
        # print(df_fs_moomoo)

        try:
            next = driver.find_element(By.CSS_SELECTOR, "span[class='right']")
            if "disabled" not in next.get_attribute("class"):
                # print("The element does not have the class 'disabled'.")
                next.click()

        except:
            # print("The element has the class 'disabled'.")
            break

    if len(df_fs_moomoo) > 5:

        folder_path = "./Data/" + ticker

        # check if folder exists
        if not os.path.exists(folder_path):
            # create folder if it doesn't exist
            os.makedirs(folder_path)

        df_fs_moomoo.to_csv(folder_path + f'/{ticker}_moomoo.csv')
        print(f"Y---{ticker}---{len(df_fs_moomoo)}")

        if len(df_fs_moomoo) == 6:
            gc.collect()

    else:
        delete_ticker_folder(ticker)
    driver.quit()



def get_financial_statements():
    pool = Pool(8)
    pool.map(get_financial_statements_by_ticker, tickers)
    pool.close()
    pool.join()


if __name__ == '__main__':
    df = pd.read_csv("US stock tickers.csv")
    tickers = df["Ticker"].tolist()

    tickers = [str(t).replace("*", "") for t in tickers if t]

    d_tickers = []

    with open("output_file.txt", "r") as input_file:
        d_tickers = [str(line.replace("\n", "")) for line in input_file.readlines()]

    print("D_tickers: ",d_tickers)

    tickers = [x for x in tickers if (x not in set(d_tickers)) and (x != "nan")]

    print("tickers: ",tickers)

    # create_folders()
    #get_financial_statements()
