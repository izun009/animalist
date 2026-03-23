CREATE TABLE IF NOT EXISTS animals (
    a_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    endpoint TEXT NOT NULL UNIQUE,
    introduction TEXT,
    owner_id INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS animal_facts (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL REFERENCES animals(a_id) ON DELETE CASCADE,
    title TEXT,
    description TEXT,
    position INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS animal_images (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL REFERENCES animals(a_id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    position INTEGER NOT NULL,
    UNIQUE (animal_id, image_url)
);
