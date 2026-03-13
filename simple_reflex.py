import matplotlib.pyplot as plt

# Simple reflex agent rule
def reflex_agent(percept):
    if percept == "Dirty":
        return "Clean"
    else:
        return "No Action"

# Environment (rooms)
rooms = ["Clean", "Dirty", "Dirty", "Clean", "Dirty"]

# Convert to numeric for visualization
values = [1 if r == "Dirty" else 0 for r in rooms]

# Plot before cleaning
plt.figure()
plt.title("Room Status Before Agent Action")
plt.bar(range(len(rooms)), values)
plt.xlabel("Room Number")
plt.ylabel("Status (1=Dirty, 0=Clean)")
plt.show()

# Agent actions
for i in range(len(rooms)):
    action = reflex_agent(rooms[i])
    print("Room", i+1, ":", rooms[i], "-> Agent Action:", action)
    
    if action == "Clean":
        rooms[i] = "Clean"

# Convert again after cleaning
values_after = [1 if r == "Dirty" else 0 for r in rooms]

# Plot after cleaning
plt.figure()
plt.title("Room Status After Agent Action")
plt.bar(range(len(rooms)), values_after)
plt.xlabel("Room Number")
plt.ylabel("Status (1=Dirty, 0=Clean)")
plt.show()