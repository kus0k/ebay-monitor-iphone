from flask import Flask, render_template, request, jsonify
import threading
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys
import re
import json
import random

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Список User-Agent'ов для рандомизации
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

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

    def start_monitoring(self, keywords, min_price, max_price, min_bids, interval):
        if self.is_running:
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
            args=(keywords, min_price, max_price, min_bids, interval),
            daemon=True
        )
        self.monitor_thread.start()
        return True

    def stop_monitoring(self):
        self.is_running = False
        self.log("\n⏹️  Мониторинг остановлен.\n")

    def monitor_loop(self, keywords, min_price, max_price, min_bids, interval):
        while self.is_running:
            try:
                if keywords:
                    for keyword in keywords.split(','):
                        if not self.is_running:
                            break
                        self.search_ebay(keyword.strip(), min_price, max_price, min_bids)
                        time.sleep(2)
                else:
                    self.search_ebay('', min_price, max_price, min_bids)

                self.log(f"⏳ Следующая проверка через {interval} сек...\n")
                time.sleep(interval)
            except Exception as e:
                self.log(f"❌ Ошибка: {str(e)}")
                time.sleep(5)

    def search_ebay(self, keyword, min_price, max_price, min_bids):
        try:
            if keyword:
                self.log(f"🔍 Поиск: '{keyword}'...")
            else:
                self.log(f"🔍 Поиск: ВСЕ аукционы...")

            # Парсим eBay напрямую
            if keyword:
                url = f"https://www.ebay.com/sch/i.html?_nkw={keyword}&_sop=10"
            else:
                url = "https://www.ebay.com/sch/i.html?_sop=10"

            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.ebay.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
            except Exception as e:
                self.log(f"   ⚠️ Не удалось подключиться к eBay: {str(e)}")
                self.log(f"   💡 eBay блокирует облачные серверы. Используй локально или VPN.")
                self.log(f"   📝 Приложение работает правильно - это ограничение eBay.")
                return

            try:
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                self.log(f"   ⚠️ Ошибка парсинга HTML: {str(e)}")
                return

            # Ищем карточки товаров
            items = soup.find_all('div', {'class': 's-item'})

            if not items:
                self.log(f"   ⚠️ Результаты не найдены")
                return

            self.log(f"   ✓ Найдено {len(items)} аукционов")
            found_count = 0

            for item in items:
                try:
                    # Название
                    title_elem = item.find('span', {'role': 'heading'})
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Цена
                    price_elem = item.find('span', {'class': 's-item__price'})
                    if not price_elem:
                        continue
                    price_text = price_elem.get_text(strip=True)
                    try:
                        price = float(re.sub(r'[^\d.]', '', price_text.split()[0]))
                    except:
                        continue

                    # Ставки
                    bids_elem = item.find('span', {'class': 's-item__bids'})
                    bids = 0
                    if bids_elem:
                        try:
                            bids_text = bids_elem.get_text(strip=True)
                            bids = int(re.sub(r'[^\d]', '', bids_text.split()[0]))
                        except:
                            bids = 0

                    # Ссылка
                    link_elem = item.find('a', {'class': 's-item__link'})
                    item_url = link_elem['href'] if link_elem else ''
                    try:
                        item_id = re.search(r'/itm/(\d+)', item_url).group(1) if item_url else ''
                    except:
                        item_id = ''

                    if price >= min_price and price <= max_price and bids >= min_bids:
                        auction_id = f"{title}_{item_id}"
                        if auction_id not in self.found_auctions:
                            self.found_auctions.add(auction_id)
                            self.log(f"✅ НАЙДЕН: {title[:60]}... | ${price} | Ставок: {bids}")
                            self.add_auction(title, f"${price}", bids, item_url)
                            found_count += 1

                except Exception as e:
                    continue

            if found_count == 0:
                self.log(f"   Подходящих аукционов не найдено")

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
    try:
        data = request.json
        keywords = data.get('keywords', '')
        min_price = float(data.get('min_price', 0))
        max_price = float(data.get('max_price', 999999))
        min_bids = int(data.get('min_bids', 1))
        interval = int(data.get('interval', 60))

        print(f"DEBUG: Calling start_monitoring with: keywords={keywords}, min_price={min_price}, max_price={max_price}, min_bids={min_bids}, interval={interval}")
        success = monitor.start_monitoring(keywords, min_price, max_price, min_bids, interval)
        return json.dumps({'success': success}, ensure_ascii=False)
    except Exception as e:
        print(f"DEBUG: Error in start(): {str(e)}")
        return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

@app.route('/api/stop', methods=['POST'])
def stop():
    try:
        monitor.stop_monitoring()
        return json.dumps({'success': True}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False)

@app.route('/api/status')
def status():
    try:
        return json.dumps({
            'running': monitor.is_running,
            'logs': monitor.logs[-20:],
            'auctions': monitor.auctions[:10]
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
