from django.shortcuts import render


def stock_picker(request):
    return render(request, "watchlist/stock_picker.html")
