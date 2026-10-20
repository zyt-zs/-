CREATE TABLE IF NOT EXISTS flights (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_no   TEXT NOT NULL,
    airline     TEXT NOT NULL,
    dep_city    TEXT NOT NULL,
    dep_airport TEXT NOT NULL,
    arr_city    TEXT NOT NULL,
    arr_airport TEXT NOT NULL,
    dep_time    TEXT NOT NULL,
    arr_time    TEXT NOT NULL,
    duration    INTEGER NOT NULL,
    price       REAL NOT NULL,
    seats_left  INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_route ON flights(dep_city, arr_city, dep_time);