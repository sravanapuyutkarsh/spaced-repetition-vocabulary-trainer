
-- Sample vocabulary data for the Spaced Repetition Vocabulary Trainer.
-- Run against a database that has already been initialized with the
-- words and reviews tables.

INSERT INTO words (word, definition, language, created_at)
VALUES
    ('Abundant', 'Available in large quantities; plentiful.', 'English', CURRENT_TIMESTAMP),
    ('Resilient', 'Able to recover quickly from difficulties.', 'English', CURRENT_TIMESTAMP),
    ('Meticulous', 'Showing great attention to detail.', 'English', CURRENT_TIMESTAMP);

-- Make each new word available for its first review immediately.
INSERT INTO reviews
    (word_id, review_date, score, interval, easiness_factor, repetition, next_review)
SELECT
    id,
    CURRENT_TIMESTAMP,
    NULL,
    1,
    2.5,
    0,
    CURRENT_TIMESTAMP
FROM words
WHERE word IN ('Abundant', 'Resilient', 'Meticulous')
  AND language = 'English'
  AND NOT EXISTS (
      SELECT 1
      FROM reviews
      WHERE reviews.word_id = words.id
  );
