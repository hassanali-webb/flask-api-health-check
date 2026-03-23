from flask import Flask, jsonify, request, render_template
import datetime
import platform
import random
import time

app = Flask(__name__)
START_TIME = time.time()

# ──────────────────────────────────────────────
# HOME (Frontend UI)
# ──────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ──────────────────────────────────────────────
# HEALTH CHECK (Kubernetes)
# ──────────────────────────────────────────────
@app.route("/health")
def health():
    uptime = round(time.time() - START_TIME, 2)
    return jsonify({
        "status": "healthy",
        "uptime_seconds": uptime,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route("/readiness")
def readiness():
    return jsonify({
        "status": "ready",
        "checks": {
            "database": "ok",
            "cache": "ok",
            "dependencies": "ok"
        }
    }), 200

# ──────────────────────────────────────────────
# SYSTEM INFO
# ──────────────────────────────────────────────
@app.route("/info")
def info():
    return jsonify({
        "app": "FlaskAPI Demo",
        "version": "1.0.0",
        "python": platform.python_version(),
        "platform": platform.system(),
        "uptime_seconds": round(time.time() - START_TIME, 2)
    })

# ──────────────────────────────────────────────
# USERS (CRUD-style)
# ──────────────────────────────────────────────
USERS = [
    {"id": 1, "name": "Alice Nakamura", "role": "admin", "email": "alice@example.com"},
    {"id": 2, "name": "Bob Okafor", "role": "developer", "email": "bob@example.com"},
    {"id": 3, "name": "Clara Müller", "role": "designer", "email": "clara@example.com"},
    {"id": 4, "name": "David Patel", "role": "developer", "email": "david@example.com"},
]

@app.route("/users")
def get_users():
    return jsonify({"users": USERS, "total": len(USERS)})

@app.route("/users/<int:uid>")
def get_user(uid):
    user = next((u for u in USERS if u["id"] == uid), None)
    if not user:
        return jsonify({"error": "User not found", "id": uid}), 404
    return jsonify(user)

# ──────────────────────────────────────────────
# METRICS (Monitoring ready)
# ──────────────────────────────────────────────
@app.route("/metrics")
def metrics():
    return jsonify({
        "requests_total": random.randint(1000, 9999),
        "errors_total": random.randint(0, 50),
        "latency_p50_ms": round(random.uniform(5, 20), 2),
        "latency_p99_ms": round(random.uniform(80, 200), 2),
        "memory_mb": round(random.uniform(40, 120), 1),
        "cpu_percent": round(random.uniform(0.5, 15.0), 2)
    })

# ──────────────────────────────────────────────
# DEBUG / TEST ENDPOINT
# ──────────────────────────────────────────────
@app.route("/echo", methods=["GET", "POST"])
def echo():
    return jsonify({
        "method": request.method,
        "args": dict(request.args),
        "json": request.get_json(silent=True),
        "headers": {k: v for k, v in request.headers if k != "Cookie"}
    })

# ──────────────────────────────────────────────
# ERROR HANDLER
# ──────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Route not found",
        "hint": "Visit / for UI"
    }), 404

# ──────────────────────────────────────────────
# RUN APP (Production Ready for DevOps)
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)