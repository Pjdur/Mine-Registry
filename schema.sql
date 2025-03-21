CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    package_name TEXT NOT NULL,
    package_version TEXT NOT NULL,
    description TEXT NOT NULL,
    main_file TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES users (username)
);