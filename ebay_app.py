from flask import Flask, render_template, request, jsonify
import threading
import time
from datetime import datetime
import requests
import re
import json
import sys

# Устанавливаем UTF-8 кодировку
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

class EbayMonitorWeb:
    def __init__(self):
        self.is_running = False
        self.found_auctions = set()
        self.logs = []
        self.auctions = []
        self.monitor_thread = None

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        if len(self.logs) > 100:
            self.logs.pop(0)

    def add_auction(self, title, price, bids, url):
        auction = {
            'title': title,
            'price': price,
            'bids': bids,
            'url': url,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        self.auctions.insert(0, auction)
        if len(self.auctions) > 50:
            self.auctions.pop()

    def start_monitoring(self, api_key, dev_id, cert_id, keywords, min_price, max_price, min_bids, interval):
        if self.is_running:
            return False

        if not api_key or not dev_id or not cert_id:
            self.log("❌ Ошибка: Введи все API ключи!")
            return False

        self.is_running = True
        self.logs = []
        self.auctions = []

        self.log("="*80)
        self.log("🚀 МОНИТОРИНГ ЗАПУЩЕН")
        self.log("="*80)

        if keywords:
            self.log(f"🔍 Ключевые слова: {keywords}")
        else:
            self.log(f"🔍 Поиск: ВСЕ аукционы")

        self.log(f"💰 Цена: ${min_price} - ${max_price}")
        self.log(f"📊 Минимум ставок: {min_bids}")
        self.log(f"⏱️  Интервал: {interval} сек")
        self.log("="*80 + "\n")

        self.monitor_thread = threading.Thread(
            target=self.monitor_loop,
            args=(api_key, dev_id, cert_id, keywords, min_price, max_price, min_bids, interval),
            daemon=True
        )
        self.monitor_thread.start()
        return True

    def stop_monitoring(self):
        self.is_running = False
        self.log("\n⏹️  Мониторинг остановлен.\n")

    def monitor_loop(self, api_key, dev_id, cert_id, keywords, min_price, max_price, min_bids, interval):
        while self.is_running:
            try:
                if keywords:
                    for keyword in keywords.split(','):
                        if not self.is_running:
                            break
                        self.search_ebay(api_key, dev_id, cert_id, keyword.strip(), min_price, max_price, min_bids)
                        time.sleep(2)
                else:
                    self.search_ebay(api_key, dev_id, cert_id, '', min_price, max_price, min_bids)

                self.log(f"⏳ Следующая проверка через {interval} сек...\n")
                time.sleep(interval)
            except Exception as e:
                self.log(f"❌ Ошибка: {str(e)}")
                time.sleep(5)

    def search_ebay(self, api_key, dev_id, cert_id, keyword, min_price, max_price, min_bids):
        try:
            if keyword:
                self.log(f"🔍 Поиск: '{keyword}'...")
            else:
                self.log(f"🔍 Поиск: ВСЕ аукционы...")

            url = "http://svcs.ebay.com/services/search/FindingService/v1"

            params = {
                'OPERATION-NAME': 'findItemsByKeywords' if keyword else 'findItemsAdvanced',
                'SERVICE-VERSION': '1.0.0',
                'SECURITY-APPNAME': api_key,
                'RESPONSE-DATA-FORMAT': 'JSON',
                'REST-PAYLOAD': 'true',
                'keywords': keyword if keyword else '',
                'itemFilter(0).name': 'ListingType',
                'itemFilter(0).value': 'AuctionWithBIN',
                'itemFilter(1).name': 'MinPrice',
                'itemFilter(1).value': str(min_price),
                'itemFilter(2).name': 'MaxPrice',
                'itemFilter(2).value': str(max_price),
                'sortOrder': 'EndTimeSoonest',
                'paginationInput.entriesPerPage': '100',
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'findItemsByKeywordsResponse' in data:
                items = data['findItemsByKeywordsResponse'][0].get('searchResult', [{}])[0].get('item', [])
            elif 'findItemsAdvancedResponse' in data:
                items = data['findItemsAdvancedResponse'][0].get('searchResult', [{}])[0].get('item', [])
            else:
                self.log(f"   ⚠️ Результаты не найдены")
                return

            if not items:
                self.log(f"   ⚠️ Результаты не найдены")
                return

            self.log(f"   ✓ Найдено {len(items)} аукционов")
            found_count = 0

            for item in items:
                try:
                    title = item.get('title', [''])[0]
                    price = float(item.get('sellingStatus', [{}])[0].get('currentPrice', [{'__value__': 0}])[0].get('__value__', 0))
                    bids = int(item.get('sellingStatus', [{}])[0].get('bidCount', [0])[0])
                    url = item.get('viewItemURL', [''])[0]
                    item_id = item.get('itemId', [''])[0]

                    if price >= min_price and price <= max_price and bids >= min_bids:
                        auction_id = f"{title}_{item_id}"
                        if auction_id not in self.found_auctions:
                            self.found_auctions.add(auction_id)
                            self.log(f"✅ НАЙДЕН: {title[:60]}... | ${price} | Ставок: {bids}")
                            self.add_auction(title, f"${price}", bids, url)
                            found_count += 1

                except Exception as e:
                    continue

            if found_count == 0:
                self.log(f"   Подходящих аукционов не найдено")

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Ошибка API: {str(e)}")
        except Exception as e:
            self.log(f"❌ Ошибка: {str(e)}")

monitor = EbayMonitorWeb()

@app.route('/')
def index():
    response = render_template('ebay.html')
    response = app.make_response(response)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/api/start', methods=['POST'])
def start():
    data = request.json
    api_key = data.get('api_key', '')
    dev_id = data.get('dev_id', '')
    cert_id = data.get('cert_id', '')
    keywords = data.get('keywords', '')
    min_price = float(data.get('min_price', 0))
    max_price = float(data.get('max_price', 999999))
    min_bids = int(data.get('min_bids', 1))
    interval = int(data.get('interval', 60))

    success = monitor.start_monitoring(api_key, dev_id, cert_id, keywords, min_price, max_price, min_bids, interval)
    return jsonify({'success': success})

@app.route('/api/stop', methods=['POST'])
def stop():
    monitor.stop_monitoring()
    return jsonify({'success': True})

@app.route('/api/status')
def status():
    return jsonify({
        'running': monitor.is_running,
        'logs': monitor.logs[-20:],
        'auctions': monitor.auctions[:10]
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
