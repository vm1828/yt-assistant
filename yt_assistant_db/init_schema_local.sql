CREATE EXTENSION IF NOT EXISTS vector;

-- account table
CREATE TABLE IF NOT EXISTS account (
    id VARCHAR PRIMARY KEY
);

-- video table
CREATE TABLE IF NOT EXISTS video (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR NOT NULL,
    url VARCHAR NOT NULL
);

-- account_video table (junction table)
CREATE TABLE IF NOT EXISTS account_video (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    account_id VARCHAR NOT NULL,
    video_id UUID NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE,
    FOREIGN KEY (video_id) REFERENCES video(id) ON DELETE CASCADE
);

-- transcript table
CREATE TABLE IF NOT EXISTS transcript (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    video_id UUID NOT NULL,
    transcript_text TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES video(id) ON DELETE CASCADE
);

-- summaries table
CREATE TABLE IF NOT EXISTS summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    video_id UUID NOT NULL,
    summary_text TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES video(id) ON DELETE CASCADE
);

-- qa table
CREATE TABLE IF NOT EXISTS qa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    account_id VARCHAR NOT NULL,
    video_id UUID NOT NULL,
    question_text TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE,
    FOREIGN KEY (video_id) REFERENCES video(id) ON DELETE CASCADE
);

-- embedding table
CREATE TABLE IF NOT EXISTS embedding (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    video_id UUID NOT NULL,
    embedding vector(768),
    FOREIGN KEY (video_id) REFERENCES video(id) ON DELETE CASCADE
);

