class Task1BasicRoute:
    def __init__(self):
        self.ticket_id = "T-100"
        self.ticket_text = "Hi, I forgot my password to the dashboard. Please help me reset it."
        self.expected_dept = "IT Support"

    def get_initial_data(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "ticket_text": self.ticket_text
        }

    def handle_ask(self, question: str) -> str:
        return "Just send me the password reset link, please."

    def handle_search(self, query: str) -> str:
        if "password" in query.lower():
            return "Article: Password Resets are handled by IT Support."
        return "No relevant articles found."

    def grade_route(self, dept: str, state) -> tuple:
        if dept.lower() == self.expected_dept.lower():
            return True, 1.0, f"Correctly routed to {self.expected_dept}"
        else:
            return True, 0.0, f"Incorrect routing. Routed to {dept} instead of {self.expected_dept}"

    def grade_resolve(self, resolution: str, state) -> tuple:
        return True, 0.0, "Task failed. This ticket should be routed, not resolved."
