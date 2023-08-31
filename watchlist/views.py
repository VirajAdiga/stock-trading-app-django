from threading import Thread
from queue import Queue

from django.shortcuts import render
from yahoo_fin.stock_info import *


def stock_picker(request):
    nifty_stocks = tickers_nifty50()
    return render(request, "watchlist/stock_picker.html", {'nifty_stocks': nifty_stocks})


def stock_tracker(request):
    stock_list = request.GET.getlist("stock_list")
    stock_data = []
    threads = []
    que = Queue()

    def add_stock_details_to_queue(stock_name):
        que.put({stock: get_quote_table(stock_name)})

    for stock in stock_list:
        thread = Thread(target=add_stock_details_to_queue(stock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not que.empty():
        stock_data.append(que.get())

    return render(request, "watchlist/stock_tracker.html", {"stock_data": stock_data})
