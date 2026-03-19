-- Create database extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for better performance
-- These will be created by SQLAlchemy but we can add them here for reference

-- Users table indexes
-- CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
-- CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Models table indexes
-- CREATE INDEX IF NOT EXISTS idx_models_user_id ON models(user_id);
-- CREATE INDEX IF NOT EXISTS idx_models_model_id ON models(model_id);
-- CREATE INDEX IF NOT EXISTS idx_models_created_at ON models(created_at);

-- Model edits table indexes
-- CREATE INDEX IF NOT EXISTS idx_model_edits_model_id ON model_edits(model_id);
-- CREATE INDEX IF NOT EXISTS idx_model_edits_user_id ON model_edits(user_id);
