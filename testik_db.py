# test_start.py
print("🔍 Проверка установки...")

try:
    import flask
    print("✅ Flask работает")
except Exception as e:
    print(f"❌ Flask: {e}")

try:
    import psycopg2
    print("✅ psycopg2 работает (SQL без ORM)")
except Exception as e:
    print(f"❌ psycopg2: {e}")

try:
    import jwt
    print("✅ PyJWT работает")
except Exception as e:
    print(f"❌ PyJWT: {e}")

try:
    import bcrypt
    print("✅ bcrypt работает")
except Exception as e:
    print(f"❌ bcrypt: {e}")

try:
    import fastapi
    print("✅ FastAPI работает")
except Exception as e:
    print(f"❌ FastAPI: {e}")

print("\n🎉 Если все ✅ — переходим к коду!")