class Task2InfoGathering:
    def __init__(self):
        self.ticket_id = "T-200"
        self.ticket_text = "The app keeps crashing when I try to upload a profile picture."
        self.has_asked_version = False
        self.expected_dept = "Engineering"

    def get_initial_data(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "ticket_text": self.ticket_text
        }

    def handle_ask(self, question: str) -> str:
        q = question.lower()
        if "version" in q or "os" in q or "device" in q or "app" in q:
            self.has_asked_version = True
            return "I am using iOS version 16.4 on an iPhone 13, app version 2.1.0."
        return "I don't understand. I just click upload and it closes!"

    def handle_search(self, query: str) -> str:
        if "crash" in query.lower() or "upload" in query.lower():
            return "Article: Crash reports must include OS and app version before routing to Engineering."
        return "No relevant articles found."

    def grade_route(self, dept: str, state) -> tuple:
        if dept.lower() == self.expected_dept.lower():
            if self.has_asked_version:
                return True, 1.0, f"Correctly gathered info and routed to {self.expected_dept}"
            else:
                return True, 0.5, "Routed to Engineering, but failed to ask for OS/App version first."
        else:
            return True, 0.0, f"Incorrect routing to {dept}."

    def grade_resolve(self, resolution: str, state) -> tuple:
        return True, 0.0, "Task failed. Bug reports must be routed to Engineering."
