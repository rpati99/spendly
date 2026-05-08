import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database.db import get_db


@pytest.fixture
def authenticated_client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM expenses")
            db.execute("DELETE FROM users")
            db.execute("DELETE FROM sqlite_sequence WHERE name='users'")
            db.execute("DELETE FROM sqlite_sequence WHERE name='expenses'")
            db.commit()
            user_id = _seed_test_data(db)
        with client.session_transaction() as sess:
            sess["user_id"] = user_id
        yield client
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM expenses")
            db.execute("DELETE FROM users")
            db.commit()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def _seed_test_data(db):
    pw_hash = "pbkdf2:sha256:260000$test$hash"
    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Test User", "test@example.com", pw_hash),
    )
    db.commit()
    user_id = db.execute("SELECT last_insert_rowid() as id").fetchone()["id"]
    expenses = [
        ("Food", 10.00, "2026-05-01", "Breakfast"),
        ("Food", 15.00, "2026-05-02", "Lunch"),
        ("Transport", 30.00, "2026-05-03", "Uber"),
        ("Food", 20.00, "2026-05-04", "Dinner"),
        ("Bills", 100.00, "2026-05-05", "Electricity"),
        ("Food", 25.00, "2026-05-06", "Coffee"),
        ("Transport", 50.00, "2026-05-07", "Gas"),
        ("Food", 35.00, "2026-05-08", "Brunch"),
        ("Health", 80.00, "2026-05-09", "Pharmacy"),
        ("Food", 18.00, "2026-05-10", "Snacks"),
        ("Shopping", 200.00, "2026-05-11", "Clothes"),
        ("Food", 22.00, "2026-05-12", "Dinner"),
        ("Entertainment", 45.00, "2026-05-13", "Movies"),
        ("Food", 28.00, "2026-05-14", "Lunch"),
        ("Transport", 15.00, "2026-05-15", "Bus"),
        ("Food", 12.00, "2026-05-16", "Breakfast"),
        ("Bills", 150.00, "2026-05-17", "Internet"),
        ("Food", 19.00, "2026-05-18", "Coffee"),
        ("Health", 60.00, "2026-05-19", "Gym"),
        ("Food", 31.00, "2026-05-20", "Dinner"),
    ]
    for cat, amt, dt, desc in expenses:
        db.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, amt, cat, dt, desc),
        )
    db.commit()
    return user_id


class TestProfileHistoryDateFilter:
    def test_history_no_filter_returns_all_expenses(self, authenticated_client):
        response = authenticated_client.get("/profile/history")
        assert response.status_code == 200
        data = response.data.decode()
        assert "2026-05-01" in data
        assert "2026-05-20" in data

    def test_history_with_start_and_end_filter(self, authenticated_client):
        response = authenticated_client.get("/profile/history?start=2026-05-05&end=2026-05-10")
        assert response.status_code == 200
        data = response.data.decode()
        assert "2026-05-05" in data
        assert "2026-05-10" in data
        assert "2026-05-01" not in data
        assert "2026-05-20" not in data

    def test_history_only_start_date(self, authenticated_client):
        response = authenticated_client.get("/profile/history?start=2026-05-15")
        assert response.status_code == 200
        data = response.data.decode()
        assert "2026-05-15" in data
        assert "2026-05-20" in data
        assert "2026-05-01" not in data

    def test_history_only_end_date(self, authenticated_client):
        response = authenticated_client.get("/profile/history?end=2026-05-05")
        assert response.status_code == 200
        data = response.data.decode()
        assert "2026-05-01" in data
        assert "2026-05-05" in data
        assert "2026-05-06" not in data

    def test_history_date_boundary_inclusive(self, authenticated_client):
        response = authenticated_client.get("/profile/history?start=2026-05-05&end=2026-05-07")
        assert response.status_code == 200
        data = response.data.decode()
        assert "2026-05-05" in data
        assert "2026-05-06" in data
        assert "2026-05-07" in data
        assert "2026-05-04" not in data
        assert "2026-05-08" not in data

    def test_history_pagination_preserves_date_params(self, authenticated_client):
        response = authenticated_client.get("/profile/history?start=2026-05-05&end=2026-05-15&page=1")
        assert response.status_code == 200
        data = response.data.decode()
        assert "2026-05-05" in data
        assert "2026-05-15" in data


class TestProfileStatsDateFilter:
    def test_stats_no_filter_returns_all(self, authenticated_client):
        response = authenticated_client.get("/profile/stats")
        assert response.status_code == 200
        data = response.data.decode()
        assert "965" in data

    def test_stats_with_date_filter(self, authenticated_client):
        response = authenticated_client.get("/profile/stats?start=2026-05-01&end=2026-05-05")
        assert response.status_code == 200
        data = response.data.decode()
        assert "2026-05-01" in data
        assert "2026-05-05" in data

    def test_stats_recalculates_correctly(self, authenticated_client):
        all_response = authenticated_client.get("/profile/stats")
        filtered_response = authenticated_client.get("/profile/stats?start=2026-05-10&end=2026-05-15")

        assert all_response.status_code == 200
        assert filtered_response.status_code == 200

        all_data = all_response.data.decode()
        filtered_data = filtered_response.data.decode()

        assert all_data != filtered_data


class TestProfileCategoriesDateFilter:
    def test_categories_no_filter_returns_all(self, authenticated_client):
        response = authenticated_client.get("/profile/categories")
        assert response.status_code == 200
        data = response.data.decode()
        assert "Food" in data
        assert "Transport" in data
        assert "Bills" in data

    def test_categories_with_date_filter(self, authenticated_client):
        response = authenticated_client.get("/profile/categories?start=2026-05-01&end=2026-05-05")
        assert response.status_code == 200
        data = response.data.decode()
        assert "Food" in data
        assert "Transport" in data
        assert "Bills" in data

    def test_categories_breakdown_recalculates(self, authenticated_client):
        all_response = authenticated_client.get("/profile/categories")
        filtered_response = authenticated_client.get("/profile/categories?start=2026-05-01&end=2026-05-05")

        assert all_response.status_code == 200
        assert filtered_response.status_code == 200

        all_data = all_response.data.decode()
        filtered_data = filtered_response.data.decode()

        assert all_data != filtered_data


class TestAuthGuard:
    def test_history_requires_auth(self, client):
        response = client.get("/profile/history")
        assert response.status_code == 302
        assert "/login" in response.location

    def test_stats_requires_auth(self, client):
        response = client.get("/profile/stats")
        assert response.status_code == 302
        assert "/login" in response.location

    def test_categories_requires_auth(self, client):
        response = client.get("/profile/categories")
        assert response.status_code == 302
        assert "/login" in response.location

    def test_history_with_date_filter_requires_auth(self, client):
        response = client.get("/profile/history?start=2026-05-01&end=2026-05-10")
        assert response.status_code == 302
        assert "/login" in response.location

    def test_stats_with_date_filter_requires_auth(self, client):
        response = client.get("/profile/stats?start=2026-05-01&end=2026-05-10")
        assert response.status_code == 302
        assert "/login" in response.location

    def test_categories_with_date_filter_requires_auth(self, client):
        response = client.get("/profile/categories?start=2026-05-01&end=2026-05-10")
        assert response.status_code == 302
        assert "/login" in response.location