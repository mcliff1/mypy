# -*- coding: utf-8 -*-
"""
From youtube series

https://www.youtube.com/watch?v=tKdWpiSZO8M&list=PL1A2CSdiySGIPxpSlgzsZiWDavYTAx61d&index=2
templating
"""

from string import Template


class MyTemplate(Template):
    """
    modifies the base Template class
    """
    delimiter = '#'  # from $



def main():
    cart = []
    cart.append(dict(item='Coke', price=8, qty=2))
    cart.append(dict(item='Cake', price=12, qty=1))
    cart.append(dict(item='Fish', price=9, qty=3))

    #t = Template('$qty x $item = $price')
    t = MyTemplate('#qty x #item = #price')

    total = 0
    print("Cart:")
    for data in cart:
        print(t.substitute(data))
        total += data['price']

    print('Total:' + str(total))

if __name__ == '__main__':
    main()
