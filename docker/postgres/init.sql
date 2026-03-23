-- ============================================================
-- ANIMALS
-- ============================================================
CREATE TABLE IF NOT EXISTS animals (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name         TEXT        NOT NULL,
    endpoint     TEXT        NOT NULL UNIQUE,
    introduction TEXT,
    owner_id     BIGINT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_animals_owner
        FOREIGN KEY (owner_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_animals_name
        CHECK (char_length(name) > 1),

    CONSTRAINT chk_animals_endpoint
        CHECK (char_length(endpoint) > 1)
);

CREATE INDEX IF NOT EXISTS idx_animals_owner_id
    ON animals(owner_id);

-- ============================================================
-- ANIMAL FACTS
-- ============================================================
CREATE TABLE IF NOT EXISTS animal_facts (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    animal_id   BIGINT NOT NULL,
    title       TEXT NOT NULL,
    description TEXT NOT NULL,
    position    INTEGER NOT NULL,

    CONSTRAINT fk_facts_animal
        FOREIGN KEY (animal_id)
        REFERENCES animals(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_animal_fact_position
        UNIQUE (animal_id, position)
);

CREATE INDEX IF NOT EXISTS idx_animal_facts_animal_id
    ON animal_facts (animal_id);

-- ============================================================
-- ANIMAL IMAGES
-- ============================================================
CREATE TABLE IF NOT EXISTS animal_images (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    animal_id   BIGINT NOT NULL,
    image_url   TEXT    NOT NULL,
    position    INTEGER NOT NULL,

    CONSTRAINT fk_images_animal
        FOREIGN KEY (animal_id)
        REFERENCES animals(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_animal_image_position
        UNIQUE (animal_id, position)
);

CREATE INDEX IF NOT EXISTS idx_animal_images_animal_id
    ON animal_images (animal_id);