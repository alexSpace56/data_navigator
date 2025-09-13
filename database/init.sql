-- Таблица справочник скважин
CREATE TABLE well (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    field VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('В работе', 'Остановлена', 'В ремонте', 'В простое')),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица событий по скважине
CREATE TABLE well_event (
    id SERIAL PRIMARY KEY,
    well_id INTEGER NOT NULL REFERENCES well(id),
    type VARCHAR(20) NOT NULL CHECK (type IN ('Запуск', 'Остановка', 'Перевод на другой режим')),
    event_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    initiated_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица бригад
CREATE TABLE crew (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    specialization VARCHAR(100),
    is_active BOOLEAN DEFAULT true
);

-- Таблица ремонтов
CREATE TABLE well_repair (
    id SERIAL PRIMARY KEY,
    well_id INTEGER NOT NULL REFERENCES well(id),
    crew_id INTEGER NOT NULL REFERENCES crew(id),
    start_date TIMESTAMP NOT NULL,
    planned_end_date TIMESTAMP,
    actual_end_date TIMESTAMP,
    repair_type VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'В планировании' CHECK (status IN ('В планировании', 'В работе', 'Завершен', 'Отменен'))
);

-- ТРИГГЕР: Автоматическое обновление timestamp при изменении скважины
CREATE OR REPLACE FUNCTION update_well_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_well_timestamp
    BEFORE UPDATE ON well
    FOR EACH ROW
    EXECUTE FUNCTION update_well_timestamp();

-- ТРИГГЕР: Автоматическое обновление статуса скважины при начале ремонта
CREATE OR REPLACE FUNCTION update_well_status_on_repair()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'В работе' THEN
        UPDATE well SET status = 'В ремонте' WHERE id = NEW.well_id;
    ELSIF NEW.status = 'Завершен' THEN
        UPDATE well SET status = 'В работе' WHERE id = NEW.well_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_well_repair_status
    AFTER INSERT OR UPDATE ON well_repair
    FOR EACH ROW
    EXECUTE FUNCTION update_well_status_on_repair();

-- ПРОЦЕДУРА: Расчет длительности ремонта
CREATE OR REPLACE FUNCTION calculate_repair_duration(repair_id INTEGER)
RETURNS INTERVAL AS $$
DECLARE
    duration INTERVAL;
BEGIN
    SELECT (actual_end_date - start_date) INTO duration
    FROM well_repair WHERE id = repair_id;

    RETURN duration;
END;
$$ LANGUAGE plpgsql;

-- ПРОЦЕДУРА: Получение текущего статуса скважины
CREATE OR REPLACE FUNCTION get_well_status(well_id INTEGER)
RETURNS TABLE(well_name VARCHAR, well_status VARCHAR, current_repair_status VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT w.name, w.status, wr.status
    FROM well w
    LEFT JOIN well_repair wr ON w.id = wr.well_id AND wr.status = 'В работе'
    WHERE w.id = well_id;
END;
$$ LANGUAGE plpgsql;

-- Наполнение демо-данными
INSERT INTO well (name, field, status) VALUES
('Скв-102', 'Приобское', 'В работе'),
('Скв-205', 'Самотлорское', 'В ремонте'),
('Скв-301', 'Федоровское', 'Остановлена');

INSERT INTO well_event (well_id, type, event_date, reason, initiated_by) VALUES
(1, 'Запуск', '2024-01-15 08:00:00', 'Плановый запуск после ТКРС', 'Иванов И.И.'),
(2, 'Остановка', '2024-01-20 14:30:00', 'Технологическая остановка', 'Петров П.П.');

INSERT INTO crew (name, specialization) VALUES
('Бригада КРС-1', 'Капитальный ремонт скважин'),
('Бригада КРС-2', 'Капитальный ремонт скважин'),
('Бригада ТКРС-1', 'Текущий ремонт скважин');

INSERT INTO well_repair (well_id, crew_id, start_date, planned_end_date, repair_type, description, status) VALUES
(2, 1, '2024-01-21 09:00:00', '2024-01-25 18:00:00', 'Текущий ремонт', 'Замена насосного оборудования', 'В работе');