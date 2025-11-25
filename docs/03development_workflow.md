# 🔄 DEVELOPMENT WORKFLOW

## 1. Branching Strategy
We use a simplified **Git Flow**:
*   **`main`**: The "Gold Standard". Only fully working code goes here.
*   **`dev`**: The "Construction Zone". All daily work happens here.

## 2. The Rules
1.  **Never push to main.** Always push to `dev`.
2.  **Commit Messages:** Must be clear.
    *   ❌ Bad: "Fixed stuff"
    *   ✅ Good: "Added MQTT connection logic to ingestion service"

## 3. Project Management (Kanban)
To track tasks, we will use **GitHub Projects** (or Trello/Notion).
**Columns:**
1.  **To Do** (Backlog)
2.  **In Progress** (Currently coding)
3.  **Done** (Tested and working)
