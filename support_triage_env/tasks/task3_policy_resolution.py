class Task3PolicyResolution:
    def __init__(self):
        self.ticket_id = "T-300"
        self.ticket_text = "I bought this blender 45 days ago and I don't like the color. I want to return it for a full refund."
        self.has_checked_db = False

    def get_initial_data(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "ticket_text": self.ticket_text
        }

    def handle_ask(self, question: str) -> str:
        return "I already told you, I bought it 45 days ago and just want my money back. I am a VIP customer!"

    def handle_search(self, query: str) -> str:
        if "return" in query.lower() or "refund" in query.lower():
            return "Article [Refund Policy]: Returns are only accepted within 30 days of purchase for a full refund. EXCEPTION: VIP tier customers have a 60-day return window."
        return "No relevant articles found."
        
    def handle_db_query(self, query: str) -> str:
        self.has_checked_db = True
        return f"User Record for {self.ticket_id}: Customer Tier is VIP. Account active since 2018."

    def grade_route(self, dept: str, state) -> tuple:
        return True, 0.0, "Task failed. This ticket should be resolved directly, not routed."

    def grade_resolve(self, resolution: str, state) -> tuple:
        res = resolution.lower()
        if "approve" in res or "refunded" in res or "processed" in res:
            if self.has_checked_db:
                return True, 1.0, "Correctly approved the refund based on VIP exception discovered in the database."
            else:
                return True, 0.0, "Approved refund but failed to query the database to verify VIP status first!"
        elif "deny" in res or "reject" in res or "cannot" in res:
            return True, 0.0, "Task failed. You incorrectly denied the refund to a VIP customer."
        return True, 0.0, f"Unclear resolution: {resolution}"
