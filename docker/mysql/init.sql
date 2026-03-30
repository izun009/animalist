-- ============================================================
-- USERS
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    full_name       VARCHAR(255) NOT NULL,
    hashed_password TEXT NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- ANIMALS
-- ============================================================
CREATE TABLE IF NOT EXISTS animals (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    endpoint     VARCHAR(255) NOT NULL UNIQUE,
    introduction TEXT,
    owner_id     BIGINT,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_animals_owner
        FOREIGN KEY (owner_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_animals_name
        CHECK (CHAR_LENGTH(name) > 1),

    CONSTRAINT chk_animals_endpoint
        CHECK (CHAR_LENGTH(endpoint) > 1),

    KEY idx_animals_owner_id (owner_id)
) ENGINE=InnoDB;

-- ============================================================
-- ANIMAL FACTS
-- ============================================================
CREATE TABLE IF NOT EXISTS animal_facts (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    animal_id   BIGINT NOT NULL,
    title       VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    position    INT NOT NULL,

    CONSTRAINT fk_facts_animal
        FOREIGN KEY (animal_id)
        REFERENCES animals(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_animal_fact_position
        UNIQUE (animal_id, position),

    KEY idx_animal_facts_animal_id (animal_id)
) ENGINE=InnoDB;

-- ============================================================
-- ANIMAL IMAGES
-- ============================================================
CREATE TABLE IF NOT EXISTS animal_images (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    animal_id   BIGINT NOT NULL,
    image_url   TEXT NOT NULL,
    position    INT NOT NULL,

    CONSTRAINT fk_images_animal
        FOREIGN KEY (animal_id)
        REFERENCES animals(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_animal_image_position
        UNIQUE (animal_id, position),

    KEY idx_animal_images_animal_id (animal_id)
) ENGINE=InnoDB;
