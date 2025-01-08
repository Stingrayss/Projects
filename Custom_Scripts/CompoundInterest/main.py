def calculateCompoundInterest(years=1):
    balance = 0
    interestBalance = 0
    returnPercent = .1
    
    baseSalary = 75000
    salaryRaise = 1.03
    
    stringCenter = 30
    for year in range(years):
        print(f"{'#'*stringCenter}")
        print(f"Year {year + 1}".center(stringCenter))
        print(f"Current Balance: {balance}".center(stringCenter))
        print(f"Current Salary: {int(baseSalary)}".center(stringCenter))
        amountDeposited = int((baseSalary * (2/3)))
        balance += amountDeposited
        print(f"{'='*stringCenter}")
        print(f"Amount Deposited: {amountDeposited}".center(stringCenter))
        yearInterest = int(balance * returnPercent)
        interestBalance += yearInterest
        balance += yearInterest
        print(f"       Interest: {yearInterest}".center(stringCenter))
        print(f" +{'-'*(stringCenter - 3)}")
        print(f"     New Balance: {balance}".center(stringCenter))
        print(f"  Total Interest: {interestBalance}".center(stringCenter))
        
        baseSalary *= salaryRaise
    
    
calculateCompoundInterest(20)