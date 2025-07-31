-- seed.sql

-- Insert sample users
INSERT INTO users (username, email) VALUES
('alice_dev', 'alice@example.com'),
('bob_coder', 'bob@example.com'),
('charlie_ai', 'charlie@example.com');

-- Insert lessons (AI learning roadmap)
INSERT INTO lessons (title, description, phase) VALUES
('Prompt Engineering', 'Learn how to craft clear, effective prompts to guide AI tools.', 1),
('Code Generation & Refactoring', 'Use AI to write and refactor real-world code snippets.', 2),
('Debugging & Explanation', 'Leverage AI to explain code behavior and assist in bug fixing.', 3),
('Workflow Automation', 'Automate common tasks using AI tools and scripts.', 4),
('Prototyping Apps with AI', 'Design full-stack apps using AI-generated components.', 5);

-- Insert lesson content for Lesson 1
INSERT INTO lesson_content (lesson_id, content, step_number) VALUES
(1, 'What is a prompt? Understand the basic concept and its role in LLM interaction.', 1),
(1, 'Prompt structure: Task + Context + Constraints.', 2),
(1, 'Rewrite vague prompts into clear, goal-oriented ones.', 3),
(1, 'Compare examples of weak vs. strong prompts.', 4),
(1, 'Hands-on: Practice your own prompts using the sandbox.', 5);

-- Insert quizzes for Lesson 1
INSERT INTO quizzes (lesson_id, question, answer) VALUES
(1, 'What are the three key parts of a good prompt?', 'Task, Context, Constraints'),
(1, 'Which of the following is a better prompt: (A) "Make code" or (B) "Generate a Python class that models a shopping cart with add/remove methods"?', 'B');

-- Insert user progress
-- Alice: Completed lessons 1 & 2, working on lesson 3
INSERT INTO user_progress (user_id, lesson_id, completed) VALUES
(1, 1, TRUE),
(1, 2, TRUE),
(1, 3, FALSE);

-- Bob: Only started lesson 1
INSERT INTO user_progress (user_id, lesson_id, completed) VALUES
(2, 1, FALSE);

-- Charlie: Hasn't started anything
-- (no rows needed for user_id 3 yet)