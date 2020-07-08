def bytes_per_symbol(symbols):
    prefix = {}
    for index, symbol in enumerate(symbols):
        prefix[symbol] = 1 << (index + 1) * 10
    
    return prefix

def bytes_to_human(bts):
    response = {
        "bytes": bts
    }

    symbols = ('K', 'M', 'G', 'T')
    prefix = bytes_per_symbol(symbols)
    for symbol in reversed(symbols):
        if bts >= prefix[symbol]:
            value = float(bts) / prefix[symbol]
            
            return {
                **response,
                "human": {
                    "format": symbol,
                    "value": float('{:.1f}'.format(value))
                }
            }
    
    return response