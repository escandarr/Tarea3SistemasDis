#cache_monitor/cache_monitor.py
from flask import Flask, jsonify, render_template
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    hits = int(r.get("hits") or 0)
    misses = int(r.get("misses") or 0)
    total = hits + misses
    hit_rate = (hits / total) * 100 if total > 0 else 0
    miss_rate = (misses / total) * 100 if total > 0 else 0
    politica = r.config_get('maxmemory-policy').get('maxmemory-policy', 'unknown')

    return jsonify({
        "hits": hits,
        "misses": misses,
        "total_consultas": total,
        "hit_rate": round(hit_rate, 2),
        "miss_rate": round(miss_rate, 2),
        "politica": politica
    })

@app.route('/reset', methods=['POST'])
def reset():
    r.flushall()
    return jsonify({"status": "OK", "message": "Cache y métricas reseteadas correctamente."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000)