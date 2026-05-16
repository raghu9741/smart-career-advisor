try:
    from .app import app, initialize_app_data
except ImportError:
    from app import app, initialize_app_data


def main():
    with app.app_context():
        initialized = initialize_app_data()
        if initialized:
            print("Application data initialized.")
            return

        print("Database schema is not ready yet. Run migrations before seeding.")


if __name__ == "__main__":
    main()
