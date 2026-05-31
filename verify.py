import re
with open('C:\\Users\\Brittany\\AppData\\Local\\Temp\\opencode\\TuFish\\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
print('Script tags:', 'OK' if '<script>' in c and '</script>' in c else 'FAIL')
for fn in ['function connectWallet', 'function toggleTheme', 'function init()', 'function renderSwarm', 'function autoTradeTick', 'function runBacktest']:
    count = len(list(re.finditer(re.escape(fn), c)))
    status = 'OK' if count == 1 else ('MISSING' if count == 0 else 'DUPLICATE x' + str(count))
    print(fn + ': ' + status)
for check, label in [('QuotaExceededError','QuotaExceeded'),('marketsLoaded','marketsLoaded'),('baseWinRate','conf-based outcome'),('swarmAnchorMarket','anchor market'),('ADAPTERS.polymarket','Poly adapter'),('ADAPTERS.crypto','Crypto adapter'),('ADAPTERS.stocks','Stocks adapter'),('ADAPTERS.solana','Solana adapter')]:
    print(label + ': ' + ('OK' if check in c else 'MISSING'))
print('Size: ' + str(len(c)) + ' chars')
