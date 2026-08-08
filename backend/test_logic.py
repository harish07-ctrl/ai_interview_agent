"""
Quick test script — run this with: python test_logic.py
No server needed. Just checks that interview_logic.py works.
"""

import json
from interview_logic import pick_focus_days, generate_next_question_llm, generate_feedback_llm

# Load a real candidate from your data file
with open("data/candidates.json") as f:
    data = json.load(f)

candidate = data["candidates"][15]  # Isabella Rossi — has some real failures to probe
print("Testing with candidate:", candidate["member"]["name"])

# Step 1: see which days get prioritized
focus_list = pick_focus_days(candidate, already_asked=set())
print("\nTop focus days (priority, day, mission title):")
for priority, day, mission in focus_list[:3]:
    print(f"  priority={priority} day={day} -> {mission['title']}")

# Step 2: generate an opening question
history = []
question = generate_next_question_llm(candidate, history, set(), mission=focus_list[0][2])
print("\nGenerated question:\n", question)

# Step 3: simulate a candidate answer, then generate feedback
history.append({"role": "assistant", "content": question})
history.append({"role": "user", "content": "I used cosine similarity to compare embeddings, but honestly I'm still fuzzy on why it works better than Euclidean distance for text."})

feedback = generate_feedback_llm(history)
print("\nGenerated feedback:\n", json.dumps(feedback, indent=2))
