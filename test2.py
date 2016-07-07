



def main():
    
    company_list = open('companylist.csv')

    the_stocks = []
    for line in company_list:
        # Skip the first header line.
        print(line.find("Symbol"))
        if(line.find("Symbol") != -1): pass
        else:
            stock_symbol_list = line.split(',')
            the_stocks.append(stock_symbol_list[0].strip('"'))
        

    for k in the_stocks: print(k)

if __name__ == "__main__": main()