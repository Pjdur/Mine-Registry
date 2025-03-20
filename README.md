# Mine Package Registry

This is a simple package registry for the Mine programming language. Users can sign up, log in, and publish packages.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/mine-package-registry.git
cd mine-package-registry
```

2. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file based on the `.env.example` file and set the `DATABASE_URL`:

```bash
cp .env.example .env
```

4. Run the application:

```bash
python app.py
```

## Endpoints

- `POST /signup`: Create a new user.
  - Request body: `{ "username": "user", "password": "pass" }`
- `POST /login`: Log in a user.
  - Request body: `{ "username": "user", "password": "pass" }`
- `POST /publish`: Publish a new package.
  - Request body: `{ "username": "user", "package_name": "pkg", "package_version": "1.0.0" }`

## License

This project is licensed under the MIT License.